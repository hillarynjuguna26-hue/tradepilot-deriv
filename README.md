# TradePilot Deriv

A mobile-first trading automation system for Deriv featuring a LuxAlgo-inspired pivot-point strategy on the 15-minute timeframe. Supports all forex pairs and synthetic instruments available on your Deriv account.

**Status**: Demo-first architecture. Test thoroughly on a demo account before any live trading.

## Architecture

```
Mobile App (Flutter)
    ↓ HTTP API
Backend (FastAPI)
    ↓ WebSocket
Deriv Broker (Demo/Live)
    ↓ Market Data
Strategy Engine (15m Pivots)
    ↓ Risk Manager
Order Execution (Demo Only)
    ↓ Database (PostgreSQL)
Trade Logging
```

## Key Features

- **15-Minute Pivot Strategy**: LuxAlgo-inspired support/resistance levels
- **Multi-Asset Support**: Forex pairs and synthetic indices
- **Demo-First**: Connect to Deriv demo account; verify before live
- **Risk Management**: Max risk per trade, daily loss limits, max positions
- **Mobile Dashboard**: Real-time signal display and strategy control
- **Automated Scanning**: Continuous market monitoring on 15m candles
- **Trade Logging**: All signals and orders persisted to database

## Requirements

- Python 3.9+
- Flutter 3.2+
- Docker and Docker Compose
- Deriv demo account with app credentials

## Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/hillarynjuguna26-hue/tradepilot-deriv.git
cd tradepilot-deriv
```

### 2. Set up environment

Create `backend/.env`:

```bash
cat > backend/.env << EOF
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/tradepilot
DERIV_APP_ID=YOUR_DEMO_APP_ID
DERIV_TOKEN=YOUR_DEMO_TOKEN
JWT_SECRET=change-this-secret
EOF
```

**Get your Deriv credentials:**
1. Create a Deriv account (or use existing demo)
2. Go to Settings > API Tokens
3. Create a new token with "Trade" and "Read" scopes
4. Copy the app ID from your app settings
5. Paste both into the `.env` file

### 3. Start PostgreSQL database

```bash
cd docker
docker compose up -d
cd ..
```

Verify:
```bash
psql postgresql://postgres:postgres@localhost:5432/tradepilot -c "SELECT version();"
```

### 4. Set up backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Run backend server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 6. Test the API

Open http://localhost:8000/docs in your browser.

Test endpoints:
- GET `/api/health` → returns `{"status": "ok"}`
- GET `/api/symbols` → returns list of supported instruments
- POST `/api/deriv-connect` → connects to Deriv broker
- POST `/api/demo-scan` → returns BUY/SELL/HOLD for a symbol

### 7. Set up mobile app

```bash
cd mobile
flutter pub get
```

### 8. Run mobile app

**Android Emulator:**
```bash
flutter run
```

**iOS Simulator:**
```bash
flutter run -d ios
```

**Physical device:**
```bash
flutter run -d <device-id>
```

## API Endpoints

### Health & Status

```bash
# Check backend is running
curl http://localhost:8000/api/health

# Get supported symbols
curl http://localhost:8000/api/symbols
```

### Deriv Connection

```bash
# Connect to Deriv demo
curl -X POST http://localhost:8000/api/deriv-connect

# Disconnect
curl -X POST http://localhost:8000/api/deriv-disconnect
```

### Strategy Control

```bash
# Start scanning all symbols
curl -X POST http://localhost:8000/api/start-scheduler

# Stop scanning
curl -X POST http://localhost:8000/api/stop-scheduler

# Scan a specific symbol (demo data)
curl -X POST http://localhost:8000/api/demo-scan \
  -H "Content-Type: application/json" \
  -d '{"symbol": "frxEURUSD"}'
```

### View Results

```bash
# Get all signals
curl http://localhost:8000/api/signals

# Get all trade orders
curl http://localhost:8000/api/orders

# Get strategies
curl http://localhost:8000/api/strategies
```

## Strategy Logic

### 15-Minute Pivot Points

The strategy evaluates support/resistance levels based on the last 20 candles:

- **Pivot (P)**: (High + Low) / 2
- **Resistance 1 (R1)**: (P × 2) - Min(Low)
- **Support 1 (S1)**: (P × 2) - Max(High)
- **R2**: P + (R1 - S1)
- **S2**: P - (R1 - S1)

### Trade Rules

1. **BUY signal** when price closes above R1 (confidence: 82%)
2. **SELL signal** when price closes below S1 (confidence: 82%)
3. **HOLD** otherwise (confidence: 20-35%)

### Risk Controls

Before any trade is placed:
- ✅ Account balance check
- ✅ Risk per trade ≤ 1% of account
- ✅ Open positions < max (default: 5)
- ✅ Daily loss < 5% of account balance

## Mobile App Flow

1. **Home Screen**: Shows balance, P&L, open positions
2. **Connect Button**: Initiates Deriv WebSocket connection
3. **Symbol Dropdown**: Select forex pair or synthetic to scan
4. **Scan Button**: Manually trigger scan (shows demo data)
5. **Start Button**: Begin automated 15-minute scanning
6. **Stop Button**: Halt the scheduler
7. **Status Panel**: Shows latest action (BUY/SELL/HOLD) and confidence

## Database

PostgreSQL tables created automatically on startup:

```sql
strategy_configs  -- Strategy rules (symbol, timeframe, risk)
signal_logs       -- All generated signals (action, confidence, pivot level)
trade_orders      -- All placed orders (symbol, action, stake, status)
```

## Troubleshooting

### Backend won't start

```bash
# Check Python version
python --version  # Should be 3.9+

