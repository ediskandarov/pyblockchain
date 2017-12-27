import mmap
import struct

from .block import Block


class BlockchainFileReader(object):
    def __init__(self, file_name):
        self._file_name = file_name

    def __iter__(self):
        """TODO: Possibly inefficient implementation."""
        with open(self._file_name, 'rb') as f:
            # Map for 8MB block size
            mmap_length = 0
            blockchain_mmap = mmap.mmap(
                f.fileno(),
                mmap_length,
                access=mmap.ACCESS_READ,
            )
            file_size = blockchain_mmap.size()
            offset = 0
            # linit - 8 MB
            limit = 8 * 1024 * 1024
            while offset < file_size:
                # TODO: no need in memory view?
                blockchain_mview = memoryview(
                    blockchain_mmap[offset:offset + limit]
                )
                try:
                    block = Block.from_binary_data(blockchain_mview, offset=0)
                except struct.error as err:
                    print('Current mmap position: ', blockchain_mmap.tell())
                    print('Total mmap size: ', blockchain_mmap.size())
                    raise err
                yield block
                offset += block.total_size
                blockchain_mmap.seek(block.total_size)
            blockchain_mmap.close()
