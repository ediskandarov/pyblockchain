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
