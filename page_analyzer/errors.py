from page_analyzer.data import UrlDTO


class FlashableError(RuntimeError):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def get_message(self):
        return self.message


class ValidationError(FlashableError):
    pass


class URLExistsError(FlashableError):
    def __init__(self, url: UrlDTO):
        super().__init__('Страница уже существует')
        self._url = url

    def get_url(self):
        return self._url


class URLNotExistsError(FlashableError):
    def __init__(self, url_id: int):
        super().__init__(f'URL c id {url_id} не существует')
        self._url_id = url_id

    def get_url_id(self):
        return self._url_id


class UrlCheckError(FlashableError):
    def __init__(self):
        super().__init__("Произошла ошибка при проверке")
