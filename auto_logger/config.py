import json
from typing import Callable, Dict, Optional, Type

from .text_formatter import formatText


class Config:
    format: Callable = formatText
    log: Callable = print
    ignoreMethods: Dict[Type, str] = dict()
    jsonEncoder: Optional[Type[json.JSONEncoder]] = None
