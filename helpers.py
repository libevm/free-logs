from eth_bloom import BloomFilter
from web3 import Web3


def h2b(h: str) -> bytes:
    """
    Hex 2 bytes
    """
    return bytes.fromhex(h.replace("0x", ""))


def log_in_bloom(bloom_filter: bytes, log_address: str, log_topics: list[str]) -> bool:
    bf = BloomFilter(int.from_bytes(bloom_filter))

    # Check the address
    if not h2b(log_address) in bf:
        return False
    
    # Check all topics
    for topic in log_topics:
        if not h2b(topic) in bf:
            return False

    return True
