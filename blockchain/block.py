import struct
from typing import Sequence


def varint(data: memoryview, offset: int) -> (int, int):
    # variable length integer
    # 1 byte unsigned int8
    value, = struct.unpack('<B', data[offset:offset + 1])
    bytes_consumed = 1

    if value < 253:
        pass
    elif value == 253:
        # 2 bytes unsigned int16
        value, = struct.unpack('<H', data[offset + 1:offset + 3])
        bytes_consumed += 2
    elif value == 254:
        # 4 bytes unsigned int32
        value, = struct.unpack('<I', data[offset + 1:offset + 5])
        bytes_consumed += 4
    elif value == 255:
        # 8 bytes unsigned int64
        value, = struct.unpack('<Q', data[offset + 1:offset + 9])
        bytes_consumed += 8
    return value, bytes_consumed


class BlockHeader(object):
    __slots__ = [
        'magic_number',
        'block_size',
        'version',
        'previous_hash',
        'merkle_hash',
        'time',
        'bits',
        'nonce',
    ]

    def __init__(
            self,
            magic_number: int,
            block_size: int,
            version: int,
            previous_hash: bytes,
            merkle_hash: bytes,
            time: int,
            bits: int,
            nonce: int,
    ):
        self.magic_number = magic_number
        self.block_size = block_size
        self.version = version
        self.previous_hash = previous_hash
        self.merkle_hash = merkle_hash
        self.time = time
        self.bits = bits
        self.nonce = nonce

    @classmethod
    def from_binary_data(
            cls,
            data: memoryview,
    ):
        # unsigned int32 version
        # 32 bytes of previous hash
        # 32 bytes of merkle hash
        # unsigned int32 time
        # unsigned int32 bits
        # unsigned int32 nonce
        tup = struct.unpack('<III32s32sIII', data)
        return cls(*tup)

    @property
    def magic_number_hex(self) -> str:
        return '{:02x}'.format(self.magic_number)


class TransactionInput(object):
    __slots__ = ['prev_hash', 'txn_out_id', 'script_sig', 'seq_no']

    def __init__(
            self,
            prev_hash: bytes,
            txn_out_id: int,
            script_sig: bytes,
            seq_no: int,
    ):
        self.prev_hash = prev_hash
        self.txn_out_id = txn_out_id
        self.script_sig = script_sig
        self.seq_no = seq_no

    @classmethod
    def from_binary_data(
            cls,
            data: memoryview,
            offset: int,
    ):
        prev_hash, txn_out_id = struct.unpack(
            '<32sI',
            data[offset:offset + 36]
        )
        offset += 36

        script_length, bytes_consumed = varint(data, offset=offset)
        offset += bytes_consumed

        script_sig, seq_no = struct.unpack(
            '<{}sI'.format(script_length),
            data[offset:offset + script_length + 4]
        )
        offset += script_length + 4

        return cls(prev_hash, txn_out_id, script_sig, seq_no), offset


class TransactionOutput(object):
    __slots__ = ['value', 'public_key']

    def __init__(
            self,
            value: int,
            public_key: bytes,
    ):
        self.value = value
        self.public_key = public_key

    @classmethod
    def from_binary_data(
            cls,
            data: memoryview,
            offset: int,
    ):
        value, = struct.unpack('<Q', data[offset:offset + 8])
        offset += 8

        public_key_length, bytes_consumed = varint(data, offset=offset)
        offset += bytes_consumed

        public_key, = struct.unpack(
            '<{}s'.format(public_key_length),
            data[offset:offset + public_key_length]
        )
        offset += public_key_length

        return cls(value, public_key), offset


class Transaction(object):
    __slots__ = ['version', 'inputs', 'outputs', 'lock_time']

    def __init__(
            self,
            version: int,
            inputs: Sequence[TransactionInput],
            outputs: Sequence[TransactionOutput],
            lock_time: int,
    ):
        self.version = version
        self.inputs = inputs
        self.outputs = outputs
        self.lock_time = lock_time

    @classmethod
    def from_binary_data(
            cls,
            data: memoryview,
            offset: int,
    ):
        version, = struct.unpack('<I', data[offset:offset + 4])
        offset += 4

        # Input transactions
        txn_input_count, bytes_consumed = varint(data, offset=offset)
        offset += bytes_consumed

        txn_input_list = []
        for i in range(txn_input_count):
            txn_input, new_offset = TransactionInput.from_binary_data(
                data,
                offset=offset,
            )
            offset = new_offset
            txn_input_list.append(txn_input)

        # Output transactions
        txn_output_count, bytes_consumed = varint(data, offset=offset)
        offset += bytes_consumed

        txn_output_list = []
        for i in range(txn_output_count):
            txn_output, new_offset = TransactionOutput.from_binary_data(
                data,
                offset=offset,
            )
            offset = new_offset
            txn_output_list.append(txn_output)

        lock_time, = struct.unpack('<I', data[offset:offset + 4])
        offset += 4

        return cls(version, txn_input_list, txn_output_list, lock_time), offset


class Block(object):
    __slots__ = ['header', 'transactions']

    def __init__(
            self,
            header: BlockHeader,
            transactions: Sequence[Transaction],
    ):
        self.header = header
        self.transactions = transactions

    @classmethod
    def from_binary_data(
            cls,
            block_data: memoryview,
            offset: int,
    ):
        header_data = block_data[offset:offset + 88]
        header = BlockHeader.from_binary_data(header_data)
        offset += 88

        txn_count, bytes_consumed = varint(block_data, offset=offset)
        offset += bytes_consumed

        txns = []
        for i in range(txn_count):
            txn, new_offset = Transaction.from_binary_data(
                block_data,
                offset=offset
            )
            offset = new_offset

            txns.append(txn)

        return cls(header, txns)
