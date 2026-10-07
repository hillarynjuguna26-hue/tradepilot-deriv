import json
import threading
import time

import websocket


class DerivClient:
    """
    Minimal Deriv WebSocket client. Use it with a demo account first.
    You must verify exact symbol names and contract types in your broker account.
    """

    def __init__(self, app_id: str, token: str):
        self.app_id = app_id
        self.token = token
        self.ws = None
        self.connected = False
        self._handlers = []

    def register_handler(self, handler):
        self._handlers.append(handler)

    def _on_message(self, ws, message):
        try:
            payload = json.loads(message)
        except json.JSONDecodeError:
            return
        for handler in self._handlers:
            handler(payload)

    def _on_open(self, ws):
        self.connected = True
        print("Deriv WebSocket connected")

    def connect(self):
        if not self.app_id:
            raise ValueError("DERIV_APP_ID is required")
        if not self.token:
            raise ValueError("DERIV_TOKEN is required")

        url = f"wss://ws.deriv.com/websockets/v3?app_id={self.app_id}"
        self.ws = websocket.WebSocketApp(
            url=url,
            on_open=self._on_open,
            on_message=self._on_message,
        )
        thread = threading.Thread(target=self.ws.run_forever, daemon=True)
        thread.start()
        time.sleep(1)
        return self

    def authorize(self):
        if self.ws is None:
            raise RuntimeError("WebSocket not connected")
        self.ws.send(json.dumps({"authorize": self.token}))

    def get_symbols(self):
        return [
            "frxEURUSD",
            "frxGBPUSD",
            "frxUSDJPY",
            "frxAUDUSD",
            "frxUSDCAD",
            "frxNZDUSD",
            "frxEURJPY",
            "frxGBPJPY",
            "frxEURCHF",
            "frxAUDJPY",
            "frxUSDCHF",
            "frxEURGBP",
            "frxGBPCHF",
            "frxEURAUD",
            "R_50",
            "R_100",
            "R_200",
            "1HZ10V",
            "1HZ50V",
            "1HZ100V",
            "B_10",
            "B_25",
            "B_50",
            "B_75",
            "B_100",
        ]

    def subscribe_ticks(self, symbol: str):
        if self.ws is not None:
            self.ws.send(json.dumps({"ticks": symbol, "subscribe": 1}))

    def subscribe_candles(self, symbol: str, timeframe: str):
        granularity = self._to_granularity(timeframe)
        if self.ws is not None:
            self.ws.send(
                json.dumps(
                    {
                        "ticks_history": symbol,
                        "style": "candles",
                        "granularity": granularity,
                        "count": 200,
                    }
                )
            )

    @staticmethod
    def _to_granularity(timeframe: str) -> int:
        mapping = {
            "1m": 60,
            "5m": 300,
            "15m": 900,
            "1h": 3600,
            "4h": 14400,
            "1d": 86400,
        }
        return mapping.get(timeframe, 900)

    def buy(self, symbol: str, stake: float, contract_type: str = "CALL"):
        if self.ws is None:
            raise RuntimeError("WebSocket not connected")
        payload = {
            "buy": 1,
            "price": float(stake),
            "parameters": {"symbol": symbol, "contract_type": contract_type},
        }
        self.ws.send(json.dumps(payload))
        return {"status": "sent", "symbol": symbol, "stake": stake, "contract_type": contract_type}

    def sell(self, symbol: str, stake: float, contract_type: str = "PUT"):
        if self.ws is None:
            raise RuntimeError("WebSocket not connected")
        payload = {
            "buy": 1,
            "price": float(stake),
            "parameters": {"symbol": symbol, "contract_type": contract_type},
        }
        self.ws.send(json.dumps(payload))
        return {"status": "sent", "symbol": symbol, "stake": stake, "contract_type": contract_type}
