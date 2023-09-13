from page_analyzer.url_repository import URLRepository


class URLService:
    def __init__(self, repository: URLRepository):
        self._repository = repository
