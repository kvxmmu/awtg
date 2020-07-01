from rapidjson import (loads, dumps,
                       JSONDecodeError)

from struct import pack, unpack
from base64 import b64decode, b64encode
from binascii import Error as BinasciiError


INTEGER_TYPE = 0x1
STRING_TYPE = 0x2
BYTES_TYPE = 0x3
NESTED_TYPE = 0x4


class CustomJsonRPC:
    """
        RPC scheme:
            {
                "procedure": procedure_name,
                "args": {
                    // data
                }
            }
    """

    def __init__(self, procedure_name):
        self.reaction_procedure = procedure_name

    def __call__(self, callback):
        data = callback.data.get_data()

        try:
            data = loads(data)
        except JSONDecodeError:
            return False

        if 'procedure' not in data or 'args' not in data:
            return False

        match = data['procedure'] == self.reaction_procedure

        if match:
            callback.memory['cjsonrpc_args'] = data['args']

        return match


class CustomBinRPC:
    """
        RPC scheme:
            procedure_length - 2 bytes unsigned
            procedure - n bytes

            key_length - 2 bytes unsigned
            value_length - 2 bytes unsigned
            value_type - 1 byte unsigned

            key - n bytes
            value - n bytes

            value types:
                integer type - 0x1
                string type - 0x2
                bytes type - 0x3
                nested scheme - 0x4
    """

    def __init__(self, procedure_reaction):
        self.procedure_reaction = procedure_reaction

    @staticmethod
    def parse(data,
              header_parsing=True):
        procedure_name = None

        bin_data = data

        if header_parsing:

            try:
                bin_data = b64decode(data)
            except BinasciiError:
                return

            procedure_length, = unpack('<H', bin_data[:2])

            try:
                procedure_name = bin_data[2:procedure_length+2].decode()
            except UnicodeDecodeError:
                return

            bin_data = bin_data[2+procedure_length:]

        args = {}

        while bin_data:
            try:
                (key_length, value_length,
                 value_type) = unpack("<HHB", bin_data[:5])
            except ValueError:
                return

            bin_data = bin_data[5:]

            try:
                key = bin_data[:key_length].decode()
            except UnicodeDecodeError:
                return

            bin_data = bin_data[key_length:]
            value = bin_data[:value_length]
            bin_data = bin_data[key_length:]

            if value_type == 0x1:
                value = int.from_bytes(value, 'little')
            elif value_type == 0x2:
                try:
                    value = value.decode()
                except UnicodeDecodeError:
                    return
            elif value_type == 0x4:
                value = CustomBinRPC.parse(value, False)
            elif value_type != 0x3:
                return

            args[key] = value

            bin_data = bin_data[value_length+key_length:]

        if header_parsing:
            return args, procedure_name

        return args

    def __call__(self, callback):
        response = self.parse(callback.data.get_data())

        if response is None:
            return False

        args, procedure_name = response

        callback.memory['cbinrpc_args'] = args

        return True


def build_cjsonrpc_procedure(procedure_name, **args):
    procedure = {'procedure': procedure_name, "args": args}

    return dumps(procedure)


def determine_and_encode(value):
    if isinstance(value, int):
        return INTEGER_TYPE, pack("<I", value), 4
    elif isinstance(value, str):
        return STRING_TYPE, value.encode()
    elif isinstance(value, bytes):
        return BYTES_TYPE, value
    elif isinstance(value, dict):
        value = encode_kv_container(value)

        return NESTED_TYPE, value, len(value)

    raise ValueError('Unknown value type')


def encode_kv_container(args):
    data = b''

    for key, value in args.items():
        typeid, encoded_value, *length = determine_and_encode(value)

        header = pack("<HHB", len(key), length[0] if length else len(value), typeid)+key.encode()

        data += header+encoded_value

    return data


def build_cbinrpc_procedure(procedure_name, **args):
    header = pack("<H", len(procedure_name))+procedure_name.encode()

    return b64encode(header+encode_kv_container(args))
