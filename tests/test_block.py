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


@pytest.fixture
def block_170():
    """Block #170 is the first block with 2 transactions"""
    block_170_hex = (
        'f9beb4d9ea0100000100000055bd840a78798ad0da853f68974f3d183e2bd1db6a842'
        'c1feecf222a00000000ff104ccb05421ab93e63f8c3ce5c2c2e9dbb37de2764b3a317'
        '5c8166562cac7d51b96a49ffff001d283e9e700201000000010000000000000000000'
        '000000000000000000000000000000000000000000000ffffffff0704ffff001d0102'
        'ffffffff0100f2052a01000000434104d46c4968bde02899d2aa0963367c7a6ce34ee'
        'c332b32e42e5f3407e052d64ac625da6f0718e7b302140434bd725706957c092db538'
        '05b821a85b23a7ac61725bac000000000100000001c997a5e56e104102fa209c6a852'
        'dd90660a20b2d9c352423edce25857fcd3704000000004847304402204e45e16932b8'
        'af514961a1d3a1a25fdf3f4f7732e9d624c6c61548ab5fb8cd410220181522ec8eca0'
        '7de4860a4acdd12909d831cc56cbbac4622082221a8768d1d0901ffffffff0200ca9a'
        '3b00000000434104ae1a62fe09c5f51b13905f07f06b99a2f7159b2225f374cd378d7'
        '1302fa28414e7aab37397f554a7df5f142c21c1b7303b8a0626f1baded5c72a704f7e'
        '6cd84cac00286bee0000000043410411db93e1dcdb8a016b49840f8c53bc1eb68a382'
        'e97b1482ecad7b148a6909a5cb2e0eaddfb84ccf9744464f82e160bfa9b8b64f9d4c0'
        '3f999b8643f656b412a3ac00000000'
    )
    return bytes.fromhex(block_170_hex)


def test_genesis_block(genesis_block):
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
    assert block.hashcash == (
        '000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f'
    )

    assert len(block.transactions) == 1

    # NOQA https://blockchain.info/tx/4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b
    txn = block.transactions[0]
    assert txn.version == 1
    assert len(txn.inputs) == 1
    assert txn.lock_time == datetime(1970, 1, 1, 0, 0)

    txn_input = txn.inputs[0]
    assert txn_input.is_coinbase
    assert txn_input.previous_hash == (
        '0000000000000000000000000000000000000000000000000000000000000000'
    )

    assert txn_input.seq_no == 0xffffffff
    assert txn_input.txn_out_id == 0xffffffff
    assert txn_input.signature_script.hex() == (
        '04ffff001d0104455468652054696d65732030332f4a616e2f32303039204368616e6'
        '3656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f75742066'
        '6f722062616e6b73'
    )
    assert txn_input.signature_script.endswith(
        b'The Times 03/Jan/2009 Chancellor on '
        b'brink of second bailout for banks'
    )

    assert len(txn.outputs) == 1
    txn_output = txn.outputs[0]
    assert txn_output.is_coinbase
    assert txn_output.value == 50 * (10 ** 8)
    assert txn_output.script_pub_key.hex() == (
        '4104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb'
        '649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac'
    )
    assert txn_output.address == '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'


def test_block_170(block_170):
    blockchain_mview = memoryview(block_170)
    block = Block.from_binary_data(blockchain_mview, offset=0)

    assert block.header.magic_number == Network.mainnet.value
    assert block.header.block_size == 490
    assert block.header.version == 1
    assert block.header.previous_hash == (
        '000000002a22cfee1f2c846adbd12b3e183d4f97683f85dad08a79780a84bd55'
    )
    assert block.header.merkle_hash == (
        '7dac2c5666815c17a3b36427de37bb9d2e2c5ccec3f8633eb91a4205cb4c10ff'
    )
    assert block.header.time == datetime(2009, 1, 12, 3, 30, 25)
    assert block.header.bits == 486604799
    assert block.header.bits == 0x1d00ffff
    assert block.header.nonce == 1889418792

    assert block.total_size == 498
    assert block.hashcash == (
        '00000000d1145790a8694403d4063f323d499e655c83426834d4ce2f8dd4a2ee'
    )

    assert len(block.transactions) == 2

    coinbase_txn = block.transactions[0]
    assert coinbase_txn.version == 1
    assert len(coinbase_txn.inputs) == 1
    assert coinbase_txn.lock_time == datetime(1970, 1, 1, 0, 0)

    coinbase_txn_input = coinbase_txn.inputs[0]
    assert coinbase_txn_input.previous_hash == (
        '0000000000000000000000000000000000000000000000000000000000000000'
    )

    assert coinbase_txn_input.seq_no == 0xffffffff
    assert coinbase_txn_input.txn_out_id == 0xffffffff
    assert coinbase_txn_input.signature_script.hex() == (
        '04ffff001d0102'
    )

    assert len(coinbase_txn.outputs) == 1
    coinbase_txn_output = coinbase_txn.outputs[0]
    assert coinbase_txn_output.value == 50 * (10 ** 8)
    assert coinbase_txn_output.script_pub_key.hex() == (
        '4104d46c4968bde02899d2aa0963367c7a6ce34eec332b32e42e5f3407e052d64ac'
        '625da6f0718e7b302140434bd725706957c092db53805b821a85b23a7ac61725bac'
    )

    real_txn = block.transactions[1]
    assert real_txn.version == 1
    assert len(real_txn.inputs) == 1
    assert real_txn.lock_time == datetime(1970, 1, 1, 0, 0)

    real_txn_input = real_txn.inputs[0]
    assert real_txn_input.previous_hash == (
        '0437cd7f8525ceed2324359c2d0ba26006d92d856a9c20fa0241106ee5a597c9'
    )
    assert real_txn_input.txn_out_id == 0
    assert real_txn_input.signature_script.hex() == (
        '47304402204e45e16932b8af514961a1d3a1a25fdf3f4f7732e9d624c6c61548ab5fb'
        '8cd410220181522ec8eca07de4860a4acdd12909d831cc56cbbac4622082221a8768d'
        '1d0901'
    )

    assert len(real_txn.outputs) == 2
    real_txn_output1 = real_txn.outputs[0]
    assert real_txn_output1.value == 10 * (10 ** 8)
    # TODO
    # assert real_txn_output1.script_pub_key.hex() == ''

    real_txn_output2 = real_txn.outputs[1]
    assert real_txn_output2.value == 40 * (10 ** 8)
    # TODO
    # assert real_txn_output2.script_pub_key == b''
