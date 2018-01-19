"""Supplies Decorators and utility functions."""
# Import Built-ins
import os
import configparser
from functools import wraps
# Import Homebrew
from bitex.exceptions import UnsupportedEndpointError
from bitex.pairs import PairFormatter
from bitex.responses import ResponseFormatter


def check_version_compatibility(**version_func_pairs):
    """Check for correct version before method execution.

    Checks if the decorated function is compatible with the currently set API version.
    Should this not be the case, an UnsupportedEndpointError is raised.

    If the api version required contains '.', replace it with an
    underscore ('_') - the decorator will take care of it.
    """
    def decorator(func):
        """Decorate wrapper."""
        @wraps(func)
        def wrapped(*args, **kwargs):
            """Wrap function."""
            interface = args[0]
            for version, methods in version_func_pairs.items():
                if func.__name__ in methods:
                    if version.replace('_', '.') != interface.REST.version:
                        error_msg = ("Method not available on this API version"
                                     "(current is %s, supported is %s)" %
                                     (interface.REST.version,
                                      version.replace('_', '.')))
                        raise UnsupportedEndpointError(error_msg)

            return func(*args, **kwargs)
        return wrapped
    return decorator

# pylint: disable=protected-access


def check_and_format_pair(func):
    """Execute format_for() method if available, and assert that pair is supported by the exchange.

    When using this decorator, make sure that the first positional argument of
    the wrapped method is the pair, otherwise behaviour is undefined.
    """
    @wraps(func)
    def wrapped(self, *args, **kwargs):
        """Wrap function."""
        pair, *_ = args
        try:
            if isinstance(args[0], PairFormatter):
                pair = pair.format_for(self.name)
                args = list(args)
                args[0] = pair
        except IndexError:
            pass
        if pair not in self._supported_pairs:
            raise AssertionError("%s is not supported by this exchange!" % pair)
        return func(self, *args, **kwargs)
    return wrapped


def load_configuration(fname):
    """Load the configuration file.

    Returns a configparser.ConfigParser() object.
    """
    if not os.path.exists(fname) or not os.path.isfile(fname):
        return None
    config = configparser.ConfigParser()
    config.read(fname)
    return config


def check_and_format_response(func):
    @wraps(func)
    def wrapped(self, *args, **kwargs):
        if 'formatter' in kwargs:
            formatter = kwargs['formatter']
        else:
            raise RuntimeError(f'Could not find formatter in kwargs ({kwargs})')
        result = func(self, *args, **kwargs)
        try:
            if isinstance(formatter, ResponseFormatter):
                result = formatter.format_response_for(result, func.__name__, self.name)
        except IndexError:
            pass
        return result
    return wrapped
