# Discord Korean Stock Portfolio Assistant

Minimal production-ready Python project scaffold for a Discord-based Korean stock portfolio assistant.

## Tech Stack
- Python 3.12
- PostgreSQL (Supabase)
- SQLAlchemy 2.x
- Alembic
- discord.py
- python-dotenv

## Structure
- `app/` - bot and service modules
- `db/` - SQLAlchemy base, session, models, and migrations
- `tests/` - test suite

## Setup
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create `.env` from `.env.example` and set values.
4. Run migrations with Alembic.
