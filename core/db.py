import duckdb

from core.config import cfg
from core.logging import logger

is_local: bool = cfg.db_is_local


def r2_url() -> str:
    return f"r2://{cfg.r2_bucket_name}/"


def ddb_connection() -> duckdb.DuckDBPyConnection:
    conn = duckdb.connect()
    if not is_local:
        conn.execute("INSTALL AND LOAD httpfs;")
        conn.execute(
            f"""
            CREATE SECRET (
                TYPE r2,
                KEY_ID '{cfg.r2_key_id}',
                SECRET '{cfg.r2_secret}',
                ACCOUNT_ID '{cfg.r2_accound_id}'
                );
            """
        )
        try:
            conn.sql(f"SELECT * FROM glob('{r2_url}*');")
        except (duckdb.HTTPException, duckdb.IOException) as e:
            print(e)
            conn.close()

    return conn
