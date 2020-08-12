from .lexer import (lex, ID,
                    DELIMITER, OPEN_BRACKET,
                    CLOSE_BRACKET, STRING,
                    FLOAT, INTEGER, BOOLEAN)

value_converters = {
    STRING: lambda string: string[1:-1],
    FLOAT: float,
    INTEGER: int,
    BOOLEAN: lambda string: string == "true"
}


def eval_value(value, label):
    return value_converters[label](value)


def _parse(dest, source, until_label=None):
    pos = 0

    while pos < len(source):
        first, first_type = source[pos]

        if first_type == until_label:
            pos += 1

            break

        try:
            second, second_type = source[pos+1]
        except IndexError:
            second, second_type = None, None

        try:
            third, third_type = source[pos+2]
        except IndexError:
            third, third_type = None, None

        if first_type == ID and second_type == OPEN_BRACKET:
            dest[first] = {}
            end_pos = _parse(dest[first], source[pos+2:], CLOSE_BRACKET)

            pos += end_pos+2
        elif first_type == ID and second_type == DELIMITER:
            dest[first] = eval_value(third, third_type)

            pos += 3
        else:
            raise SyntaxError("Invalid syntax")

    return pos


def parse(text):
    tokens = lex(text)

    config = {}

    _parse(config, tokens)

    return config
