# Scripts de base de datos

| Archivo | Uso |
|---|---|
| `check_schema.sh` | Verifica que el esquema de `linadb` coincida con las migraciones del repositorio. No modifica `linadb`. Se puede ejecutar en cualquier momento. |
| `schema_diff.py` | Comparador que usa `check_schema.sh`. |
| `20261027_migrations_baseline.sql` | Corrección única: nueva línea base de migraciones. Ver más abajo. |

## Línea base de migraciones (2026-10-27)

Hasta esta fecha las carpetas `migrations/` estaban en `.gitignore`, y los archivos que se
aplicaron en cada servidor se perdieron. Ahora el repositorio contiene migraciones iniciales
(`0001_initial`) generadas desde los modelos actuales. Cada base de datos existente tiene que
pasar **una sola vez** a esa línea base. Después de eso, los cambios de modelo siguen el flujo
normal: `makemigrations`, commit de los archivos y `migrate`.

El script SQL:

1. Elimina las tablas `*_copy` y `*_tmp`, que no tienen modelo.
2. Convierte a `utf8` las tablas que estaban en `latin1` y restaura los `JSONField` de `catalog_catalogm`.
3. Ajusta `catalog_pdfjob.celery_task_id` a `NOT NULL` y elimina un índice sobrante de `linabi_xlsxtemplatecol`.
4. Reemplaza en `django_migrations` los registros de `core`, `catalog`, `saleapp`, `linabi`, `wms` e `inv`
   por los nuevos `0001_initial`. Si las tablas de `django_celery_beat` no existen, también borra sus
   registros (fueron aplicados con `--fake`), para que `migrate` las cree.

Ya se aplicó en desarrollo.

### Procedimiento en producción

Desde el directorio del proyecto en el servidor, con los contenedores en marcha:

```sh
# 1. Respaldo
mkdir -p ~/linaee_backups
docker exec linadb sh -c 'mysqldump -uroot -p"$MYSQL_ROOT_PASSWORD" --single-transaction --routines --triggers --default-character-set=utf8mb4 "$MYSQL_DATABASE"' \
  > ~/linaee_backups/linaee_prod_$(date +%Y%m%d_%H%M%S).sql
tail -1 ~/linaee_backups/linaee_prod_*.sql   # debe decir "-- Dump completed on ..."

# 2. Apartar las migraciones locales viejas (no versionadas) y traer el código.
#    Si quedaran, bloquearían el pull o se mezclarían con las nuevas.
mkdir -p ~/linaee_backups/old_migrations
for d in linabe/apps/*/migrations; do
  [ -d "$d" ] && mv "$d" ~/linaee_backups/old_migrations/$(basename $(dirname $d))
done
git pull
git status --short linabe/apps   # no debe listar nada

# 3. Diagnóstico ANTES de corregir (no modifica nada)
./linabe/scripts/db/check_schema.sh
```

Revisa la salida del paso 3 antes de continuar. Si las diferencias son las que corrige el script
(tablas `latin1`, `celery_task_id`, índice `name`, tablas `_copy`/`_tmp`, tablas de `django_celery_beat`
y registros de `django_migrations`), continúa. Si aparece algo distinto, **detente**: el script fue
escrito para el esquema de desarrollo y habrá que ajustarlo.

```sh
# 4. Corrección y línea base
docker exec -i linadb sh -c 'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" "$MYSQL_DATABASE"' \
  < linabe/scripts/db/20261027_migrations_baseline.sql
docker exec linabe python manage.py migrate

# 5. Verificación: debe terminar con "Esquema coherente: sin diferencias..."
./linabe/scripts/db/check_schema.sh
docker exec linabe python manage.py migrate --check
```

Para revertir, restaura el respaldo del paso 1:

```sh
docker exec -i linadb sh -c 'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" "$MYSQL_DATABASE"' < ~/linaee_backups/<archivo>.sql
```
