-- upgrade()
CREATE TABLE user_preferences (
    user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    preferred_broker VARCHAR(50),
    concentration_alert_pct NUMERIC(5,2) DEFAULT 30.00,
    cash_alert_pct NUMERIC(5,2) DEFAULT 10.00,
    notify_on_upload BOOLEAN DEFAULT TRUE,
    language VARCHAR(10) DEFAULT 'ko',
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE upload_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    snapshot_id INTEGER REFERENCES portfolio_snapshots(id),
    filename VARCHAR(255),
    upload_status VARCHAR(20) CHECK (
        upload_status IN (
            'SUCCESS',
            'FAILED',
            'PARSING',
            'CONFIRMED'
        )
    ),
    error_message TEXT,
    processing_ms INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_upload_logs_user_created
ON upload_logs(user_id, created_at DESC);

-- downgrade()
DROP INDEX IF EXISTS idx_upload_logs_user_created;
DROP TABLE IF EXISTS upload_logs;
DROP TABLE IF EXISTS user_preferences;
