"""phase 2 portfolio tables

Revision ID: 20260501_phase2
Revises: 
Create Date: 2026-05-01
"""

from alembic import op


# revision identifiers, used by Alembic.
revision = "20260501_phase2"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE portfolio_snapshots (
            id              SERIAL PRIMARY KEY,
            user_id         INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            created_at      TIMESTAMPTZ DEFAULT NOW(),
            source_broker   VARCHAR(50),
            total_value     NUMERIC(18,2),
            total_pnl       NUMERIC(18,2),
            cash_balance    NUMERIC(18,2),
            ocr_score       INTEGER,
            ocr_method      VARCHAR(20),
            raw_ocr_text    TEXT,
            image_ref       TEXT,
            is_confirmed    BOOLEAN DEFAULT FALSE
        );

        CREATE INDEX idx_snapshots_user_created
        ON portfolio_snapshots(user_id, created_at DESC);
        """
    )

    op.execute(
        """
        CREATE TABLE holdings (
            id              SERIAL PRIMARY KEY,
            snapshot_id     INTEGER NOT NULL REFERENCES portfolio_snapshots(id) ON DELETE CASCADE,
            ticker          VARCHAR(10) REFERENCES stocks_master(ticker),
            stock_name      VARCHAR(100) NOT NULL,
            normalized_name VARCHAR(100),
            quantity        INTEGER NOT NULL CHECK (quantity >= 0),
            avg_price       NUMERIC(12,2) NOT NULL CHECK (avg_price >= 0),
            current_price   NUMERIC(12,2),
            market_value    NUMERIC(18,2),
            pnl             NUMERIC(18,2),
            pnl_pct         NUMERIC(8,4),
            weight_pct      NUMERIC(8,4),
            is_matched      BOOLEAN DEFAULT FALSE,
            match_score     INTEGER,
            UNIQUE(snapshot_id, ticker)
        );

        CREATE INDEX idx_holdings_snapshot ON holdings(snapshot_id);
        CREATE INDEX idx_holdings_ticker   ON holdings(ticker);
        """
    )

    op.execute(
        """
        CREATE TABLE ocr_unmatched (
            id              SERIAL PRIMARY KEY,
            snapshot_id     INTEGER NOT NULL REFERENCES portfolio_snapshots(id) ON DELETE CASCADE,
            raw_name        VARCHAR(100),
            quantity        INTEGER,
            avg_price       NUMERIC(12,2),
            resolved_ticker VARCHAR(10) REFERENCES stocks_master(ticker),
            status          VARCHAR(20) DEFAULT 'pending',
            resolved_at     TIMESTAMPTZ,
            created_at      TIMESTAMPTZ DEFAULT NOW(),
            CONSTRAINT chk_ocr_unmatched_status
                CHECK (status IN ('pending', 'resolved', 'ignored'))
        );

        CREATE INDEX idx_unmatched_snapshot ON ocr_unmatched(snapshot_id);
        CREATE INDEX idx_unmatched_status   ON ocr_unmatched(status);
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS ocr_unmatched;")
    op.execute("DROP TABLE IF EXISTS holdings;")
    op.execute("DROP TABLE IF EXISTS portfolio_snapshots;")
