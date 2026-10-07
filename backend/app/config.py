import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "TradePilot Deriv"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/tradepilot")
    DERIV_APP_ID: str = os.getenv("DERIV_APP_ID", "")
    DERIV_TOKEN: str = os.getenv("DERIV_TOKEN", "")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "change-this-secret")
    DEFAULT_RISK_PER_TRADE: float = 0.01
    MAX_DAILY_LOSS: float = 0.05
    DEFAULT_TIMEFRAME: str = "15m"
    MAX_OPEN_POSITIONS: int = 5

    class Config:
        env_file = ".env"


settings = Settings()
