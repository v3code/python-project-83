from typing import List, Tuple
from dataclasses import asdict

from page_analyzer.data import UrlDTO, UrlCheckDTO, UrlInfo, UrlLatestCheck
from page_analyzer.errors import URLExistsError, FlashableError, ValidationError, URLNotExistsError, UrlCheckError
from page_analyzer.url_repository import URLRepository
from returns.result import Result, Success, Failure
import requests
from page_analyzer.utils import validate_url, parse_url


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

    # Faster approach would by doing this on db with join.
    # It implemented this way because of the task requirements.
    def get_urls_with_latest_checks(self) -> List[UrlLatestCheck]:
        urls = self._repository.get_all_urls()
        checks = self._repository.get_latest_checks()

        result = []
        checks_by_url_id = {check['url_id']: check for check in checks}

        for url in urls:
            check = checks_by_url_id.get(url['id'])
            url_latest_check = UrlLatestCheck(
                id=url['id'],
                url_name=url['name'],
                latest_check_date=str(check['created_at']) if check is not None else '',
                status_code=str(check['status_code']) if check is not None else ''
            )
            result.append(url_latest_check)

        return result

    def get_url_and_checks_by_id(self, url_id: int) -> Result[Tuple[UrlDTO, List[UrlCheckDTO]], FlashableError]:
        result = self.get_url_by_id(url_id)
        return result.map(self._compose_url_and_checks)

    def _compose_url_and_checks(self, url: UrlDTO):
        checks = [UrlCheckDTO(**check) for check in self._repository.get_checks_for_url_id(url.id)]
        return url, checks

    def get_all_urls(self) -> List[UrlDTO]:
        return [UrlDTO(**url) for url in self._repository.get_all_urls()]

    def check_url(self, url_id: int) -> Result[UrlCheckDTO, FlashableError]:
        get_url_result = self.get_url_by_id(url_id)
        return get_url_result.bind(self.process_url).map(self.add_check)

    def add_check(self, url_info: UrlInfo) -> UrlCheckDTO:
        url_check = self._repository.add_check(**asdict(url_info))
        return UrlCheckDTO(**url_check)

    def process_url(self, url: UrlDTO) -> Result[UrlInfo, FlashableError]:
        try:
            response = requests.get(url.name)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            return Failure(UrlCheckError())

        status_code = response.status_code
        parsed_url = parse_url(response.text)
        url_info = UrlInfo(
            url_id=url.id,
            status_code=status_code,
            **parsed_url
        )
        return Success(url_info)

    def get_checks_for_url_id(self, url_id: int) -> List[UrlCheckDTO]:
        return [UrlCheckDTO(**check) for check in self._repository.get_checks_for_url_id(url_id)]
