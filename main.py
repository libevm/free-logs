import requests

from web3 import Web3

w3 = Web3(Web3.HTTPProvider("https://eth.merkle.io"))

# Example of checking a swap event in block 21246368
# https://etherscan.io/tx/0x674f9e552d7ca1de866d5a779449d6b2a2f3e9322ef42a224173261fa1c1bb89#eventlog
# from helpers import h2b, log_in_bloom
# log_bloom = w3.eth.get_block(21246368)['logsBloom']
# log_bloom = h2b('0x93ff7ef7bf539d41ba9fd2cfc474d7d9b17f9c15d47b3b219e8973657f33e1e7bbb6d7a9d279a9e44af97af96fce4d7c0fa1ae4d8df77feecfe7f97a607e3df709ffbda97ffb8bace8bfd52ebb75eeeb7fff6d35e766fad77c1defd7efffd2dc9f9378badf6eb56bc317ed8b6d89f9dbf373a7bfff299ffafc57ffde66dbf06dfbdedb5f36f577fcebeff5625bfbcebfec23aff7f7f5ed2f7ff93c5e7ed5f7eaff9c3f6abfb7fddbffbf7defdbe3ffecb755d6b605a5e11c7fe79fa7bec8f57feffddcffcd4fff5e0577ddfba2efca7f7fedffbfd32ead78feb5ff97fe77edfff5ffebf93edf37433bb5f7fb05f5f8d7effdff77775deeff93079d42e7587767')
# univ3_wbtc_ton = '0x5F0d8FC6057a959E79F7f79f8dBf12f29F9a9F34'
# log_topics = [
#     '0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67',
#     '0x0000000000000000000000003fc91a3afd70395cd496c647d5a6cc9d4b2b7fad',
#     '0x0000000000000000000000003fc91a3afd70395cd496c647d5a6cc9d4b2b7fad'
# ]
# swap_in_block = log_in_bloom(log_bloom, univ3_wbtc_ton, log_topics)
# print(swap_in_block)


if __name__ == '__main__':
    # Get the validator slot<>pk map
    slot_validator_pubkey_map = {}
    validator_resp = requests.get('https://relay-builders-eu.ultrasound.money/relay/v1/builder/validators').json()

    for i in validator_resp:
        slot_validator_pubkey_map[i['slot']] = i['entry']['message']['pubkey']

    # Get the current block number
    cur_bn = w3.eth.block_number
    pending_bn = cur_bn + 1

    # Get the best bid from the relay
    relay_resp = requests.get(f'https://relay-builders-eu.ultrasound.money/relay/v1/data/bidtraces/builder_blocks_received?block_number={pending_bn}').json()
    relay_resp = list(map(lambda x: {**x, 'value': int(x['value'])}, relay_resp))
    relay_resp = sorted(relay_resp, key=lambda x: x['value'], reverse=True)
    best_bid = relay_resp[0]

    # Get the header
    cur_slot = best_bid['slot']
    parent_hash = best_bid['parent_hash']
    validator_pubkey = slot_validator_pubkey_map[cur_slot]

    # Get the logs bloom
    bloom_resp = requests.get(f'https://relay-builders-eu.ultrasound.money/eth/v1/builder/header/{cur_slot}/{parent_hash}/{validator_pubkey}').json()
    print(pending_bn, bloom_resp)

    # TODO: Check the logs bloom