"""Binance Interface class."""
# Import Built-Ins
import logging

# Import Homebrew
from bitex.api.REST.binance import BinanceREST
from bitex.interface.rest import RESTInterface
from bitex.utils import check_and_format_response

# Init Logging Facilities
log = logging.getLogger(__name__)


class Binance(RESTInterface):
    """Binance Interface class.

    Includes standardized methods, as well as all other Endpoints
    available on their REST API.
    """

    # pylint: disable=arguments-differ

    def __init__(self, **api_kwargs):
        """Initialize class instance."""
        super(Binance, self).__init__('Binance', BinanceREST(**api_kwargs))

    def request(self, verb, endpoint, authenticate=False, **req_kwargs):
        """Preprocess request to API."""
        return super(Binance, self).request(verb, endpoint, authenticate=authenticate,
                                            **req_kwargs)

    def _get_supported_pairs(self):
        """Return a list of supported pairs."""
        r = self.request('GET', 'v1/exchangeInfo').json()
        pairs = [entry['symbol'] for entry in r['symbols']]
        return pairs

    @check_and_format_response
    def ticker(self, pair, *args, **kwargs):
        """Return the ticker for the given pair."""
        payload = {'symbol': pair}
        payload.update(kwargs)
        return self.request('GET', 'v1/ticker/24hr', params=payload)

    @check_and_format_response
    def order_book(self, pair, *args, **kwargs):
        """Return the order book for the given pair."""
        payload = {'symbol': pair}
        payload.update(kwargs)
        return self.request("GET", "v1/depth", params=payload)

    def trades(self, pair, *args, **kwargs):
        """Return the trades for the given pair."""
        payload = {'symbol': pair}
        payload.update(kwargs)
        return self.request('GET', 'v1/trades', params=payload)

    # Private Endpoints
    def _place_order(self, pair, price, size, side, *args, **kwargs):
        payload = {'symbol': pair,
                   'side': side,
                   'type': "LIMIT",       # limit-maker won't accpet taker orders
                   'timeInForce': 'GTC',  # GTC=Good-til-cancelled, IOC=Immediate-or-kill, FOK=fill-or-kill
                   'price': price,
                   'quantity': size}
        payload.update(kwargs)
        return self.request('POST', 'v3/order', authenticate=True, params=payload)

    def ask(self, pair, price, size, *args, **kwargs):
        """Place an ask order."""
        return self._place_order(pair, price, size, "SELL", *args, **kwargs)

    def bid(self, pair, price, size, *args, **kwargs):
        """Place a bid order."""
        return self._place_order(pair, price, size, "BUY", *args, **kwargs)

    def order_status(self, pair, order_id, *args, **kwargs):
        """Return the status of an order with the given id."""
        payload = {'symbol': pair,
                   'orderId': order_id}
        payload.update(kwargs)
        return self.request('GET', 'v3/order', authenticate=True, params=payload)

    def open_orders(self, *args, **kwargs):
        """Return all open orders."""
        return self.request('GET', 'v3/openOrders', authenticate=True, params=kwargs)

    def cancel_order(self, pair, *order_ids, **kwargs):
        """Cancel the order(s) with the given id(s)."""
        results = []
        for order_id in order_ids:
            payload = {'symbol': pair,
                       'orderId': order_id}
            payload.update(kwargs)
            r = self.request('DELETE', 'v3/order', authenticate=True, params=payload)
            results.append(r)

        return results if len(results) > 1 else results[0]

    def wallet(self, *args, **kwargs):
        """Return the wallet of this account."""
        return self.request('GET', "v3/account", True) # .json()['balances']

    def withdraw(self, currency, amount, address):
        payload = {'asset': currency,
                   'address': address,
                   'amount': amount}
        return self.request('POST', 'v3/withdraw', authenticate=True, params=payload)