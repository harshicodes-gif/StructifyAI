import hashlib


_cache = {}


def generate_key(text: str):

    return hashlib.sha256(text.encode()).hexdigest()


def get(text: str):

    return _cache.get(generate_key(text))


def set(text: str, value):

    _cache[generate_key(text)] = value