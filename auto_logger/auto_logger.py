import logging
from typing import Tuple

from .config import Config

logger = logging.getLogger(__name__)


def logMethodCall(func):
    def inner(self, *args, **kwargs):
        objStr = repr(self)
        ret = func(self, *args, **kwargs)
        if func.__name__ not in Config.ignoreMethods.get(type(self), set({})):
            Config.log(Config.format(args, kwargs, ret, objStr=objStr, method=func))
        return ret

    return inner


def logFuncCall(func):
    def inner(*args, **kwargs):
        ret = func(*args, **kwargs)
        Config.log(Config.format(args, kwargs, ret, func=func))
        return ret

    return inner


class MethodLoggerMeta(type):
    def __new__(cls, name: str, bases: Tuple[type], attrs: dict):
        attrs_copy = attrs.copy()
        for key, value in attrs.items():
            if callable(value) and not key.startswith("__"):
                attrs_copy[key] = logMethodCall(value)
        return type(name, bases, attrs_copy)
