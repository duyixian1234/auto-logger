__version__ = "0.1.1"

import json
import logging
from typing import Any, Callable, Dict, List, Optional, Tuple, Type

logger = logging.getLogger(__name__)


def formatText(
    args: List[Any],
    kwargs: Dict[str, Any],
    ret: Any,
    *,
    objStr: str = "",
    method: Optional[Callable] = None,
    func: Optional[Callable] = None,
):
    if objStr:
        return (
            f"CALL METHOD <{method.__name__ if method else 'Unknown'}>"
            f" OF {objStr} WITH ARGS {args} KWARGS {kwargs} RETURNS  {ret}"
        )
    return (
        f"CALL FUCNTION <{func.__name__ if func else 'Unknown'}>" f" WITH ARGS {args} KWARGS {kwargs} RETURNS  {ret}"
    )


def formatJson(
    args: List[Any],
    kwargs: Dict[str, Any],
    ret: Any,
    *,
    objStr: str = "",
    method: Optional[Callable] = None,
    func: Optional[Callable] = None,
):
    data = dict(args=args, kwargs=kwargs, ret=ret)
    if objStr:
        data["method"] = method.__name__ if method else "Unknown"
        data["object"] = objStr
    else:
        data["function"] = func.__name__ if func else "Unknown"
    return json.dumps(data, cls=Config.jsonEncoder)


class Config:
    format = formatText
    log = logger.info
    ignoreMethods: Dict[Type, str] = dict()
    jsonEncoder: Optional[Type[json.JSONEncoder]] = None


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
