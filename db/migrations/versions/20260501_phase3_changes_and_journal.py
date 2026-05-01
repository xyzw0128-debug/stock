"""phase 3 changes and journal

Revision ID: 20260501_phase3
Revises: 20260501_phase2
Create Date: 2026-05-01
"""

from pathlib import Path

from alembic import op

revision = "20260501_phase3"
down_revision = "20260501_phase2"
branch_labels = None
depends_on = None


def _sql(name: str) -> str:
    return (Path(__file__).resolve().parent.parent / name).read_text(encoding="utf-8")


def upgrade() -> None:
    op.execute(_sql("202605010001_phase3.sql"))


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS journal_entries;")
    op.execute("DROP TABLE IF EXISTS portfolio_changes;")
