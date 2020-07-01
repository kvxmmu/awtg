# AWTG base plugin

plugin examples:
```python

class ClassFilter:
    def __init__(self, arg):
        self.arg = arg

    def __call__(self, message):
        return message.data.get_text() == self.arg


def function_filter(message):
    return message.data.get_text() == 'op'

```
