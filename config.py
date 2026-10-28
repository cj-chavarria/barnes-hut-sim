import os
from dataclasses import dataclass

import duckdb
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    db_backend: str = os.getenv("DB_BACKEND", "local")
    simulation_backend: str = os.getenv("SIMULATION_BACKEND", "local")

    bucket_name: str | None = os.getenv("R2_BUCKET_NAME")
    key_id: str | None = os.getenv("R2_ACCESS_KEY_ID")
    accound_id: str | None = os.getenv("R2_ACCOUNT_ID")
    secret: str | None = os.getenv("R2_SECRET_ACCESS_KEY")

    def __post__init(self) -> None:
        if self.db_backend or self.simulation_backend not in ("local", "cloud"):
            raise ValueError

    @property
    def db_conn(self) -> duckdb.DuckDBPyConnection:
        conn = duckdb.connect()
        if self.db_backend == "cloud":
            conn.execute(
                f"""
                CREATE SECRET (
                    TYPE r2,
                    KEY_ID '{self.key_id}',
                    SECRET '{self.secret}',
                    ACCOUNT_ID '{self.accound_id}'
                    );
                """
            )
            try:
                conn.sql(f"SELECT * FROM glob('r2://{self.bucket_name}/*')")
            except duckdb.HTTPException, duckdb.IOException:
                conn.close()
                return duckdb.connect()

        return conn


cfg = Config()

ddb_conn = cfg.db_conn
