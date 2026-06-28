import hashlib
from typing import Any

_cache: dict[str, Any] = {}


def generate_key(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def get_cache(text: str) -> Any:
    return _cache.get(generate_key(text))


def set_cache(text: str, value: Any) -> None:
    _cache[generate_key(text)] = value
