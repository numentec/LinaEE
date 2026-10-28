"""Compara el esquema de la BD de la aplicación contra una BD de referencia.

La BD de referencia se crea vacía y se le aplican las migraciones del repositorio
(ver check_schema.sh), de modo que representa el esquema que esperan los modelos.

Uso (dentro del contenedor linabe):
    REF_DB_HOST=linadb_ref REF_DB_PW=... python scripts/db/schema_diff.py

Termina con código 1 si encuentra diferencias.
"""
import os
import sys

import MySQLdb


def connect(host, port, user, pw, name):
    conn = MySQLdb.connect(host=host, port=int(port), user=user, passwd=pw, db=name, charset="utf8mb4")
    return conn, name


def q(db, sql):
    conn, name = db
    c = conn.cursor()
    c.execute(sql, (name,))
    return c.fetchall()


def snapshot(db):
    tables = {r[0]: (r[1], r[2]) for r in q(db, "select table_name, engine, table_collation from information_schema.tables where table_schema=%s and table_type='BASE TABLE'")}
    cols = {}
    for t, c, ct, nul, extra, coll in q(db, "select table_name, column_name, column_type, is_nullable, extra, collation_name from information_schema.columns where table_schema=%s"):
        cols.setdefault(t, {})[c] = (ct, nul, extra, coll)
    idx = {}
    for t, name, nonuniq, cols_ in q(db, "select table_name, index_name, non_unique, group_concat(column_name order by seq_in_index) from information_schema.statistics where table_schema=%s group by table_name, index_name, non_unique"):
        idx.setdefault(t, set()).add(("UNIQUE" if not nonuniq else "INDEX", cols_, "PK" if name == "PRIMARY" else ""))
    fks = {}
    for t, c, rt, rc in q(db, "select table_name, column_name, referenced_table_name, referenced_column_name from information_schema.key_column_usage where table_schema=%s and referenced_table_name is not null"):
        fks.setdefault(t, set()).add((c, rt, rc))
    checks = {}
    for t, clause in q(db, "select table_name, check_clause from information_schema.check_constraints where constraint_schema=%s"):
        checks.setdefault(t, set()).add(clause)
    migrations = {r for r in q(db, "select app, name from django_migrations where %s is not null")}
    return tables, cols, idx, fks, migrations, checks


def diff(R, F):
    out = []
    rt, ft = set(R[0]), set(F[0])
    for t in sorted(rt - ft):
        out.append(f"tabla sin modelo en BD real: {t}")
    for t in sorted(ft - rt):
        out.append(f"tabla FALTANTE en BD real: {t}")
    for t in sorted(rt & ft):
        rc, fc = R[1].get(t, {}), F[1].get(t, {})
        for c in sorted(set(rc) - set(fc)):
            out.append(f"{t}: columna sobrante {c} {rc[c]}")
        for c in sorted(set(fc) - set(rc)):
            out.append(f"{t}: columna FALTANTE {c} {fc[c]}")
        for c in sorted(set(rc) & set(fc)):
            if rc[c] != fc[c]:
                out.append(f"{t}.{c}: real={rc[c]} esperado={fc[c]}")
        for i in sorted(R[2].get(t, set()) - F[2].get(t, set())):
            out.append(f"{t}: índice sobrante {i}")
        for i in sorted(F[2].get(t, set()) - R[2].get(t, set())):
            out.append(f"{t}: índice FALTANTE {i}")
        for k in sorted(R[3].get(t, set()) - F[3].get(t, set())):
            out.append(f"{t}: FK sobrante {k}")
        for k in sorted(F[3].get(t, set()) - R[3].get(t, set())):
            out.append(f"{t}: FK FALTANTE {k}")
        for k in sorted(R[5].get(t, set()) - F[5].get(t, set())):
            out.append(f"{t}: CHECK sobrante {k}")
        for k in sorted(F[5].get(t, set()) - R[5].get(t, set())):
            out.append(f"{t}: CHECK FALTANTE {k}")
        if R[0][t] != F[0][t]:
            out.append(f"{t}: engine/collation real={R[0][t]} esperado={F[0][t]}")
    for m in sorted(R[4] - F[4]):
        out.append(f"django_migrations: registro sin archivo de migración {m}")
    for m in sorted(F[4] - R[4]):
        out.append(f"django_migrations: migración NO registrada {m}")
    return out


def main():
    e = os.environ
    real = connect(e["DB_HOST"], e["DB_PORT"], e["DB_USER"], e["DB_USER_PW"], e["DB_NAME"])
    ref = connect(e.get("REF_DB_HOST", "linadb_ref"), e.get("REF_DB_PORT", 3306), e.get("REF_DB_USER", "root"),
                  e["REF_DB_PW"], e.get("REF_DB_NAME", "linaee_ref"))
    out = diff(snapshot(real), snapshot(ref))
    if out:
        print("\n".join(out))
        print(f"\n{len(out)} diferencia(s) encontradas.")
        sys.exit(1)
    print("Esquema coherente: sin diferencias contra la BD de referencia.")


if __name__ == "__main__":
    main()
