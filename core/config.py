import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    db_backend: str = os.getenv("DB_BACKEND", "local")
    simulation_backend: str = os.getenv("SIMULATION_BACKEND", "local")

    r2_bucket_name: str | None = os.getenv("R2_BUCKET_NAME")
    r2_key_id: str | None = os.getenv("R2_ACCESS_KEY_ID")
    r2_accound_id: str | None = os.getenv("R2_ACCOUNT_ID")
    r2_secret: str | None = os.getenv("R2_SECRET_ACCESS_KEY")

    def __post__init__(self) -> None:
        if (self.db_backend or self.simulation_backend not in ("local", "cloud")) or (
            None
            in (
                self.r2_bucket_name,
                self.r2_key_id,
                self.r2_accound_id,
                self.r2_accound_id,
            )
        ):
            raise ValueError

    @property
    def db_is_local(self) -> bool:
        return self.db_backend == "local"


cfg = Config()
