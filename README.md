# TradePilot Deriv

A mobile-friendly trading automation starter for Deriv featuring LuxAlgo-inspired pivot analysis on the 15-minute timeframe.

Features
- Deriv WebSocket integration for market data and order execution
- Dynamic symbol catalog covering forex pairs and synthetic markets
- LuxAlgo-inspired pivot-point strategy on the 15m timeframe
- Risk controls and orders management
- FastAPI backend
- Flutter mobile dashboard
- Docker-based local setup

Architecture
- Mobile app: Flutter dashboard and controls
- Backend API: Python + FastAPI
- Database: PostgreSQL
- Execution layer: Deriv broker WebSocket API
- Strategy: pivot breakout/reversal logic on 15m candles

Quick start

1. Create environment file:
   cp docker/.env.example docker/.env

2. Start PostgreSQL:
   docker compose -f docker/docker-compose.yml up -d

3. Install backend deps:
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

4. Run backend:
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

5. Run mobile app:
   cd mobile
   flutter pub get
   flutter run

Important
- Do not trade live without proper broker credentials and strict risk validation.
- Use a demo or test account first.
- MT5 is not involved here because this project targets Deriv.
- Deriv symbol naming can differ by account type and region; verify exact names in your own account before live use.

Required environment variables
- DERIV_APP_ID
- DERIV_TOKEN
- DATABASE_URL

Files
- backend/app/services/pivot_strategy.py: LuxAlgo-style pivot logic
- backend/app/services/deriv_client.py: live Deriv broker interaction
- backend/app/services/strategy_engine.py: trade scanning engine
- backend/app/services/symbol_catalog.py: forex + synthetic instrument catalog
- mobile/lib/main.dart: mobile app entry
