import os
from typing import Literal

import duckdb
from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self) -> None:
        self.db_backend: str | None = os.getenv("DB_BACKEND", "local")
        self.simulation_backend: str | None = os.getenv("SIMULATION_BACKEND", "local")

        print(self.db_backend)

    @staticmethod
    def is_local(backend: Literal["local", "cloud"]) -> bool:
        return backend == "local"

    def duckdb_conn(self) -> duckdb.DuckDBPyConnection:
        conn = duckdb.connect()
        conn.execute("INSTALL AND LOAD httpfs")

        return conn


Settings()
