============
pyblockchain
============

.. image:: https://img.shields.io/pypi/v/pyblockchain.svg
   :target: http://pypi.python.org/pypi/pyblockchain
.. image:: https://travis-ci.org/toidi/pyblockchain.svg?branch=master
   :target: https://travis-ci.org/toidi/pyblockchain

pyblockchain is a Python library for parsing blockchain data


Installation
============

::

   pip install pyblockchain


Usage
=====

.. code-block:: python

   from blockchain.reader import BlockchainFileReader

   block_reader = BlockchainFileReader('tests/1M.dat')

   for block in block_reader:
       print('magic number', block.header.magic_number_hex)


Useful links
============

* `Bitcoin Developer Guide`_
* `Bitcoin Developer Reference`_
* `Block Parser for Bitcoin`_
* `How to Program Block Chain Explorers with Python`_
* `Genesis block`_
* `Transaction`_
* `Technical background of version 1 Bitcoin addresses`_
* `Block hashing algorithm`_
* `Blockchain.info Block #0`_
* `Script opcodes`_
* `Parsing the Bitcoin Blockchain`_

.. _Block Parser for Bitcoin: https://github.com/tenthirtyone/blocktools
.. _How to Program Block Chain Explorers with Python: http://alexgorale.com/how-to-program-block-chain-explorers-with-python-part-1
.. _Genesis block: https://en.bitcoin.it/wiki/Genesis_block
.. _Transaction: https://en.bitcoin.it/wiki/Transaction
.. _Block hashing algorithm : https://en.bitcoin.it/wiki/Block_hashing_algorithm
.. _Blockchain.info Block #0: https://blockchain.info/block/000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f
.. _Bitcoin Developer Guide: https://bitcoin.org/en/developer-guide
.. _Bitcoin Developer Reference: https://bitcoin.org/en/developer-reference
.. _script opcodes: https://github.com/bitcoin/bitcoin/blob/0.12/src/script/script.h
.. _Technical background of version 1 Bitcoin addresses: https://en.bitcoin.it/wiki/Technical_background_of_version_1_Bitcoin_addresses
.. _Parsing the Bitcoin Blockchain: http://blog.gebhartom.com/posts/Parsing%20the%20Bitcoin%20Blockchain
