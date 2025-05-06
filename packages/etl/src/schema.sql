CREATE TABLE IF NOT EXISTS wallet_txs (
  id            SERIAL PRIMARY KEY,
  wallet        TEXT    NOT NULL,
  tx_hash       TEXT    UNIQUE NOT NULL,
  block_number  BIGINT  NOT NULL,
  timestamp     TIMESTAMPTZ NOT NULL,
  from_address  TEXT    NOT NULL,
  to_address    TEXT,
  value         NUMERIC NOT NULL,
  gas_used      BIGINT,
  chain         TEXT    NOT NULL,
  fetched_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
