import os
from abc import ABC, abstractmethod
from contextlib import contextmanager
from enum import Enum
from typing import Optional, Sequence, Any
from urllib.parse import urlparse

from psycopg2 import connect
from psycopg2.pool import SimpleConnectionPool
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import cursor


def get_connection_resolver_from_env():
    db_uri = os.environ['DATABASE_URL']
    use_single_connection = os.environ.get('USE_SINGLE_CONNECTION', 'false')

    if use_single_connection == 'true':
        return SingleConnectionResolver(db_uri)

    min_connections = int(os.environ.get('DB_MIN_CONNECTIONS', 1))
    max_connections = int(os.environ.get('DB_MAX_CONNECTIONS', 10))

    return PoolConnectionResolver(db_uri,
                                  min_connections=min_connections,
                                  max_connections=max_connections)


class ConnectionResolver(ABC):
    @abstractmethod
    def get_connection(self) -> connect:
        raise NotImplementedError

    @abstractmethod
    def return_connection(self, connection: connect):
        raise NotImplementedError


class PoolConnectionResolver(ConnectionResolver):

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

    def get_connection(self) -> connect:
        return self._pool.getconn()

    def return_connection(self, connection: connect):
        self._pool.putconn(connection)


# Some database implementations already using pool
class SingleConnectionResolver(ConnectionResolver):
    def __init__(self, db_uri: str):
        self.db_uri = db_uri

    def get_connection(self) -> connect:
        return connect(self.db_uri)

    def return_connection(self, connection: connect):
        connection.close()


@contextmanager
def create_cursor(connection_resolver: ConnectionResolver,
                  cursor_factory: cursor = RealDictCursor):
    conn = connection_resolver.get_connection()
    db_cursor = conn.cursor(cursor_factory=cursor_factory)
    yield db_cursor
    db_cursor.close()
    conn.commit()
    connection_resolver.return_connection(conn)


class FetchOptions(Enum):
    ONE = 1
    ALL = 2
    NONE = 3


class DatabaseHandler:

    def __init__(self, connection_resolver: ConnectionResolver):
        self._connection_resolver = connection_resolver

    def execute(self,
                query: str,
                vars: Optional[Sequence[Any]] = None):
        return self._run_query(query, FetchOptions.NONE, vars)

    def _run_query(self,
                   query: str,
                   fetch_type: FetchOptions,
                   vars: Optional[Sequence[Any]] = None):
        with create_cursor(self._connection_resolver) as db_cursor:
            db_cursor.execute(query, vars)
            match fetch_type:
                case FetchOptions.ONE:
                    return db_cursor.fetchone()
                case FetchOptions.ALL:
                    return db_cursor.fetchall()

    def fetch_one(self,
                  query: str,
                  vars: Optional[Sequence[Any]] = None):
        return self._run_query(query, FetchOptions.ONE, vars)

    def fetch_all(self,
                  query: str,
                  vars: Optional[Sequence[Any]] = None):
        return self._run_query(query, FetchOptions.ALL, vars)
