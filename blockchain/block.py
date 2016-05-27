from hashlib import sha256
import struct


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
            magic_number,
            block_size,
            version,
            previous_hash,
            merkle_hash,
            time,
            bits,
            nonce,
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
    def from_binary_data(cls, data):
        # unsigned int 4 bytes version
        # 32 bytes of previous hash
        # 32 byres of merkle hash
        # unsigned int 4 bytes time
        # unsigned int 4 bytes of bits
        # unsigned int 4 bytes of nonce
        tup = struct.unpack('<III32s32sIII', data)
        return cls(*tup)

    @property
    def magic_number_hex(self):
        return '{:02x}'.format(self.magic_number)


class Block(object):
    def __init__(self, block_data):
        self.txn_count = 0
        self.txns = []

        header_data = block_data[:88]
        self.header = BlockHeader.from_binary_data(header_data)

        # body data - already consumed header part
        body_size = self.header.block_size - 80
        body_data = block_data[88:body_size]

    def consume_body_data(self, data):
        pass
