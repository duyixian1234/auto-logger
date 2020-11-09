import json
from typing import Any, Callable, Dict, List, Optional

from .config import Config

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
