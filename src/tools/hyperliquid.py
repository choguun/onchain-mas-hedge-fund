from dotenv import load_dotenv
import os
from hyperliquid.info import Info
from hyperliquid.utils import constants

load_dotenv()

info = Info(constants.TESTNET_API_URL, skip_ws=True)

class HyperLiquid:
    def __init__(self):
        self.api_key = os.environ.get("HYPER_API_KEY")

