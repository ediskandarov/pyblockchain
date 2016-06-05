from enum import Enum


class Network(Enum):
    """
    Reference:
    https://github.com/bitcoin/bitcoin/blob/master/src/chainparams.cpp

    """
    mainnet = 0xd9b4bef9
    testnet = 0x0709110b
    regtest = 0xdab5bffa
