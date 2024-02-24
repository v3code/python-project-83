from typing import List

from page_analyzer.dto import UrlDTO
from page_analyzer.errors import URLExistsError, FlashableError, ValidationError, URLNotExistsError
from page_analyzer.url_repository import URLRepository
from returns.result import Result, Success, Failure

from page_analyzer.utils import validate_url


class URLService:
    def __init__(self, repository: URLRepository):
        self._repository = repository

    def add_url(self, name: str) -> Result[UrlDTO, FlashableError]:
        error = validate_url(name)
        if error is not None:
            return Failure(ValidationError(error))
        url = self._repository.get_url_by_name(name)
        if url is not None:
            return Failure(URLExistsError(UrlDTO(**url)))
        url = self._repository.add_url(name)
        return Success(UrlDTO(**url))

    def get_url_by_id(self, url_id: int) -> Result[UrlDTO, FlashableError]:
        url = self._repository.get_url_by_id(url_id)

        if url is None:
            return Failure(URLNotExistsError(url_id))

        return Success(UrlDTO(**url))

    def get_all_urls(self) -> List[UrlDTO]:
        return [UrlDTO(**url) for url in self._repository.get_all_urls()]
