import hashlib

_cache = {}


def generate_key(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def get_cache(text: str):
    return _cache.get(generate_key(text))


def set_cache(text: str, value):
    _cache[generate_key(text)] = value