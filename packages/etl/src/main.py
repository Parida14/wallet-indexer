import argparse
from .fetcher import fetch_txs
from .loader import save_txs

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--wallet", required=True, help="0x…")
    args = p.parse_args()

    txs = fetch_txs(args.wallet)
    count = save_txs(args.wallet, txs)
    print({"wallet": args.wallet, "fetched": len(txs), "inserted": count})

if __name__ == "__main__":
    main()
