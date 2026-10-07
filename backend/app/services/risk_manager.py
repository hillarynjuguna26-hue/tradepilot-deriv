from app.services.symbol_catalog import get_symbol_catalog


class RiskManager:
    def __init__(self, max_risk_per_trade: float = 0.01, max_daily_loss: float = 0.05, max_positions: int = 5):
        self.max_risk_per_trade = max_risk_per_trade
        self.max_daily_loss = max_daily_loss
        self.max_positions = max_positions

    def allowed_trade(self, account_balance: float, open_positions: int, daily_loss: float):
        if open_positions >= self.max_positions:
            return False, "max_positions_reached"

        if daily_loss >= account_balance * self.max_daily_loss:
            return False, "daily_loss_limit"

        risk_amount = account_balance * self.max_risk_per_trade
        return True, risk_amount


def get_supported_symbols():
    return get_symbol_catalog()
