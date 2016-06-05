"""
According to https://bitcoin.org/en/developer-reference#block-headers

> The hashes are in internal byte order; the other values are all in
  little-endian order.

"""
from datetime import datetime
import struct
from typing import Sequence


def varint(data: memoryview, offset: int) -> (int, int):
    """The raw transaction format and several peer-to-peer network messages use
    a type of variable-length integer to indicate the number of bytes in a
    following piece of data.

    Reference:
    https://bitcoin.org/en/developer-reference#compactsize-unsigned-integers

    """
    # variable length integer
    # 1 byte unsigned int8
    value, = struct.unpack_from('<B', data, offset=offset)
    offset += struct.calcsize('<B')

    if value < 253:
        pass
    elif value == 0xfd:
        # 0xfd followed by the number as uint16_t
        value, = struct.unpack_from('<H', data, offset=offset)
        offset += struct.calcsize('<H')
    elif value == 0xfe:
        # 0xfe followed by the number as uint32_t
        value, = struct.unpack_from('<I', data, offset=offset)
        offset += struct.calcsize('<I')
    elif value == 255:
        # 0xff followed by the number as uint64_t
        value, = struct.unpack_from('<Q', data, offset=offset)
        offset += struct.calcsize('<Q')
    return value, offset


class BlockHeader(object):
    """Block headers are serialized in the 80-byte format described below and
    then hashed as part of Bitcoin’s proof-of-work algorithm, making the
    serialized header format part of the consensus rules.

    Reference:
    https://bitcoin.org/en/developer-reference#block-headers

    """
    __slots__ = [
        'magic_number',
        'block_size',
        'version',
        'previous_hash_raw',
        'merkle_hash_raw',
        'timestamp',
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
            timestamp: int,
            bits: int,
            nonce: int,
    ):
        """
        :param version: The block version number indicates which set of block
            validation rules to follow.
        :param previous_hash: A SHA256(SHA256()) hash in internal byte order of
             the previous block’s header. This ensures no previous block can be
             changed without also changing this block’s header.
        :param merkle_hash: A SHA256(SHA256()) hash in internal byte order. The
            merkle root is derived from the hashes of all transactions included
            in this block, ensuring that none of those transactions can be
            modified without modifying the header.
        :param timestamp: The block time is a Unix epoch time when the miner
            started hashing the header (according to the miner).
        :param bits: An encoded version of the target threshold this block’s
            header hash must be less than or equal to.
        :param nonce: An arbitrary number miners change to modify the header
            hash in order to produce a hash below the target threshold.

        """
        self.magic_number = magic_number
        self.block_size = block_size
        self.version = version
        self.previous_hash_raw = previous_hash
        self.merkle_hash_raw = merkle_hash
        self.timestamp = timestamp
        self.bits = bits
        self.nonce = nonce

    @property
    def time(self):
        return datetime.utcfromtimestamp(self.timestamp)

    @property
    def previous_hash(self):
        return self.previous_hash_raw[::-1].hex()

    @property
    def merkle_hash(self):
        return self.merkle_hash_raw[::-1].hex()

    @classmethod
    def from_binary_data(
            cls,
            data: memoryview,
            offset: int,
    ):
        # unsigned int32 version
        # 32 bytes of previous hash
        # 32 bytes of merkle hash
        # unsigned int32 time
        # unsigned int32 bits
        # unsigned int32 nonce
        header_fmt = '<III32s32sIII'
        tup = struct.unpack_from(header_fmt, data, offset=offset)

        offset += struct.calcsize(header_fmt)

        return cls(*tup), offset


class TransactionInput(object):
    """The first transaction in a block, called the coinbase transaction, must
    have exactly one input, called a coinbase. The coinbase input currently has
    the following format.

    Reference:
    https://bitcoin.org/en/developer-reference#coinbase

    """
    __slots__ = [
        'previous_hash_raw',
        'txn_out_id',
        'signature_script',
        'seq_no',
    ]

    def __init__(
            self,
            previous_hash: bytes,
            txn_out_id: int,
            signature_script: bytes,
            seq_no: int,
    ):
        """
        :param previous_hash: The previous outpoint being spent.
        :txn_out_id: 0xffffffff, as a coinbase has no previous outpoint.
        :param signature_script: A script-language script which satisfies the
            conditions placed in the outpoint’s pubkey script.
        :param seq_no: Sequence number. Default for Bitcoin Core and almost all
            other programs is 0xffffffff.

        """
        self.previous_hash_raw = previous_hash
        self.txn_out_id = txn_out_id
        self.signature_script = signature_script
        self.seq_no = seq_no

    @property
    def previous_hash(self):
        return self.previous_hash_raw[::-1].hex()

    @classmethod
    def from_binary_data(
            cls,
            data: memoryview,
            is_coinbase: bool,
            offset: int,
    ):
        if is_coinbase:
            # The first transaction in a block, called the coinbase
            # transaction, must have exactly one input, called a coinbase.
            #
            # Reference:
            # https://bitcoin.org/en/developer-reference#coinbase
            prev_hash_txn_out_id_fmt = '<32sI'
            prev_hash, txn_out_id = struct.unpack_from(
                prev_hash_txn_out_id_fmt,
                data,
                offset=offset
            )
        else:
            # Each non-coinbase input spends an outpoint from a previous
            # transaction.
            #
            # Reference:
            # https://bitcoin.org/en/developer-reference#txin
            prev_hash_txn_out_id_fmt = '<36s'
            prev_hash, = struct.unpack_from(
                prev_hash_txn_out_id_fmt,
                data,
                offset=offset
            )
            txn_out_id = None
        offset += struct.calcsize(prev_hash_txn_out_id_fmt)

        script_length, offset = varint(data, offset=offset)

        script_sig_seq_no_fmt = '<{}sI'.format(script_length)
        script_sig, seq_no = struct.unpack_from(
            script_sig_seq_no_fmt,
            data,
            offset=offset
        )
        offset += struct.calcsize(script_sig_seq_no_fmt)

        return cls(prev_hash, txn_out_id, script_sig, seq_no), offset


