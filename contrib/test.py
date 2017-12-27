from blockchain.reader import BlockchainFileReader


def main():
    block_reader = BlockchainFileReader('blk00000.dat')
    total_consumed = 0
    for i, block in enumerate(block_reader):
        total_consumed += block.header.block_size + 8
        print(i)
        print('magic number', block.header.magic_number)
        print('previous hash', block.header.previous_hash)
        print('merkle hash', block.header.merkle_hash)
        print('total consumed', total_consumed)
        print('total transactions', len(block.transactions))


if __name__ == '__main__':
    main()
