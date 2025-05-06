import requests
from .config import settings

API_URL = f"https://eth-mainnet.g.alchemy.com/v2/{settings.alchemy_api_key}"


def fetch_txs(wallet: str, max_count: int = 1_000) -> list[dict]:
    payload = {
      "jsonrpc": "2.0",
      "method": "alchemy_getAssetTransfers",
      "params": [{
         "fromAddress": wallet,
         "category": ["external", "erc20", "erc721", "erc1155"],
         "maxCount": hex(max_count)
      }],
      "id": 1
    }

    resp = requests.post(API_URL, json=payload)
    # 1) Raise if HTTP is not 200
    resp.raise_for_status()

    data = resp.json()
    # import json; print(json.dumps(data, indent=2))

    # 2) If Alchemy returned an error block, show it
    if "error" in data:
        err = data["error"]
        raise RuntimeError(f"Alchemy error {err.get('code')}: {err.get('message')}")

    # 3) Now safely grab transfers
    transfers = data.get("result", {}).get("transfers")
    if transfers is None:
        # Dump the entire response so you can inspect it
        raise RuntimeError(f"No ‘result.transfers’ in response: {data!r}")

    return transfers