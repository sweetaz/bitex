# -*- coding: utf-8 -*-

from bitex.pairs import PairFormatter
from requests.exceptions import HTTPError

class ResponseFormatter(PairFormatter):

    def __init__(self, base, quote):
        """Initialize formatter instance."""
        super().__init__(base, quote)
        self.func_name_map = {'Kraken':                'kraken_{}_response_formatter',
                              'Bitstamp':              'bitstamp_{}_response_formatter',
                              'Bitfinex':              'bitfinex_{}_response_formatter',
                              'Bittrex':               'bittrex_{}_response_formatter',
                              'CoinCheck':             'coincheck_{}_response_formatter',
                              'GDAX':                  'gdax_{}_response_formatter',
                              'ITBit':                 'itbit_{}_response_formatter',
                              'OKCoin':                'okcoin_{}_response_formatter',
                              'OKEX':                  'okex_{}_response_formatter',
                              'CCEX':                  'ccex_{}_response_formatter',
                              'Cryptopia':             'cryptopia_{}_response_formatter',
                              'Gemini':                'gemini_{}_response_formatter',
                              'The Rock Trading Ltd.': 'rocktrading_{}_response_formatter',
                              'Poloniex':              'poloniex_{}_response_formatter',
                              'Quoine':                'quoine_{}_response_formatter',
                              'QuadrigaCX':            'quadriga_{}_response_formatter',
                              'HitBTC':                'hitbtc_{}_response_formatter',
                              'Vaultoro':              'vaultoro_{}_response_formatter',
                              'Bter':                  'bter_{}_response_formatter',
                              'Yunbi':                 'yunbi_{}_response_formatter',
                              'Binance':               'binance_{}_response_formatter'}

    def format_response_for(self, response, func_name, exchange_name):
        """Format the response from the given exchange."""
        result = self.basic_response_formatter(response)
        static_func_name = self.func_name_map[exchange_name].format(func_name)
        try:
            func = getattr(self, static_func_name)
            result = func(self.format_for(exchange_name), result)
        except AttributeError:
            pass
        return result

    @staticmethod
    def basic_response_formatter(response):
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPError(response=response)

    #-- ticker() ----
    @staticmethod
    def kraken_ticker_response_formatter(pair, response):
        return response['result'][pair]

    @staticmethod
    def bittrex_ticker_response_formatter(pair, response):
        return [item for item in  response['result'] if item['MarketName'] ==  pair][0]

    @staticmethod
    def poloniex_ticker_response_formatter(pair, response):
        return response[pair]

    #-- order_book() ----
    @staticmethod
    def kraken_order_book_response_formatter(pair, response):
        result = {'bids': [], 'asks': []}
        for k in result:
            result[k].extend([{'price': float(i[0]), 'amount': float(i[1])} for i in response['result'][pair][k]])
        return result

    @staticmethod
    def bittrex_order_book_response_formatter(pair, response):
        result = {'bids': [], 'asks': []}
        keymap = {'bids': 'buy', 'asks': 'sell'}
        for k in keymap:
            result[k].extend([{'price': i['Rate'], 'amount': i['Quantity']} for i in response['result'][keymap[k]]])
        return result

    @staticmethod
    def bitfinex_order_book_response_formatter(pair, response):
        result = {'bids': [], 'asks': []}
        for k in result:
            result[k].extend([{'price': float(i['price']), 'amount': float(i['amount'])} for i in response[k]])
        return result

    @staticmethod
    def hitbtc_order_book_response_formatter(pair, response):
        result = {'bids': [], 'asks': []}
        for k in result:
            result[k].extend([{'price': float(i[0]), 'amount': float(i[1])} for i in response[k]])
        return result

    @staticmethod
    def okcoin_order_book_response_formatter(pair, response):
        result = {'bids': [], 'asks': []}
        for k in result:
            result[k].extend([{'price': i[0], 'amount': i[1]} for i in response[k]])
        return result

    @staticmethod
    def okex_order_book_response_formatter(pair, response):
        result = {'bids': [], 'asks': []}
        for k in result:
            result[k].extend([{'price': i[0], 'amount': i[1]} for i in response[k]])
        return result

    @staticmethod
    def binance_order_book_response_formatter(pair, response):
        result = {'bids': [], 'asks': []}
        for k in result:
            result[k].extend([{'price': float(i[0]), 'amount': float(i[1])} for i in response[k]])
        return result

    @staticmethod
    def poloniex_order_book_response_formatter(pair, response):
        result = {'bids': [], 'asks': []}
        for k in result:
            result[k].extend([{'price': float(i[0]), 'amount': i[1]} for i in response[k]])
        return result

    @staticmethod
    def bitstamp_order_book_response_formatter(pair, response):
        result = {'bids': [], 'asks': []}
        for k in result:
            result[k].extend([{'price': float(i[0]), 'amount': float(i[1])} for i in response[k]])
        return result

    @staticmethod
    def cryptopia_order_book_response_formatter(pair, response):
        result = {'bids': [], 'asks': []}
        keymap = {'bids': 'Buy', 'asks': 'Sell'}
        for k in keymap:
            result[k].extend([{'price': i['Price'], 'amount': i['Volume']} for i in response['Data'][keymap[k]]])
        return result

    @staticmethod
    def ccex_order_book_response_formatter(pair, response):
        result = {'bids': [], 'asks': []}
        keymap = {'bids': 'buy', 'asks': 'sell'}
        for k in keymap:
            result[k].extend([{'price': i['Rate'], 'amount': i['Quantity']} for i in response['result'][keymap[k]]])
        return result

    #-- wallet() ----
    @staticmethod
    def binance_wallet_response_formatter(pair, response):
        return {i['asset']: float(i['free']) for i in response['balances'] if float(i['free']) > 0.0}

    @staticmethod
    def bitfinex_wallet_response_formatter(pair, response):
        return {i['currency'].upper(): float(i['amount']) for i in response if float(i['amount']) > 0.0}

    @staticmethod
    def bittrex_wallet_response_formatter(pair, response):
        return {i['Currency']: i['Balance'] for i in response['result'] if i['Balance'] > 0.0}

    @staticmethod
    def poloniex_wallet_response_formatter(pair, response):
        return {currency: float(response[currency]) for currency in response if float(response[currency]) > 0.0}

    @staticmethod
    def kraken_wallet_response_formatter(pair, response):
        result = {}
        currencymap = {'XXBT': 'BTC', 'XETH': 'ETH'}
        for currency in response['result']:
            if float(response['result'][currency]) > 0.0:
                if currency in currencymap:
                    result[currencymap[currency]] = float(response['result'][currency])
                else:
                    result[currency] = float(response['result'][currency])
        return result

    @staticmethod
    def okex_wallet_response_formatter(pair, response):
        result = response['info']['funds']['free']
        return {currency.upper(): float(result[currency]) for currency in result if float(result[currency]) > 0.0}

    #-- bid() ----
    @staticmethod
    def binance_bid_response_formatter(pair, response):
        return response

    @staticmethod
    def bitfinex_bid_response_formatter(pair, response):
        return response

    #-- ask() ----
    @staticmethod
    def binance_ask_response_formatter(pair, response):
        return response

    @staticmethod
    def bitfinex_ask_response_formatter(pair, response):
        return response
