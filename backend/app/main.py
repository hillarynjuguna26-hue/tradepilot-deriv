from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import StrategyConfig, SignalLog
from app.services.symbol_catalog import get_symbol_catalog

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/symbols")
def get_symbols():
    return {"symbols": get_symbol_catalog()}


@router.get("/strategies")
def get_strategies(db: Session = Depends(get_db)):
    strategies = db.query(StrategyConfig).all()
    return {"strategies": strategies}


@router.post("/strategies")
def create_strategy(payload: dict, db: Session = Depends(get_db)):
    strategy = StrategyConfig(
        user_id="demo-user",
        symbol=payload.get("symbol", "frxEURUSD"),
        timeframe=payload.get("timeframe", "15m"),
        enabled=payload.get("enabled", True),
        risk_per_trade=payload.get("risk_per_trade", 0.01),
        max_positions=payload.get("max_positions", 5),
    )
    db.add(strategy)
    db.commit()
    db.refresh(strategy)
    return {"message": "Strategy created", "strategy": strategy.id}


@router.post("/signals")
def add_signal(payload: dict, db: Session = Depends(get_db)):
    signal = SignalLog(
        user_id="demo-user",
        symbol=payload.get("symbol", "frxEURUSD"),
        action=payload.get("action", "HOLD"),
        confidence=payload.get("confidence", 0.0),
        pivot_level=payload.get("pivot_level", 0.0),
    )
    db.add(signal)
    db.commit()
    db.refresh(signal)
    return {"message": "Signal saved", "signal": signal.id}


@router.get("/scan")
def scan_market():
    sample_candles = [
        {"high": 1.0838, "low": 1.0822, "close": 1.0830},
        {"high": 1.0842, "low": 1.0828, "close": 1.0835},
        {"high": 1.0848, "low": 1.0831, "close": 1.0840},
        {"high": 1.0850, "low": 1.0836, "close": 1.0845},
        {"high": 1.0854, "low": 1.0838, "close": 1.0849},
        {"high": 1.0860, "low": 1.0842, "close": 1.0850},
        {"high": 1.0865, "low": 1.0845, "close": 1.0856},
        {"high": 1.0870, "low": 1.0847, "close": 1.0859},
        {"high": 1.0875, "low": 1.0851, "close": 1.0862},
        {"high": 1.0878, "low": 1.0854, "close": 1.0865},
        {"high": 1.0881, "low": 1.0858, "close": 1.0868},
        {"high": 1.0886, "low": 1.0860, "close": 1.0871},
        {"high": 1.0888, "low": 1.0863, "close": 1.0874},
        {"high": 1.0890, "low": 1.0867, "close": 1.0878},
        {"high": 1.0895, "low": 1.0870, "close": 1.0883},
        {"high": 1.0898, "low": 1.0874, "close": 1.0886},
        {"high": 1.0905, "low": 1.0880, "close": 1.0890},
        {"high": 1.0908, "low": 1.0884, "close": 1.0893},
        {"high": 1.0912, "low": 1.0886, "close": 1.0898},
        {"high": 1.0915, "low": 1.0888, "close": 1.0901},
    ]

    from app.services.pivot_strategy import evaluate_signal
    action, confidence, levels = evaluate_signal(sample_candles, "frxEURUSD")
    return {"symbol": "frxEURUSD", "action": action, "confidence": confidence, "levels": levels}
