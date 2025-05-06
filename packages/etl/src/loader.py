import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime
from .config import settings

INSERT_SQL = """
INSERT INTO wallet_txs
  (wallet, tx_hash, block_number, timestamp,
   from_address, to_address, value, gas_used, chain)
VALUES %s
ON CONFLICT (tx_hash) DO NOTHING;
"""

def save_txs(wallet: str, txs: list[dict], chain: str = "ethereum") -> int:
    rows = []
    skipped = 0

    for tx in txs:
        meta = tx.get("metadata")
        if not meta or "blockTimestamp" not in meta:
            skipped += 1
            continue

        ts = datetime.fromisoformat(meta["blockTimestamp"].rstrip("Z"))
        block_num = int(tx.get("blockNum","0x0"), 16)
        value     = int(tx.get("value", "0"), 10)
        gas_used  = int(tx.get("gas",   "0"), 10)

        rows.append((
            wallet,
            tx.get("hash"),
            block_num,
            ts,
            tx.get("from"),
            tx.get("to"),
            value,
            gas_used,
            chain
        ))

    with psycopg2.connect(settings.database_url) as conn:
        with conn.cursor() as cur:
            # 1) How many rows exist for this wallet right now?
            cur.execute("SELECT COUNT(*) FROM wallet_txs WHERE wallet = %s", (wallet,))
            before = cur.fetchone()[0]

            # 2) Bulk insert (skipping conflicts)
            execute_values(cur, INSERT_SQL, rows)

            # 3) How many rows now?
            cur.execute("SELECT COUNT(*) FROM wallet_txs WHERE wallet = %s", (wallet,))
            after = cur.fetchone()[0]

    inserted = after - before
    print(f"Skipped {skipped} transfers without metadata; inserted {inserted} new rows.")
    return inserted
