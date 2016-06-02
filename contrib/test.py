from blockchain.reader import BlockchainFileReader


def main():
    block_reader = BlockchainFileReader('tests/1M.dat')
    total_consumed = 0
    for i, block in enumerate(block_reader):
        total_consumed += block.header.block_size + 8
        print(i)
        print('magic number', block.header.magic_number_hex)
        print('previous hash', block.header.previous_hash.hex())
        print('merkle hash', block.header.merkle_hash.hex())
        print('total consumed', total_consumed)


if __name__ == '__main__':
    main()
