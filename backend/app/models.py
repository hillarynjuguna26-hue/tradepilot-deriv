from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func

from app.db import Base


class StrategyConfig(Base):
    __tablename__ = "strategy_configs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    symbol = Column(String, index=True)
    timeframe = Column(String, default="15m")
    enabled = Column(Boolean, default=True)
    risk_per_trade = Column(Float, default=0.01)
    max_positions = Column(Integer, default=5)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SignalLog(Base):
    __tablename__ = "signal_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    symbol = Column(String)
    action = Column(String)
    confidence = Column(Float)
    pivot_level = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TradeOrder(Base):
    __tablename__ = "trade_orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    symbol = Column(String)
    action = Column(String)
    contract_type = Column(String, default="CALL")
    stake = Column(Float)
    price = Column(Float)
    status = Column(String, default="PENDING")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
