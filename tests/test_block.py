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
        block = Block.from_binary_data(blockchain_mview, offset=0)

    assert block.header.magic_number_hex == 'd9b4bef9'
    assert block.header.block_size == 285
    assert block.header.version == 1
    assert block.header.previous_hash == (
        '0000000000000000000000000000000000000000000000000000000000000000'
    )
    assert block.header.merkle_hash == (
        '4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b'
    )
    assert block.header.time == 1231006505
    assert '{:02x}'.format(block.header.bits) == '1d00ffff'
    assert block.header.nonce == 2083236893

    assert block.total_size == 293

    assert len(block.transactions) == 1

    txn = block.transactions[0]
    assert txn.version == 1
    assert len(txn.inputs) == 1
    assert txn.lock_time == 0

    txn_input = txn.inputs[0]
    assert txn_input.prev_hash.hex() == (
        '0000000000000000000000000000000000000000000000000000000000000000'
    )
    assert '{:02x}'.format(txn_input.seq_no) == 'ffffffff'
    assert txn_input.txn_out_id == 4294967295
    assert txn_input.script_sig.endswith(
        b'The Times 03/Jan/2009 Chancellor on '
        b'brink of second bailout for banks'
    )

    assert len(txn.outputs) == 1
    txn_output = txn.outputs[0]
    assert txn_output.value == 50 * (10 ** 8)
    assert txn_output.public_key.hex() == (
        '4104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb'
        '649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac'
    )
