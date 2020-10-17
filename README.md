# Auto-logger

![CI](https://github.com/duyixian1234/auto-logger/workflows/CI/badge.svg?branch=master)

Automatically add function call logs and method call logs for Python code.

## Install

```bash
pip install -U auto-logger
```

## Use

```python
import logging
from dataclasses import dataclass

from auto_logger import Config, MethodLoggerMeta, logFuncCall,formatJson

logging.basicConfig(level=logging.INFO)


@logFuncCall
def add(a: int, b: int):
    return a + b


add(1, 2) # INFO:auto_logger:CALL FUCNTION <add> WITH ARGS (1, 2) KWARGS {} RETURNS  3
add(a=1, b=2) # INFO:auto_logger:CALL FUCNTION <add> WITH ARGS () KWARGS {'a': 1, 'b': 2} RETURNS  3


@dataclass
class A(metaclass=MethodLoggerMeta):
    a: int = 0

    def add(self, n: int):
        self.a += 1

    def abs(self):
        return abs(self.a)

A().add(1)  # INFO:auto_logger:CALL METHOD <add> OF A(a=0) WITH ARGS (1,) KWARGS {} RETURNS  None


Config.format = formatJson
A().add(1) # INFO:auto_logger:{"args": [1], "kwargs": {}, "ret": null, "method": "add", "object": "A(a=0)"}

Config.ignoreMethods[A] = {'abs'}
A().abs() # Log nothing
```
