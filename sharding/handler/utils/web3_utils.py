import rlp

from eth_utils import (
    to_checksum_address,
)


def get_code(w3, address):
    return w3.eth.getCode(to_checksum_address(address))


def get_nonce(w3, address):
    return w3.eth.getTransactionCount(to_checksum_address(address))


def take_snapshot(w3):
    return w3.testing.snapshot()


def revert_to_snapshot(w3, snapshot_id):
    w3.testing.revert(snapshot_id)


def mine(w3, num_blocks):
    w3.testing.mine(num_blocks)


def send_raw_transaction(w3, raw_transaction):
    raw_transaction_bytes = rlp.encode(raw_transaction)
    raw_transaction_hex = w3.toHex(raw_transaction_bytes)
    transaction_hash = w3.eth.sendRawTransaction(raw_transaction_hex)
    return transaction_hash


def get_recent_block_hashes(w3, history_size):
    block = w3.eth.getBlock('latest')
    recent_hashes = []

    for _ in range(history_size):
        recent_hashes.append(block['hash'])
        # break the loop if we hit the genesis block.
        if block['number'] == 0:
            break
        block = w3.eth.getBlock(block['parentHash'])

    return tuple(reversed(recent_hashes))


def get_canonical_chain(w3, recent_block_hashes, history_size):
    block = w3.eth.getBlock('latest')

    new_block_hashes = []

    for _ in range(history_size):
        if block['hash'] in recent_block_hashes:
            break
        new_block_hashes.append(block['hash'])
        block = w3.eth.getBlock(block['parentHash'])
    else:
        raise Exception('No common ancestor found')

    first_common_ancestor_idx = recent_block_hashes.index(block['hash'])

    revoked_hashes = recent_block_hashes[first_common_ancestor_idx + 1:]

    # reverse it to comply with the order of `self.recent_block_hashes`
    reversed_new_block_hashes = tuple(reversed(new_block_hashes))

    return revoked_hashes, reversed_new_block_hashes
