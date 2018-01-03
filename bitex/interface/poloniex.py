"""Poloniex Interface class."""
# Import Built-Ins
import logging

# Import Homebrew
from bitex.api.REST.poloniex import PoloniexREST
from bitex.interface.rest import RESTInterface
from bitex.utils import check_and_format_pair

# Init Logging Facilities
log = logging.getLogger(__name__)


class Poloniex(RESTInterface):
    """Poloniex Interface class."""

    def __init__(self, **api_kwargs):
        """Initialize Interface class instance."""
        super(Poloniex, self).__init__('Poloniex', PoloniexREST(**api_kwargs))

    # pylint: disable=arguments-differ
    def request(self, endpoint, authenticate=False, **req_kwargs):
        """Generate a request to the API."""
        if 'params' in req_kwargs:
            req_kwargs['params'].update({'command': endpoint})
        else:
            req_kwargs['params'] = {'command': endpoint}
        if authenticate:
            return super(Poloniex, self).request('POST', endpoint, authenticate,
                                                 **req_kwargs)
        return super(Poloniex, self).request('GET', 'public', authenticate,
                                             **req_kwargs)

    def _get_supported_pairs(self):
        # http get https://poloniex.com/public\?command\=returnTicker | jq -c 'keys'
        return ['BTC_AMP', 'BTC_ARDR', 'BTC_BCH', 'BTC_BCN', 'BTC_BCY', 'BTC_BELA', 'BTC_BLK',
                'BTC_BTCD', 'BTC_BTM', 'BTC_BTS', 'BTC_BURST', 'BTC_CLAM', 'BTC_CVC', 'BTC_DASH',
                'BTC_DCR', 'BTC_DGB', 'BTC_DOGE', 'BTC_EMC2', 'BTC_ETC', 'BTC_ETH', 'BTC_EXP',
                'BTC_FCT', 'BTC_FLDC', 'BTC_FLO', 'BTC_GAME', 'BTC_GAS', 'BTC_GNO', 'BTC_GNT',
                'BTC_GRC', 'BTC_HUC', 'BTC_LBC', 'BTC_LSK', 'BTC_LTC', 'BTC_MAID', 'BTC_NAV',
                'BTC_NEOS', 'BTC_NMC', 'BTC_NXC', 'BTC_NXT', 'BTC_OMG', 'BTC_OMNI', 'BTC_PASC',
                'BTC_PINK', 'BTC_POT', 'BTC_PPC', 'BTC_RADS', 'BTC_REP', 'BTC_RIC', 'BTC_SBD',
                'BTC_SC', 'BTC_STEEM', 'BTC_STORJ', 'BTC_STR', 'BTC_STRAT', 'BTC_SYS', 'BTC_VIA',
                'BTC_VRC', 'BTC_VTC', 'BTC_XBC', 'BTC_XCP', 'BTC_XEM', 'BTC_XMR', 'BTC_XPM',
                'BTC_XRP', 'BTC_XVC', 'BTC_ZEC', 'BTC_ZRX', 'ETH_BCH', 'ETH_CVC', 'ETH_ETC',
                'ETH_GAS', 'ETH_GNO', 'ETH_GNT', 'ETH_LSK', 'ETH_OMG', 'ETH_REP', 'ETH_STEEM',
                'ETH_ZEC', 'ETH_ZRX', 'USDT_BCH', 'USDT_BTC', 'USDT_DASH', 'USDT_ETC', 'USDT_ETH',
                'USDT_LTC', 'USDT_NXT', 'USDT_REP', 'USDT_STR', 'USDT_XMR', 'USDT_XRP', 'USDT_ZEC',
                'XMR_BCN', 'XMR_BLK', 'XMR_BTCD', 'XMR_DASH', 'XMR_LTC', 'XMR_MAID', 'XMR_NXT',
                'XMR_ZEC']

    # Public Endpoints
    @check_and_format_pair
    def ticker(self, pair, *args, **kwargs):
        """Return the ticker for the given pair."""
        return self.request('returnTicker', params=kwargs)

    @check_and_format_pair
    def order_book(self, pair, *args, **kwargs):
        """Return the order book for the given pair."""
        payload = {'currencyPair': pair}
        payload.update(kwargs)
        return self.request('returnOrderBook', params=payload)

    @check_and_format_pair
    def trades(self, pair, *args, **kwargs):
        """Return the trades for the given pair."""
        payload = {'currencyPair': pair}
        payload.update(kwargs)
        return self.request('returnTradeHistory', params=payload)

    # Private Endpoints
    def _place_order(self, pair, price, size, side, **kwargs):
        """Place an order with the given parameters."""
        payload = {'currencyPair': pair, 'rate': price, 'amount': size}
        payload.update(kwargs)
        if side == 'bid':
            return self.request('buy', authenticate=True, params=payload)
        return self.request('sell', authenticate=True, params=payload)

    @check_and_format_pair
    def ask(self, pair, price, size, *args, **kwargs):
        """Place an ask order."""
        raise NotImplementedError

    @check_and_format_pair
    def bid(self, pair, price, size, *args, **kwargs):
        """Place a bid order."""
        raise NotImplementedError

    def order_status(self, order_id, *args, **kwargs):
        """Return the order status of the order with given ID."""
        payload = {'orderNumber': order_id}
        payload.update(kwargs)
        return self.request('returnOrderTrades', authenticate=True, params=payload)

    def open_orders(self, *args, **kwargs):
        """Return all open orders."""
        payload = {'currencyPair': 'all'}
        payload.update(kwargs)
        return self.request('returnOpenOrders', authenticate=True, params=payload)

    def cancel_order(self, *order_ids, **kwargs):
        """Cancel order(s) with the given ID(s)."""
        results = []
        payload = kwargs
        for oid in order_ids:
            payload.update({'orderNumber', oid})
            r = self.request('cancelOrder', authenticate=True, params=oid)
            results.append(r)
        return results if len(results) > 1 else results[0]

    def wallet(self, *args, **kwargs):
        """Return the account's wallet."""
        return self.request('returnTradableBalances', authenticate=True, params=kwargs)
