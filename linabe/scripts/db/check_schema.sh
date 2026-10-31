#!/usr/bin/env sh
# Verifica que el esquema de linadb coincida con lo que esperan las migraciones.
#
# Levanta un MariaDB temporal (misma imagen que linadb) en la red de linabe,
# le aplica las migraciones del repositorio y compara ambos esquemas.
# No modifica linadb. Ejecutar desde el host, con los contenedores en marcha.

set -e

REF=linadb_ref
REF_PW=$(od -An -N12 -tx1 /dev/urandom | tr -d ' \n')
IMAGE=$(docker inspect -f '{{.Config.Image}}' linadb)
NETWORK=$(docker inspect -f '{{range $k, $v := .NetworkSettings.Networks}}{{$k}}{{end}}' linabe)

cleanup() { docker stop "$REF" >/dev/null 2>&1 || true; }
trap cleanup EXIT

docker run -d --rm --name "$REF" --network "$NETWORK" \
  -e PUID=1000 -e PGID=1000 -e MYSQL_ROOT_PASSWORD="$REF_PW" -e MYSQL_DATABASE=linaee_ref \
  -e MYSQL_USER=ref -e MYSQL_PASSWORD="$REF_PW" \
  "$IMAGE" >/dev/null

echo "Esperando BD de referencia..."
i=0
until docker exec "$REF" mysql -uroot -p"$REF_PW" -e 'select 1' linaee_ref >/dev/null 2>&1; do
  i=$((i + 1))
  [ "$i" -gt 60 ] && echo "La BD de referencia no respondió" && exit 1
  sleep 2
done

echo "Aplicando migraciones en la BD de referencia..."
docker exec -e DB_HOST="$REF" -e DB_PORT=3306 -e DB_NAME=linaee_ref -e DB_USER=root -e DB_USER_PW="$REF_PW" \
  linabe python manage.py migrate --noinput >/dev/null

echo "Comparando esquemas..."
docker exec -e REF_DB_HOST="$REF" -e REF_DB_PW="$REF_PW" linabe python scripts/db/schema_diff.py
