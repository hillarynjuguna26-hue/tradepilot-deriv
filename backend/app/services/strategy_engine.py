from typing import Any, Dict, List

from app.services.pivot_strategy import evaluate_signal
from app.services.risk_manager import RiskManager


class StrategyEngine:
    def __init__(self, risk_manager: RiskManager):
        self.risk_manager = risk_manager

    def scan_symbol(self, symbol: str, candles: List[Dict[str, Any]]) -> Dict[str, Any]:
        signal, confidence, levels = evaluate_signal(candles, symbol)

        account_balance = 10000.0
        open_positions = 2
        daily_loss = 250.0

        allowed, risk_value = self.risk_manager.allowed_trade(account_balance, open_positions, daily_loss)

        if signal == "HOLD":
            return {
                "symbol": symbol,
                "signal": signal,
                "confidence": confidence,
                "levels": levels,
                "allowed": False,
                "reason": "No trade triggered",
            }

        return {
            "symbol": symbol,
            "signal": signal,
            "confidence": confidence,
            "levels": levels,
            "allowed": allowed,
            "risk_value": risk_value,
        }
