from psycopg2.pool import AbstractConnectionPool


class URLRepository:
    def __init__(self, pool: AbstractConnectionPool):
        self._pool = pool

    def add_url(self,
                add_url_dto):
        pass

    def add_url_analysis(self,
                         add_url_analysis_dto):
        pass

    def get_url_analysis(self):
        pass

    def get_url(self):
        pass
