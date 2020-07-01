# AWTG base plugin

Filter examples:
```python

class ClassFilter:
    def __init__(self, arg):
        self.arg = arg

    def __call__(self, message):
        return message.data.get_text() == self.arg


def function_filter(message):
    return message.data.get_text() == 'op'

```


filter `__call__` signature: `Filter(entity[, manager])`

All AsyncHandler that marked as callback handler are used to handle callback queries

