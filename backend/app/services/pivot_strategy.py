from typing import Any, Dict, List, Tuple


def pivot_levels(candles: List[Dict[str, float]]) -> Dict[str, float | None]:
    """Simple LuxAlgo-inspired pivot calculation on a 15-minute view."""
    if len(candles) < 20:
        return {"pivot": None, "r1": None, "s1": None, "r2": None, "s2": None}

    recent_highs = [float(c["high"]) for c in candles[-20:]]
    recent_lows = [float(c["low"]) for c in candles[-20:]]

    pivot = (max(recent_highs) + min(recent_lows)) / 2
    r1 = (pivot * 2) - min(recent_lows)
    s1 = (pivot * 2) - max(recent_highs)
    r2 = pivot + (r1 - s1)
    s2 = pivot - (r1 - s1)

    return {"pivot": pivot, "r1": r1, "s1": s1, "r2": r2, "s2": s2}


def evaluate_signal(candles: List[Dict[str, float]], symbol: str) -> Tuple[str, float, Dict[str, float | None]]:
    levels = pivot_levels(candles)
    if levels["pivot"] is None:
        return "HOLD", 0.0, levels

    last_close = float(candles[-1]["close"])
    pivot = float(levels["pivot"])
    r1 = float(levels["r1"])
    s1 = float(levels["s1"])

    if last_close > r1:
        return "BUY", 0.82, levels
    if last_close < s1:
        return "SELL", 0.82, levels
    if abs(last_close - pivot) < 0.0005:
        return "HOLD", 0.35, levels

    return "HOLD", 0.20, levels


def get_pivot_summary(candles: List[Dict[str, float]], symbol: str) -> Dict[str, Any]:
    signal, confidence, levels = evaluate_signal(candles, symbol)
    return {"symbol": symbol, "signal": signal, "confidence": confidence, "levels": levels}
