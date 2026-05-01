CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    discord_user_id VARCHAR(32) NOT NULL UNIQUE,
    username VARCHAR(100),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS stocks_master (
    ticker VARCHAR(10) PRIMARY KEY,
    stock_name VARCHAR(100) NOT NULL,
    short_name VARCHAR(50),
    market VARCHAR(10) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT ck_stocks_master_market CHECK (market IN ('KOSPI', 'KOSDAQ', 'KONEX'))
);

CREATE TABLE IF NOT EXISTS stock_aliases (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL REFERENCES stocks_master(ticker) ON DELETE CASCADE,
    alias VARCHAR(100) NOT NULL,
    source VARCHAR(50) NOT NULL,
    confidence_score INTEGER NOT NULL DEFAULT 100,
    CONSTRAINT uq_stock_aliases_alias_source UNIQUE (alias, source)
);

CREATE INDEX IF NOT EXISTS ix_stocks_master_stock_name ON stocks_master (stock_name);
CREATE INDEX IF NOT EXISTS ix_stock_aliases_alias ON stock_aliases (alias);
CREATE INDEX IF NOT EXISTS ix_stock_aliases_ticker ON stock_aliases (ticker);
