-- upgrade()
CREATE TABLE portfolio_changes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    previous_snapshot_id INTEGER REFERENCES portfolio_snapshots(id),
    new_snapshot_id INTEGER REFERENCES portfolio_snapshots(id),
    ticker VARCHAR(10) REFERENCES stocks_master(ticker),
    stock_name VARCHAR(100),
    change_type VARCHAR(20) CHECK (
        change_type IN (
            'NEW_POSITION',
            'SOLD_OUT',
            'SIZE_UP',
            'SIZE_DOWN',
            'AVG_DOWN',
            'AVG_UP'
        )
    ),
    prev_quantity INTEGER,
    new_quantity INTEGER,
    prev_avg_price NUMERIC(12,2),
    new_avg_price NUMERIC(12,2),
    prev_weight_pct NUMERIC(8,4),
    new_weight_pct NUMERIC(8,4),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_changes_user
ON portfolio_changes(user_id, created_at DESC);

CREATE TABLE journal_entries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    snapshot_id INTEGER REFERENCES portfolio_snapshots(id),
    entry_date DATE NOT NULL,
    raw_input TEXT,
    ai_summary TEXT,
    emotion_tag VARCHAR(20) CHECK (
        emotion_tag IN (
            'confident',
            'anxious',
            'regret',
            'neutral',
            'greedy',
            'fearful'
        )
    ),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_journal_user_date
ON journal_entries(user_id, entry_date DESC);

CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    snapshot_id INTEGER REFERENCES portfolio_snapshots(id),
    alert_type VARCHAR(30) CHECK (
        alert_type IN (
            'HIGH_CONCENTRATION',
            'AVG_DOWN_REPEATED',
            'CASH_LOW',
            'LARGE_LOSS',
            'RAPID_WEIGHT_CHANGE'
        )
    ),
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_alerts_user_unread
ON alerts(user_id)
WHERE is_read = FALSE;

-- downgrade()
DROP INDEX IF EXISTS idx_alerts_user_unread;
DROP TABLE IF EXISTS alerts;

DROP INDEX IF EXISTS idx_journal_user_date;
DROP TABLE IF EXISTS journal_entries;

DROP INDEX IF EXISTS idx_changes_user;
DROP TABLE IF EXISTS portfolio_changes;
