from typing import Optional, Dict
from urllib.parse import urlparse

from bs4 import BeautifulSoup
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


def parse_url(page: str, length_limit: int = 255) -> Dict[str, str]:
    soup = BeautifulSoup(page, 'html.parser')
    title = soup.find('title').text if soup.find('title') else ''
    h1 = soup.find('h1').text if soup.find('h1') else ''
    description = soup.find('meta', attrs={'name': 'description'})
    return dict(h1=h1[:length_limit],
                title=title[:length_limit],
                description=description['content'][:length_limit] if description else '')