class TransactionOutput(object):
    """Each output spends a certain number of satoshis, placing them under
    control of anyone who can satisfy the provided pubkey script.

    Reference:
    https://bitcoin.org/en/developer-reference#txout

    """
    __slots__ = ['value', 'script_pub_key']

    def __init__(
            self,
            value: int,
            script_pub_key: bytes,
    ):
        """
        :param value: Number of satoshis to spend. May be zero; the sum of all
            outputs may not exceed the sum of satoshis previously spent to the
            outpoints provided in the input section.
        :param script_pub_key: Defines the conditions which must be satisfied
            to spend this output.

        """
        self.value = value
        self.script_pub_key = script_pub_key

    @classmethod
    def from_binary_data(
            cls,
            data: memoryview,
            offset: int,
    ):
        value_fmt = '<q'
        value, = struct.unpack_from(value_fmt, data, offset=offset)
        offset += struct.calcsize(value_fmt)

        public_key_length, offset = varint(data, offset=offset)

        public_key_fmt = '<{}s'.format(public_key_length)
        public_key, = struct.unpack_from(public_key_fmt, data, offset=offset)
        offset += struct.calcsize(public_key_fmt)

        return cls(value, public_key), offset


class Transaction(object):
    """Bitcoin transactions are broadcast between peers in a serialized byte
    format, called raw format. It is this form of a transaction which is
    SHA256(SHA256()) hashed to create the TXID and, ultimately, the merkle root
    of a block containing the transaction—making the transaction format part of
    the consensus rules.

    Reference:
    https://bitcoin.org/en/developer-reference#raw-transaction-format

    """
    __slots__ = ['version', 'inputs', 'outputs', 'lock_timestamp']

    def __init__(
            self,
            version: int,
            inputs: Sequence[TransactionInput],
            outputs: Sequence[TransactionOutput],
            lock_timestamp: int,
    ):
        """
        :param version: Transaction version number; currently version 1.
            Programs creating transactions using newer consensus rules may use
            higher version numbers.
        :param inputs: Transaction inputs.
        :param outputs: Transaction outputs.
        :param lock_time: A time (Unix epoch time) or block number.

        """
        self.version = version
        self.inputs = inputs
        self.outputs = outputs
        self.lock_timestamp = lock_timestamp

    @property
    def lock_time(self):
        return datetime.utcfromtimestamp(self.lock_timestamp)

    @classmethod
    def from_binary_data(
            cls,
            data: memoryview,
            txn_index: int,
            offset: int,
    ):
        version_fmt = '<I'
        version, = struct.unpack_from(version_fmt, data, offset=offset)
        offset += struct.calcsize(version_fmt)

        # Input transactions
        txn_input_count, offset = varint(data, offset=offset)

        # The first transaction in a block, called the coinbase
        # transaction, must have exactly one input, called a coinbase.
        is_coinbase = txn_index == 0

        txn_input_list = []
        for i in range(txn_input_count):
            txn_input, offset = TransactionInput.from_binary_data(
                data,
                is_coinbase=is_coinbase,
                offset=offset,
            )
            txn_input_list.append(txn_input)

        # Output transactions
        txn_output_count, offset = varint(data, offset=offset)

        txn_output_list = []
        for i in range(txn_output_count):
            txn_output, offset = TransactionOutput.from_binary_data(
                data,
                offset=offset,
            )
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

    @property
    def total_size(self):
        # block size + 4 bytes magic number + 4 bytes block size
        return self.header.block_size + 8

    @classmethod
    def from_binary_data(
            cls,
            block_data: memoryview,
            offset: int,
    ):
        header, offset = BlockHeader.from_binary_data(
            block_data,
            offset=offset,
        )

        txn_count, offset = varint(block_data, offset=offset)

        transaction_list = []
        for i in range(txn_count):
            transaction, offset = Transaction.from_binary_data(
                block_data,
                txn_index=i,
                offset=offset,
            )
            transaction_list.append(transaction)

        return cls(header, transaction_list)
