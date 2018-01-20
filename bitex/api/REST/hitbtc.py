"""Bitstamp REST API backend.

Documentation available here:
    https://www.bitstamp.net/api/
"""
# Import Built-ins
import logging
import hashlib
import hmac
import urllib
import urllib.parse

# Import Homebrew
from bitex.api.REST import RESTAPI

# Init Logging Facilities
log = logging.getLogger(__name__)


class HitBTCREST(RESTAPI):
    """HitBTC REST API class."""

    def __init__(self, key=None, secret=None, version=None,
                 addr=None, timeout=5, config=None):
        """Initialize the class instance."""
        version = '1' if not version else version
        addr = 'https://api.hitbtc.com' if not addr else addr
        super(HitBTCREST, self).__init__(addr=addr, version=version,
                                         key=key, secret=secret,
                                         timeout=timeout, config=config)

    def generate_uri(self, endpoint):
        return '/api/' + self.version + '/' + endpoint

    def sign_request_kwargs(self, endpoint, **kwargs):
        """Sign the request."""
        req_kwargs = super(HitBTCREST, self).sign_request_kwargs(endpoint,
                                                                 **kwargs)

        # prepare Payload arguments
        try:
            params = dict(kwargs['params'])
        except KeyError:
            params = {}
        nonce = self.nonce()
        params['apikey'] = self.key
        params['nonce'] = nonce
        path = self.generate_uri(endpoint) + '?' + urllib.parse.urlencode(params)

        # generate signature
        signature = hmac.new(self.secret.encode(encoding='utf-8'),
                             path.encode(encoding='utf-8'),
                             hashlib.sha512).hexdigest()

        # update req_kwargs keys
        req_kwargs['headers'] = {'Api-Signature': signature}
        req_kwargs['url'] = self.generate_url(path)

        return req_kwargs
