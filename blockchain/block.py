import struct
from typing import Sequence


def varint(data: memoryview, offset: int) -> (int, int):
    # variable length integer
    # 1 byte unsigned int8
    value, = struct.unpack_from('<B', data, offset=offset)
    bytes_consumed = struct.calcsize('<B')
    offset += bytes_consumed

    if value < 253:
        pass
    elif value == 253:
        # 2 bytes unsigned int16
        value, = struct.unpack_from('<H', data, offset=offset)
        bytes_consumed += struct.calcsize('<H')
    elif value == 254:
        # 4 bytes unsigned int32
        value, = struct.unpack_from('<I', data, offset=offset)
        bytes_consumed += struct.calcsize('<I')
    elif value == 255:
        # 8 bytes unsigned int64
        value, = struct.unpack_from('<Q', data, offset=offset)
        bytes_consumed += struct.calcsize('<Q')
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
        tup = struct.unpack_from('<III32s32sIII', data)
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
        prev_hash_txn_out_id_fmt = '<32sI'
        prev_hash, txn_out_id = struct.unpack_from(
            prev_hash_txn_out_id_fmt,
            data,
            offset=offset
        )
        offset += struct.calcsize(prev_hash_txn_out_id_fmt)

        script_length, bytes_consumed = varint(data, offset=offset)
        offset += bytes_consumed

        script_sig_seq_no_fmt = '<{}sI'.format(script_length)
        script_sig, seq_no = struct.unpack_from(
            script_sig_seq_no_fmt,
            data,
            offset=offset
        )
        offset += struct.calcsize(script_sig_seq_no_fmt)

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
        value_fmt = '<Q'
        value, = struct.unpack_from(value_fmt, data, offset=offset)
        offset += struct.calcsize(value_fmt)

        public_key_length, bytes_consumed = varint(data, offset=offset)
        offset += bytes_consumed

        public_key_fmt = '<{}s'.format(public_key_length)
        public_key, = struct.unpack_from(public_key_fmt, data, offset=offset)
        offset += struct.calcsize(public_key_fmt)

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
        version_fmt = '<I'
        version, = struct.unpack_from(version_fmt, data, offset=offset)
        offset += struct.calcsize(version_fmt)

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

        lock_time_fmt = '<I'
        lock_time, = struct.unpack_from(version_fmt, data, offset=offset)
        offset += struct.calcsize(lock_time_fmt)

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
