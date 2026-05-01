"""phase 1 core tables

Revision ID: 20260501_phase1
Revises:
Create Date: 2026-05-01
"""

from pathlib import Path

from alembic import op

revision = "20260501_phase1"
down_revision = None
branch_labels = None
depends_on = None


def _sql(name: str) -> str:
    return (Path(__file__).resolve().parent.parent / name).read_text(encoding="utf-8")


def upgrade() -> None:
    op.execute(_sql("001_phase1_core_tables.sql"))


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS stock_aliases;")
    op.execute("DROP TABLE IF EXISTS stocks_master;")
    op.execute("DROP TABLE IF EXISTS users;")
