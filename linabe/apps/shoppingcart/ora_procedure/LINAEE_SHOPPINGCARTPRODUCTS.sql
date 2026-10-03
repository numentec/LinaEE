create or replace PROCEDURE     LINAEE_SHOPPINGCARTPRODUCTS
(
    PDEPTO IN VARCHAR2 DEFAULT '%',
    PCAT IN VARCHAR2 DEFAULT '0',
    PSCAT IN VARCHAR2 DEFAULT '0',
    PBRANDS IN VARCHAR2,
    PCIA IN VARCHAR2 DEFAULT '01',
    P_INSTOCK_OPERATOR IN VARCHAR2 DEFAULT NULL,
    P_INSTOCK_VALUE IN NUMBER DEFAULT NULL,
    P_INSTOCK_VALUE_TO IN NUMBER DEFAULT NULL,
    P_INTRANSIT_OPERATOR IN VARCHAR2 DEFAULT NULL,
    P_INTRANSIT_VALUE IN NUMBER DEFAULT NULL,
    P_INTRANSIT_VALUE_TO IN NUMBER DEFAULT NULL,
    P_INFUTURE_OPERATOR IN VARCHAR2 DEFAULT NULL,
    P_INFUTURE_VALUE IN NUMBER DEFAULT NULL,
    P_INFUTURE_VALUE_TO IN NUMBER DEFAULT NULL,
    P_COLOR IN VARCHAR2 DEFAULT NULL,
    P_ACABADO IN VARCHAR2 DEFAULT NULL,
    RESULTSET OUT SYS_REFCURSOR
) AS
    query_str VARCHAR2(8000);
    vPDEPTO VARCHAR2(100);
    is_PBRANDS NUMBER;

    v_instock_min_active NUMBER := 0;
    v_instock_min NUMBER;
    v_instock_max_active NUMBER := 0;
    v_instock_max NUMBER;
    v_instock_exclude_active NUMBER := 0;
    v_instock_exclude NUMBER;
    v_intransit_min_active NUMBER := 0;
    v_intransit_min NUMBER;
    v_intransit_max_active NUMBER := 0;
    v_intransit_max NUMBER;
    v_intransit_exclude_active NUMBER := 0;
    v_intransit_exclude NUMBER;
    v_infuture_min_active NUMBER := 0;
    v_infuture_min NUMBER;
    v_infuture_max_active NUMBER := 0;
    v_infuture_max NUMBER;
    v_infuture_exclude_active NUMBER := 0;
    v_infuture_exclude NUMBER;
    v_color_active NUMBER := 0;
    v_color_pattern VARCHAR2(200);
    v_acabado_active NUMBER := 0;
    v_acabado_pattern VARCHAR2(200);

    PROCEDURE normalize_filter(
        p_operator IN VARCHAR2,
        p_value IN NUMBER,
        p_value_to IN NUMBER,
        p_min_active OUT NUMBER,
        p_min OUT NUMBER,
        p_max_active OUT NUMBER,
        p_max OUT NUMBER,
        p_exclude_active OUT NUMBER,
        p_exclude OUT NUMBER
    ) IS
    BEGIN
        p_min_active := 0;
        p_min := NULL;
        p_max_active := 0;
        p_max := NULL;
        p_exclude_active := 0;
        p_exclude := NULL;

        IF p_operator IS NULL THEN
            IF p_value IS NOT NULL OR p_value_to IS NOT NULL THEN
                RAISE_APPLICATION_ERROR(-20001, 'Filter operator is required');
            END IF;
            RETURN;
        END IF;

        IF p_operator NOT IN ('eq', 'ne', 'gt', 'gte', 'lt', 'lte', 'between') THEN
            RAISE_APPLICATION_ERROR(-20002, 'Unsupported stock filter operator');
        END IF;

        IF p_value IS NULL OR p_value <> TRUNC(p_value) THEN
            RAISE_APPLICATION_ERROR(-20003, 'Stock filter values must be integers');
        END IF;

        IF p_operator = 'between' THEN
            IF p_value_to IS NULL OR p_value_to <> TRUNC(p_value_to)
               OR p_value > p_value_to THEN
                RAISE_APPLICATION_ERROR(-20004, 'Invalid stock filter range');
            END IF;
        ELSIF p_value_to IS NOT NULL THEN
            RAISE_APPLICATION_ERROR(-20005, 'Second value is only valid for between');
        END IF;

        IF p_operator = 'eq' THEN
            p_min_active := 1;
            p_min := p_value;
            p_max_active := 1;
            p_max := p_value;
        ELSIF p_operator = 'ne' THEN
            p_exclude_active := 1;
            p_exclude := p_value;
        ELSIF p_operator = 'gt' THEN
            p_min_active := 1;
            p_min := p_value + 1;
        ELSIF p_operator = 'gte' THEN
            p_min_active := 1;
            p_min := p_value;
        ELSIF p_operator = 'lt' THEN
            p_max_active := 1;
            p_max := p_value - 1;
        ELSIF p_operator = 'lte' THEN
            p_max_active := 1;
            p_max := p_value;
        ELSE
            p_min_active := 1;
            p_min := p_value;
            p_max_active := 1;
            p_max := p_value_to;
        END IF;
    END normalize_filter;

    -- Escapes LIKE wildcards so user text is matched literally.
    FUNCTION like_pattern(p_text IN VARCHAR2) RETURN VARCHAR2 IS
        v_text VARCHAR2(100) := TRIM(p_text);
    BEGIN
        IF v_text IS NULL THEN
            RETURN NULL;
        END IF;

        IF LENGTH(v_text) > 50 THEN
            RAISE_APPLICATION_ERROR(-20006, 'Text filter is too long');
        END IF;

        RETURN '%'
            || UPPER(REPLACE(REPLACE(REPLACE(v_text, '\', '\\'), '%', '\%'), '_', '\_'))
            || '%';
    END like_pattern;
BEGIN
    vPDEPTO := CASE WHEN PDEPTO = '0' THEN '%' ELSE PDEPTO END;
    is_PBRANDS := LENGTH(TRIM(PBRANDS));

    normalize_filter(
        P_INSTOCK_OPERATOR, P_INSTOCK_VALUE, P_INSTOCK_VALUE_TO,
        v_instock_min_active, v_instock_min,
        v_instock_max_active, v_instock_max,
        v_instock_exclude_active, v_instock_exclude
    );
    normalize_filter(
        P_INTRANSIT_OPERATOR, P_INTRANSIT_VALUE, P_INTRANSIT_VALUE_TO,
        v_intransit_min_active, v_intransit_min,
        v_intransit_max_active, v_intransit_max,
        v_intransit_exclude_active, v_intransit_exclude
    );
    normalize_filter(
        P_INFUTURE_OPERATOR, P_INFUTURE_VALUE, P_INFUTURE_VALUE_TO,
        v_infuture_min_active, v_infuture_min,
        v_infuture_max_active, v_infuture_max,
        v_infuture_exclude_active, v_infuture_exclude
    );

    v_color_pattern := like_pattern(P_COLOR);
    IF v_color_pattern IS NOT NULL THEN
        v_color_active := 1;
    END IF;

    v_acabado_pattern := like_pattern(P_ACABADO);
    IF v_acabado_pattern IS NOT NULL THEN
        v_acabado_active := 1;
    END IF;

    query_str :=
           'SELECT * FROM ( '
        || 'SELECT sku AS "id", '
        || '       NVL(sku, ''no_image'') || ''.jpg'' AS "image", '
        || '       descrip AS "name", '
        || '       precio AS "price", '
        || '       descrip_en AS "description", '
        || '       stock AS "stock", '
        || '       CASE '
        || '           WHEN instock < 0 THEN GREATEST(intransit_original + instock, 0) '
        || '           ELSE intransit_original '
        || '       END AS "intransit", '
        || '       CASE '
        || '           WHEN instock < 0 '
        || '           THEN infuture_original + LEAST(intransit_original + instock, 0) '
        || '           ELSE infuture_original '
        || '       END AS "infuture", '
        || '       store_reserved AS "store_reserved", '
        || '       store_reserved_future AS "store_reserved_future", '
        || '       instock AS "instock", '
        || '       co_marca AS "brand", '
        || '       colores AS "color", '
        || '       cla1 AS "acabado" '
        || 'FROM ( '
        || '    SELECT sku, descrip, precio, descrip_en, co_marca, colores, cla1, '
        || '           NVL(cant_fisica, 0) AS stock, '
        || '           NVL(cant_transito, 0) AS intransit_original, '
        || '           NVL(cant_transito_fut, 0) AS infuture_original, '
        || '           NVL(cant_comprometida, 0) AS store_reserved, '
        || '           NVL(cant_comprometida_fut, 0) AS store_reserved_future, '
        || '           NVL(cant_fisica, 0) '
        || '             - NVL(cant_comprometida, 0) '
        || '             - NVL(cant_comprometida_fut, 0) AS instock '
        || '    FROM DMC.LINAEE_CATALOGO_VW '
        || '    WHERE NVL(cant_fisica + cant_transito + cant_transito_fut, 0) > 0 '
        || '      AND bodega = ''BC1'' '
        || '      AND co_subcat LIKE :PDEPTO '
        || '      AND (:PCAT = ''0'' OR co_cat = TO_NUMBER(:PCAT)) '
        || '      AND (:PSCAT = ''0'' OR co_dep = TO_NUMBER(:PSCAT)) ';

    IF is_PBRANDS > 0 THEN
        query_str := query_str || ' AND co_marca IN (' || PBRANDS || ') ';
    END IF;

    query_str := query_str
        || ') ) '
        || 'WHERE (:COLOR_ACTIVE = 0 OR UPPER("color") LIKE :COLOR_PATTERN ESCAPE ''\'') '
        || '  AND (:ACABADO_ACTIVE = 0 OR UPPER("acabado") LIKE :ACABADO_PATTERN ESCAPE ''\'') '
        || '  AND (:NOW_MIN_ACTIVE = 0 OR "instock" >= :NOW_MIN) '
        || '  AND (:NOW_MAX_ACTIVE = 0 OR "instock" <= :NOW_MAX) '
        || '  AND (:NOW_EXCLUDE_ACTIVE = 0 OR "instock" <> :NOW_EXCLUDE) '
        || '  AND (:TRAN_MIN_ACTIVE = 0 OR "intransit" >= :TRAN_MIN) '
        || '  AND (:TRAN_MAX_ACTIVE = 0 OR "intransit" <= :TRAN_MAX) '
        || '  AND (:TRAN_EXCLUDE_ACTIVE = 0 OR "intransit" <> :TRAN_EXCLUDE) '
        || '  AND (:FUT_MIN_ACTIVE = 0 OR "infuture" >= :FUT_MIN) '
        || '  AND (:FUT_MAX_ACTIVE = 0 OR "infuture" <= :FUT_MAX) '
        || '  AND (:FUT_EXCLUDE_ACTIVE = 0 OR "infuture" <> :FUT_EXCLUDE) '
        || 'ORDER BY "id" DESC';

    OPEN RESULTSET FOR query_str
        USING vPDEPTO, PCAT, PCAT, PSCAT, PSCAT,
              v_color_active, v_color_pattern,
              v_acabado_active, v_acabado_pattern,
              v_instock_min_active, v_instock_min,
              v_instock_max_active, v_instock_max,
              v_instock_exclude_active, v_instock_exclude,
              v_intransit_min_active, v_intransit_min,
              v_intransit_max_active, v_intransit_max,
              v_intransit_exclude_active, v_intransit_exclude,
              v_infuture_min_active, v_infuture_min,
              v_infuture_max_active, v_infuture_max,
              v_infuture_exclude_active, v_infuture_exclude;
END LINAEE_SHOPPINGCARTPRODUCTS;