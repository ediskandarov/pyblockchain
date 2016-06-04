============
pyblockchain
============

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

* `Block Parser for Bitcoin`_
* `How to Program Block Chain Explorers with Python`_
* `Genesis block`_
* `Blockchain.info Block #0`_

.. _Block Parser for Bitcoin: https://github.com/tenthirtyone/blocktools
.. _How to Program Block Chain Explorers with Python: http://alexgorale.com/how-to-program-block-chain-explorers-with-python-part-1
.. _Genesis block: https://en.bitcoin.it/wiki/Genesis_block
.. _Blockchain.info Block #0: https://blockchain.info/block/000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f
