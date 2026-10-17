create or replace PROCEDURE     LINAEE_SHOPPINGCARTSUGGEST
(
    PDEPTO IN VARCHAR2 DEFAULT '%',
    PCAT IN VARCHAR2 DEFAULT '0',
    PSCAT IN VARCHAR2 DEFAULT '0',
    PBRANDS IN VARCHAR2 DEFAULT NULL,
    PCIA IN VARCHAR2 DEFAULT '01',
    P_TEXT IN VARCHAR2 DEFAULT NULL,
    RESULTSET OUT SYS_REFCURSOR
) AS
    c_max_rows CONSTANT NUMBER := 20;
    -- Longer descriptions cannot be sent back as a filter, so they are not offered.
    c_max_name_length CONSTANT NUMBER := 100;
    vPDEPTO VARCHAR2(100);
    v_text VARCHAR2(100) := TRIM(P_TEXT);
    v_pattern VARCHAR2(200);
    v_brands VARCHAR2(4000) := TRIM(PBRANDS);
    v_brands_active NUMBER := 0;
BEGIN
    vPDEPTO := CASE WHEN PDEPTO = '0' THEN '%' ELSE PDEPTO END;

    IF v_text IS NULL OR LENGTH(v_text) < 2 THEN
        OPEN RESULTSET FOR SELECT CAST(NULL AS VARCHAR2(500)) AS "name",
                                  CAST(NULL AS NUMBER) AS "products"
                           FROM dual WHERE 1 = 0;
        RETURN;
    END IF;

    IF LENGTH(v_text) > 50 THEN
        RAISE_APPLICATION_ERROR(-20006, 'Text filter is too long');
    END IF;

    -- Escapes LIKE wildcards so user text is matched literally.
    v_pattern := '%'
        || UPPER(REPLACE(REPLACE(REPLACE(v_text, '\', '\\'), '%', '\%'), '_', '\_'))
        || '%';

    IF v_brands IS NOT NULL THEN
        v_brands_active := 1;
    END IF;

    OPEN RESULTSET FOR
        SELECT *
        FROM (
            SELECT descrip AS "name", COUNT(sku) AS "products"
            FROM DMC.LINAEE_CATALOGO_VW
            WHERE NVL(cant_fisica + cant_transito + cant_transito_fut, 0) > 0
              AND bodega = 'BC1'
              AND co_subcat LIKE vPDEPTO
              AND (PCAT = '0' OR co_cat = TO_NUMBER(PCAT))
              AND (PSCAT = '0' OR co_dep = TO_NUMBER(PSCAT))
              AND (v_brands_active = 0
                   OR co_marca IN (
                       SELECT TRIM(REGEXP_SUBSTR(v_brands, '[^,]+', 1, LEVEL))
                       FROM dual
                       CONNECT BY LEVEL <= REGEXP_COUNT(v_brands, '[^,]+')
                   ))
              AND LENGTH(descrip) <= c_max_name_length
              AND UPPER(descrip) LIKE v_pattern ESCAPE '\'
            GROUP BY descrip
            ORDER BY descrip
        )
        WHERE ROWNUM <= c_max_rows;
END LINAEE_SHOPPINGCARTSUGGEST;
