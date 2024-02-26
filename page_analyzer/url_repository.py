from datetime import datetime

from page_analyzer.db import DatabaseHandler


class URLRepository:
    def __init__(self, db: DatabaseHandler):
        self._db = db

    def add_url(self, name: str):
        query = "INSERT INTO urls (name, created_at)" \
                " VALUES (%s, %s)" \
                " RETURNING *;"
        return self._db.fetch_one(query, (name, datetime.now()))

    def get_url_by_id(self, url_id: int):
        query = "SELECT * FROM urls WHERE id = %s;"
        return self._db.fetch_one(query, (url_id,))

    def get_url_by_name(self, name: str):
        query = "SELECT * FROM urls WHERE name = %s;"
        return self._db.fetch_one(query, (name,))

    def get_all_urls(self):
        query = "SELECT * FROM urls ORDER BY id DESC;"
        return self._db.fetch_all(query)

    def get_latest_checks(self):
        query = 'SELECT DISTINCT ON (url_id) * FROM url_checks ' \
                'ORDER BY url_id DESC, created_at ASC;'
        return self._db.fetch_all(query)

    def add_check(self,
                  url_id: int,
                  status_code: int,
                  h1: str,
                  title: str,
                  description: str):
        query = "INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at)" \
                " VALUES (%s, %s, %s, %s, %s, %s)" \
                " RETURNING *;"
        return self._db.fetch_one(query,
                                  (url_id,
                                   status_code,
                                   h1,
                                   title,
                                   description,
                                   datetime.now()))

    def get_checks_for_url_id(self, url_id: int):
        query = "SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC;"
        return self._db.fetch_all(query, (url_id,))
