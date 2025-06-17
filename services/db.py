import os
import oracledb
from dotenv import load_dotenv

load_dotenv()

oracledb.init_oracle_client(lib_dir=os.getenv("ORACLE_CLIENT_LIB"))

def get_oracle_connection():
    dsn = oracledb.makedsn(
        os.getenv("ORACLE_HOST"),
        int(os.getenv("ORACLE_PORT")),
        sid=os.getenv("ORACLE_SID")
    )
    conn = oracledb.connect(
        user=os.getenv("ORACLE_USER"),
        password=os.getenv("ORACLE_PASSWORD"),
        dsn=dsn
    )
    return conn


def get_all_weights():
    conn = get_oracle_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT NAME, WEIGHT FROM ART_AVG_WEIGHTS')
        rows = cursor.fetchall()
        return {name: weight for name, weight in rows}
    finally:
        cursor.close()
        conn.close()

def insert_art_avg_weight(name, weight):
    insert_sql = """
        INSERT INTO ART_AVG_WEIGHTS (ID, NAME, WEIGHT)
        VALUES (art_avg_weights_seq.NEXTVAL, :name, :weight)
    """
    conn = get_oracle_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(insert_sql, {"name": name, "weight": weight})
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def art_select(max_rows):
    sql = """
        SELECT ID, NAME, NET_WEIGHT
        FROM (
            SELECT ID, NAME, NET_WEIGHT
            FROM ART
            WHERE CLIENT_ID IN (497, 407, 501)
              AND NAME IS NOT NULL
              AND NET_WEIGHT = 200
              AND LOWER(NAME) NOT LIKE '%mix%'
        )
        WHERE ROWNUM <= :max_rows
    """
    conn = get_oracle_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, {"max_rows": max_rows})
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def art_update(id, weight):
    sql = """
        UPDATE ART
        SET NET_WEIGHT = :weight,
            GROSS_WEIGHT = :weight
        WHERE ID = :id
    """
    conn = get_oracle_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, {"id": id, "weight": weight})
        conn.commit()
    finally:
        cursor.close()
        conn.close()