import json
from dataclasses import dataclass
from unittest import mock

from auto_logger.auto_logger import MethodLoggerMeta, logFuncCall
from auto_logger.config import Config
from auto_logger.json_formatter import formatJson
from auto_logger.text_formatter import formatText


@dataclass
class Square(metaclass=MethodLoggerMeta):
    sideLength: int

    def __init__(self, sideLength: int):
        self.sideLength = sideLength

    def area(self):
        return self.sideLength ** 2

    def perimeter(self):
        return self.sideLength * 4


def testFormatText():
    assert (
        formatText((1, 2), dict(a="a", b="b"), True, func=print)
        == "CALL FUCNTION <print> WITH ARGS (1, 2) KWARGS {'a': 'a', 'b': 'b'} RETURNS  True"
    )
    assert (
        formatText((1, 2), dict(a="a", b="b"), True, objStr="object()", method=object.__str__)
        == "CALL METHOD <__str__> OF object() WITH ARGS (1, 2) KWARGS {'a': 'a', 'b': 'b'} RETURNS  True"
    )


def testFormatJson():
    assert (
        formatJson((1, 2), dict(a="a", b="b"), True, func=print)
        == '{"args": [1, 2], "kwargs": {"a": "a", "b": "b"}, "ret": true, "function": "print"}'
    )

    class A:
        a: int = 0

    class Encoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, A):
                return f"A(a={o.a})"

    Config.jsonEncoder = Encoder

    assert (
        formatJson((1, 2), dict(a="a", b="b", c=A()), True, objStr="object()", method=object.__str__)
        == '{"args": [1, 2], "kwargs": {"a": "a", "b": "b", "c": "A(a=0)"}, "ret": true, "method": "__str__", "object": "object()"}'
    )


def testLogFuncCall():
    mockLog = mock.Mock()
    Config.log = mockLog

    @logFuncCall
    def add(a: int, b: int):
        return a + b

    add(1, 2)
    mockLog.assert_called_with("CALL FUCNTION <add> WITH ARGS (1, 2) KWARGS {} RETURNS  3")

    Config.format = formatJson
    add(1, b=2)
    mockLog.assert_called_with('{"args": [1], "kwargs": {"b": 2}, "ret": 3, "function": "add"}')


def testLogMethodCall():
    mockLog = mock.Mock()
    Config.log = mockLog
    Config.format = formatText
    square = Square(4)
    square.area()
    mockLog.assert_called_with("CALL METHOD <area> OF Square(sideLength=4) WITH ARGS () KWARGS {} RETURNS  16")

    Config.ignoreMethods[Square] = {"perimeter"}
    square.perimeter()
    assert mockLog.call_count == 1
