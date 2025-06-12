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
