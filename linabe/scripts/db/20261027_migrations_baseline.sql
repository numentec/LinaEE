-- Corrección de esquema y nueva línea base de migraciones (2026-10-27).
--
-- Se ejecuta UNA sola vez por base de datos, con el código que ya incluye
-- los archivos 0001_initial versionados. Ver README.md antes de usarlo.
-- Requiere MariaDB >= 10.5 (ALTER TABLE IF EXISTS / DROP INDEX IF EXISTS).

SET FOREIGN_KEY_CHECKS = 0;

-- 1. Tablas sin modelo, restos de pruebas (quedan en el respaldo previo).
DROP TABLE IF EXISTS catalog_catalogd_copy, catalog_catalogm_copy, core_vistaconfig_copy, core_vistaconfig_tmp;

-- 2. Tablas en latin1: se igualan al resto de la base (utf8).
ALTER TABLE IF EXISTS catalog_catalogd          CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE IF EXISTS catalog_catalogd_tags     CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE IF EXISTS catalog_catalogdimg       CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE IF EXISTS catalog_catalogm          CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE IF EXISTS catalog_catalogm_customer CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE IF EXISTS catalog_category          CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE IF EXISTS catalog_tag               CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE IF EXISTS core_customer             CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;

-- CONVERT TO también alcanza a los JSONField (en MariaDB, JSON = longtext utf8mb4_bin):
-- se restauran como los crea Django.
ALTER TABLE catalog_catalogm
    MODIFY pages    longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`pages`)),
    MODIFY settings longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`settings`)),
    MODIFY theme    longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`theme`));

SET FOREIGN_KEY_CHECKS = 1;

-- 3. PdfJob.celery_task_id es NOT NULL default '' en el modelo.
UPDATE catalog_pdfjob SET celery_task_id = '' WHERE celery_task_id IS NULL;
ALTER TABLE catalog_pdfjob MODIFY celery_task_id varchar(64) NOT NULL;

-- 4. Índice que no está definido en el modelo BIXLSXTemplateCol.
DROP INDEX IF EXISTS `name` ON linabi_xlsxtemplatecol;

-- 5. Nueva línea base en django_migrations.
START TRANSACTION;

-- Registros de migraciones cuyos archivos ya no existen.
DELETE FROM django_migrations WHERE app IN ('core', 'catalog', 'saleapp', 'linabi', 'wms', 'inv');

-- django_celery_beat figura aplicada con --fake, pero sus tablas no existen:
-- se borran sus registros para que `migrate` las cree de verdad.
DELETE FROM django_migrations
 WHERE app = 'django_celery_beat'
   AND NOT EXISTS (SELECT 1 FROM information_schema.tables
                    WHERE table_schema = DATABASE() AND table_name = 'django_celery_beat_periodictask');

-- El esquema ya existe: las migraciones iniciales se registran como aplicadas.
INSERT INTO django_migrations (app, name, applied) VALUES
    ('core',    '0001_initial',           UTC_TIMESTAMP(6)),
    ('catalog', '0001_initial',           UTC_TIMESTAMP(6)),
    ('catalog', '0002_initial_relations', UTC_TIMESTAMP(6)),
    ('linabi',  '0001_initial',           UTC_TIMESTAMP(6)),
    ('saleapp', '0001_initial',           UTC_TIMESTAMP(6)),
    ('wms',     '0001_initial',           UTC_TIMESTAMP(6));

COMMIT;
