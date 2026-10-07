# TradePilot Deriv

A mobile-first trading automation project for Deriv using a LuxAlgo-inspired pivot strategy on the 15-minute timeframe.

What is in this repo
- FastAPI backend for strategy/config APIs
- Deriv WebSocket client scaffold
- 15m pivot strategy logic
- risk manager
- symbol catalog for forex and synthetic instruments
- Flutter starter dashboard
- Dockerized Postgres

Quick start

1. Copy env file:
   cp docker/.env.example docker/.env

2. Start postgres:
   docker compose -f docker/docker-compose.yml up -d

3. Install backend dependencies:
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

4. Run backend:
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

5. Open the API docs:
   http://localhost:8000/docs

6. Run the mobile app:
   cd mobile
   flutter pub get
   flutter run

Important notes
- Use a demo account first.
- Verify exact Deriv symbol names and contract types in your account before going live.
- This is a starter architecture, not a guarantee of profit.