# Verify dependencies
pip list | grep fastapi

# Check port 8000 is free
lsof -i :8000  # Kill if needed: kill -9 <PID>
```

### Database connection failed

```bash
# Check Postgres is running
docker ps | grep postgres

# Restart if needed
cd docker && docker compose restart && cd ..

# Test connection
psql postgresql://postgres:postgres@localhost:5432/tradepilot
```

### App can't reach backend

```bash
# Android emulator uses special host
http://10.0.2.2:8000/api  # NOT localhost:8000

# Check backend is accessible
curl http://localhost:8000/api/health
```

### Deriv connection fails

```bash
# Verify credentials in .env
cat backend/.env | grep DERIV

# Check API docs for connection status
# POST /api/deriv-connect should return {"status": "connected"}

# Check WebSocket connectivity
# Look for logs: "Deriv WebSocket connected"
```

## Development

### Backend structure

```
backend/
  app/
    main.py                 # FastAPI entry point
    config.py              # Environment settings
    db.py                  # SQLAlchemy setup
    models.py              # Database models
    api/
      routes.py            # API endpoints
    services/
      deriv_demo_connector.py   # Broker connection
      pivot_strategy.py         # 15m signal logic
      trading_scheduler.py      # Continuous scan loop
      risk_manager.py           # Position/loss limits
      symbol_catalog.py         # Supported instruments
  requirements.txt         # Python dependencies
```

### Mobile structure

```
mobile/
  lib/
    main.dart              # App entry, dashboard UI
    services/
      api_service.dart     # HTTP client to backend
  pubspec.yaml             # Flutter dependencies
```

### Adding a new symbol

1. Add to `backend/app/services/symbol_catalog.py`
2. Backend will auto-subscribe on next connect
3. Scheduler will scan it on next loop

### Testing a strategy change

1. Edit `backend/app/services/pivot_strategy.py`
2. Backend reloads automatically (--reload flag)
3. Next scan will use new logic

## Safety & Best Practices

### Never do this

❌ Use a live token until strategy is validated  
❌ Trade without proper risk limits  
❌ Ignore daily loss caps  
❌ Open unlimited positions  
❌ Skip the demo testing phase  

### Always do this

✅ Start with demo account  
✅ Verify symbol names in your account  
✅ Set conservative risk (0.5-1%)  
✅ Set daily loss cap (2-5%)  
✅ Limit max positions (3-5)  
✅ Monitor first 10 trades manually  
✅ Use logs to audit every trade  
✅ Test strategy changes on demo first  

## Deployment

### Local (development)

```bash
# Terminal 1: Database
cd docker && docker compose up -d

# Terminal 2: Backend
cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 3: Mobile app
cd mobile && flutter run
```

### Docker (production)

```bash
# Build backend image
docker build -t tradepilot-backend:latest backend/

# Run with compose
docker compose -f docker/docker-compose.yml up -d
```

### Cloud VPS (recommended for live)

1. Deploy backend to AWS/Digital Ocean/Heroku
2. Run scheduler continuously
3. Mobile app connects via public API endpoint
4. Database persists trade history

## Monitoring

### View logs

```bash
# Backend logs (in uvicorn terminal)
INFO:     Deriv WebSocket connected
INFO:     Scheduler started for 25 symbols
INFO:     Trade placed: frxEURUSD BUY risk=100

# Mobile logs
flutter run -v
```

### Database queries

```bash
# Recent signals
psql postgresql://postgres:postgres@localhost:5432/tradepilot -c \
  "SELECT * FROM signal_logs ORDER BY created_at DESC LIMIT 10;"

# Recent trades
psql postgresql://postgres:postgres@localhost:5432/tradepilot -c \
  "SELECT * FROM trade_orders ORDER BY created_at DESC LIMIT 10;"
```

## Key Files to Understand

1. **backend/app/services/deriv_demo_connector.py**
   - WebSocket connection to Deriv
   - Subscribe to candles
   - Place orders

2. **backend/app/services/pivot_strategy.py**
   - Calculate pivot levels
   - Generate BUY/SELL/HOLD signals

3. **backend/app/services/trading_scheduler.py**
   - Continuous market scan loop
   - Risk validation before trade
   - Order execution

4. **mobile/lib/main.dart**
   - Connect/disconnect UI
   - Start/stop scheduler UI
   - Display latest signal

## Next Steps

1. ✅ Clone repo and run backend locally
2. ✅ Test /api/health and /api/symbols
3. ✅ Connect Deriv demo account
4. ✅ Run mobile app and verify connection
5. ✅ Test demo-scan with different symbols
6. ✅ Start scheduler and monitor signals
7. ⏳ Validate strategy on demo data for 1-2 weeks
8. ⏳ Lower risk limits and test live (after validation)

## Support

Issues or questions?

1. Check logs: `uvicorn` terminal and `flutter run -v`
2. Verify .env file has correct Deriv credentials
3. Test API directly: http://localhost:8000/docs
4. Check database: `psql postgresql://postgres:postgres@localhost:5432/tradepilot`

## License

MIT

## Disclaimer

This is a demo trading application. Trading carries risk. Use only with money you can afford to lose. Test thoroughly on a demo account before any live trading. The authors are not responsible for trading losses.
