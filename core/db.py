import duckdb

from core.config import cfg
from core.logging import logger

is_local: bool = cfg.db_is_local
r2_url = f"r2://{cfg.r2_bucket_name}/"


def db_connection() -> duckdb.DuckDBPyConnection:
    logger.debug("Start a DuckDB connection ")
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
            logger.debug("Test connection to R2")
            conn.sql(f"SELECT * FROM glob('{r2_url}*');")
        except duckdb.HTTPException, duckdb.IOException:
            logger.error("The connection to R2 failed.")
            conn.close()
            raise

    return conn


def db_path(s: str) -> str:
    return r2_url + s if not is_local else s
