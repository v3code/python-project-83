from typing import List, Tuple

from page_analyzer.data import UrlDTO, UrlCheckDTO
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

    def get_url_and_checks_by_id(self, url_id: int) -> Result[Tuple[UrlDTO, List[UrlCheckDTO]], FlashableError]:
        result = self.get_url_by_id(url_id)
        match result:
            case Success(url):
                checks = [UrlCheckDTO(**check) for check in self._repository.get_checks_for_url_id(url_id)]
                return Success((url, checks))
            case Failure(error):
                return Failure(error)

    def get_all_urls(self) -> List[UrlDTO]:
        return [UrlDTO(**url) for url in self._repository.get_all_urls()]

    def check_url(self, url_id: int) -> Result[UrlCheckDTO, URLNotExistsError]:
        result = self.get_url_by_id(url_id)
        match result:
            case Success():
                return Success(UrlCheckDTO(**self._repository.add_check(url_id)))
            case Failure(error):
                return Failure(error)

    def get_checks_for_url_id(self, url_id: int) -> List[UrlCheckDTO]:
        return [UrlCheckDTO(**check) for check in self._repository.get_checks_for_url_id(url_id)]
