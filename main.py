import requests

from web3 import Web3


if __name__ == '__main__':
    # Get the validator slot<>pk map
    slot_validator_pubkey_map = {}
    validator_resp = requests.get('https://relay-builders-eu.ultrasound.money/relay/v1/builder/validators').json()

    for i in validator_resp:
        slot_validator_pubkey_map[i['slot']] = i['entry']['message']['pubkey']

    # Get the current block number, and slot etc
    w3 = Web3(Web3.HTTPProvider("https://eth.merkle.io"))
    cur_bn = w3.eth.block_number
    pending_bn = cur_bn + 1

    # Get the best bid
    slot_resp = requests.get(f'https://relay-builders-eu.ultrasound.money/relay/v1/data/bidtraces/builder_blocks_received?block_number={pending_bn}').json()
    slot_resp = list(map(lambda x: {**x, 'value': int(x['value'])}, slot_resp))
    slot_resp = sorted(slot_resp, key=lambda x: x['value'], reverse=True)
    best_bid = slot_resp[0]

    # Get the header
    cur_slot = best_bid['slot']
    parent_hash = best_bid['parent_hash']
    validator_pubkey = slot_validator_pubkey_map[cur_slot]

    # Get the logs bloom
    bloom_resp = requests.get(f'https://relay-builders-eu.ultrasound.money/eth/v1/builder/header/{cur_slot}/{parent_hash}/{validator_pubkey}').json()
    print(bloom_resp)