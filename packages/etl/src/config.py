# packages/etl/src/config.py
import os

class Settings:
    def __init__(self):
        try:
            self.database_url   = os.environ["DATABASE_URL"]
            self.alchemy_api_key = os.environ["ALCHEMY_API_KEY"]
        except KeyError as e:
            raise RuntimeError(f"Missing required env var: {e.args[0]}") from None

settings = Settings()
