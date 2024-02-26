from contextlib import contextmanager
from enum import Enum
from typing import Optional, Sequence, Any
from urllib.parse import urlparse

from psycopg2.pool import SimpleConnectionPool, AbstractConnectionPool
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import cursor


@contextmanager
def create_cursor(pool: AbstractConnectionPool,
                  cursor_factory: cursor = RealDictCursor):
    conn = pool.getconn()
    cursor = conn.cursor(cursor_factory=cursor_factory)
    yield cursor
    conn.commit()
    cursor.close()
    pool.putconn(conn)


class FetchOptions(Enum):
    ONE = 1
    ALL = 2
    NONE = 3


class DatabaseHandler:
    def __init__(self,
                 uri: str,
                 min_connections: int = 1,
                 max_connections: int = 10):

        parsed_uri = urlparse(uri)
        user = parsed_uri.username
        password = parsed_uri.password
        database = parsed_uri.path[1:]
        host = parsed_uri.hostname
        port = parsed_uri.port
        self._pool = SimpleConnectionPool(min_connections,
                                          max_connections,
                                          user=user,
                                          password=password,
                                          database=database,
                                          host=host,
                                          port=port)

    def execute(self,
                query: str,
                vars: Optional[Sequence[Any]] = None):
        return self._run_query(query, FetchOptions.NONE, vars)

    def _run_query(self,
                   query: str,
                   fetch_type: FetchOptions,
                   vars: Optional[Sequence[Any]] = None):
        with create_cursor(self._pool) as cursor:
            cursor.execute(query, vars)
            match fetch_type:
                case FetchOptions.ONE:
                    return cursor.fetchone()
                case FetchOptions.ALL:
                    return cursor.fetchall()

    def fetch_one(self,
                  query: str,
                  vars: Optional[Sequence[Any]] = None):
        return self._run_query(query, FetchOptions.ONE, vars)

    def fetch_all(self,
                  query: str,
                  vars: Optional[Sequence[Any]] = None):
        return self._run_query(query, FetchOptions.ALL, vars)
