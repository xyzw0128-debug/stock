"""phase 4 alerts and settings

Revision ID: 20260501_phase4
Revises: 20260501_phase3
Create Date: 2026-05-01
"""

from pathlib import Path

from alembic import op

revision = "20260501_phase4"
down_revision = "20260501_phase3"
branch_labels = None
depends_on = None


def _sql(name: str) -> str:
    return (Path(__file__).resolve().parent.parent / name).read_text(encoding="utf-8")


def upgrade() -> None:
    op.execute(_sql("20260501000000_phase4.sql"))


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS alerts;")
    op.execute("DROP TABLE IF EXISTS user_preferences;")
    op.execute("DROP TABLE IF EXISTS upload_logs;")
