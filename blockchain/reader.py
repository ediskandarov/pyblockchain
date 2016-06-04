import mmap
import struct

from .block import Block


class BlockchainFileReader(object):
    def __init__(self, file_name):
        self._file_name = file_name

    def __iter__(self):
        with open(self._file_name, 'rb') as f:
            # Map for 8MB block size
            blockchain_mmap = mmap.mmap(
                f.fileno(),
                8 * 1024,
                access=mmap.ACCESS_READ,
            )

            offset = 0
            limit = 4096
            while True:
                # TODO: no need in memory view?
                blockchain_mview = memoryview(
                    blockchain_mmap[offset:offset + limit]
                )
                try:
                    block = Block.from_binary_data(blockchain_mview, offset=0)
                except struct.error:
                    break
                yield block
                offset += block.total_size

            blockchain_mmap.close()
