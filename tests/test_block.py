from datetime import datetime

import pytest

from blockchain.block import Block
from blockchain.constants import Network


@pytest.fixture
def genesis_block():
    """https://en.bitcoin.it/wiki/Genesis_block"""
    genesis_block_hex = (
        'f9beb4d91d01000001000000000000000000000000000000000000000000000000000'
        '00000000000000000003ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a'
        '9fb8aa4b1e5e4a29ab5f49ffff001d1dac2b7c0101000000010000000000000000000'
        '000000000000000000000000000000000000000000000ffffffff4d04ffff001d0104'
        '455468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206'
        'f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b'
        '73ffffffff0100f2052a01000000434104678afdb0fe5548271967f1a67130b7105cd'
        '6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7'
        'ba0b8d578a4c702b6bf11d5fac00000000'
    )
    return bytes.fromhex(genesis_block_hex)


def test_genesis_block_headers(genesis_block):
    blockchain_mview = memoryview(genesis_block)
    block = Block.from_binary_data(blockchain_mview, offset=0)

    assert block.header.magic_number == Network.mainnet.value
    assert block.header.block_size == 285
    assert block.header.version == 1
    assert block.header.previous_hash == (
        '0000000000000000000000000000000000000000000000000000000000000000'
    )
    assert block.header.merkle_hash == (
        '4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b'
    )
    assert block.header.time == datetime(2009, 1, 3, 18, 15, 5)
    assert block.header.bits == 486604799
    assert block.header.bits == 0x1d00ffff
    assert block.header.nonce == 2083236893

    assert block.total_size == 293

    assert len(block.transactions) == 1

    txn = block.transactions[0]
    assert txn.version == 1
    assert len(txn.inputs) == 1
    assert txn.lock_time == datetime(1970, 1, 1, 0, 0)

    txn_input = txn.inputs[0]
    assert txn_input.previous_hash == (
        '0000000000000000000000000000000000000000000000000000000000000000'
    )

    assert txn_input.seq_no == 0xffffffff
    assert txn_input.txn_out_id == 0xffffffff
    assert txn_input.signature_script.endswith(
        b'The Times 03/Jan/2009 Chancellor on '
        b'brink of second bailout for banks'
    )

    assert len(txn.outputs) == 1
    txn_output = txn.outputs[0]
    assert txn_output.value == 50 * (10 ** 8)
    assert txn_output.script_pub_key.hex() == (
        '4104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb'
        '649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac'
    )
