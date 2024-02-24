from typing import Optional
from urllib.parse import urlparse

from validators import url as is_valid_url


def validate_url(url: str) -> Optional[str]:
    if not url:
        return 'URL обязателен'
    if len(url) > 255:
        return 'URL превышает 255 символов'
    if not is_valid_url(url):
        return 'Некорректный URL'
    return None


def normalize_url(url: str):
    out = urlparse(url)
    scheme = out.scheme.lower()
    netloc = out.netloc.lower()
    return f'{scheme}://{netloc}'
