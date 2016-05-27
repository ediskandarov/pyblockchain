import os
import mmap

from blockchain.block import Block

blockchain_path = os.path.join(os.path.dirname(__file__), '1M.dat')

def test_genesis_block_headers():
    """https://en.bitcoin.it/wiki/Genesis_block"""

    with open(blockchain_path, 'rb') as f:
        # Map for 8MB block size
        blockchain_mmap = mmap.mmap(
            f.fileno(),
            8 * 1024,
            access=mmap.ACCESS_READ
        )
        blockchain_mview = memoryview(blockchain_mmap)
        block = Block(blockchain_mview)

    assert block.header.magic_number_hex == 'd9b4bef9'
    assert block.header.block_size == 285
    assert block.header.version == 1
    assert block.header.previous_hash.hex() == (
        '0000000000000000000000000000000000000000000000000000000000000000'
    )
    assert block.header.merkle_hash.hex() == (
        '3ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a9fb8aa4b1e5e4a'
    )
    assert block.header.time == 1231006505
    assert '{:02x}'.format(block.header.bits) == '1d00ffff'
    assert block.header.nonce == 2083236893
