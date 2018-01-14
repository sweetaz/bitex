"""BitEx - Crypto-Exchange REST API Framework.

Author: Nils Diefenbach
Email: 23okrs20+github@mykolab.com
Repository at: https://github.com/nlsdfnbch/bitex
License: MIT
"""
from bitex.api.REST import BinanceREST, BitstampREST, BterREST, BitfinexREST, BleutradeREST
from bitex.api.REST import CryptopiaREST, CoincheckREST, CCEXREST
from bitex.api.REST import GDAXREST, GeminiREST
from bitex.api.REST import HitBTCREST
from bitex.api.REST import IndependentReserveREST
from bitex.api.REST import ITbitREST
from bitex.api.REST import KiwiCoinREST
from bitex.api.REST import KrakenREST
from bitex.api.REST import NZBCXREST
from bitex.api.REST import OKCoinREST, OKEXREST
from bitex.api.REST import PoloniexREST
from bitex.api.REST import QuadrigaCXREST, QuoineREST
from bitex.api.REST import RockTradingREST
from bitex.api.REST import VaultoroREST
from bitex.api.REST import WEXREST
from bitex.api.REST import YunbiREST
from bitex.interface import Bter, Binance, Bitfinex, Bittrex, Bitstamp, Bleutrade, CCEX, CoinCheck
from bitex.interface import Cryptopia, HitBTC, IndependentReserve, KiwiCoin, Kraken, NZBCX, OKCoin
from bitex.interface import OKEX, Poloniex, QuadrigaCX, TheRockTrading, Vaultoro, WEX
from bitex.pairs import BTCUSD, ZECUSD, XMRUSD, ETCUSD, ETHUSD, DASHUSD
