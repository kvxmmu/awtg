from re import compile


OPEN_BRACKET = 0
CLOSE_BRACKET = 1
INTEGER = 2
FLOAT = 3
STRING = 4
ID = 5
DELIMITER = 6
BOOLEAN = 7


def count_lines(data):
    lines = 0

    for char in data:
        if char == '\n':
            lines += 1

    return lines


def convert_escape(char):
    if char == 'b':
        return '\b'
    elif char == 't':
        return '\t'
    elif char == 'r':
        return '\r'
    elif char == 'n':
        return '\n'
    elif char == '"':
        return '"'

    raise SyntaxError("Incorrect escape character %r" % char)


def is_string(text, start):
    chunk = text[start:]
    met_end = False

    if not chunk.startswith('"'):
        return False, None

    data = '"'
    pos = 1

    while True:
        try:
            char = chunk[pos]
        except IndexError:
            break

        if char == '"':
            data += char
            met_end = True

            break

        if char == '\\':
            try:
                escape_value = chunk[pos+1]
            except IndexError:
                raise SyntaxError("Unexpected end of data while parsing string "
                                  "on line %d" % count_lines(text[:start+pos]))
            pos += 1
            data += convert_escape(escape_value)
        else:
            data += char

        pos += 1

    if not met_end:
        raise SyntaxError("Unexpected end of data while parsing string "
                          "on line %d" % count_lines(text[:start+pos]))

    return True, data


tokens = (
    (is_string, STRING),
    (compile(r'(true|false)'), BOOLEAN),

    (compile(r'{'), OPEN_BRACKET),
    (compile(r'}'), CLOSE_BRACKET),

    (compile(r'-?\d+\.\d+'), FLOAT),
    (compile(r'-?\d+'), INTEGER),

    (compile(r'\w+[\d_\w]*'), ID),
    (compile(r':'), DELIMITER),

    (compile(r'\s+'), None)
)


def remove_comment(line):
    comment = line.find("#")

    if comment == -1:
        return line

    return line[:comment]


def remove_comments(text):
    lines = text.split("\n")

    return '\n'.join(remove_comment(line) for line in lines)


def lex(text):
    text = remove_comments(text)

    found = []
    pos = 0

    match = None

    while pos < len(text):
        for parser, label in tokens:
            if callable(parser):
                is_parsed, data = parser(text, pos)

                if not is_parsed:
                    continue

                pos += len(data)+1
                match = True

                found.append((data, label))

                break

            match = parser.match(text, pos)

            if match is not None:
                pos = match.end(0)

                if label is None:
                    break

                found.append((match.group(0), label))

        if not match:
            raise SyntaxError("Unexpected character %r on line %d:%d" % (
                text[pos], count_lines(text[:pos]), pos
            ))

    return found

