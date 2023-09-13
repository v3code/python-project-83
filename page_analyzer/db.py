from urllib.parse import urlparse

from psycopg2.pool import AbstractConnectionPool, ThreadedConnectionPool


def initialize_db(uri: str,
                  min_connections: int = 1,
                  max_connections: int = 10) -> AbstractConnectionPool:
    parsed_uri = urlparse(uri)
    username = parsed_uri.username
    password = parsed_uri.password
    database = parsed_uri.path[1:]
    hostname = parsed_uri.hostname
    port = parsed_uri.port
    pool = ThreadedConnectionPool(min_connections,
                                  max_connections,
                                  username=username,
                                  password=password,
                                  database=database,
                                  hostname=hostname,
                                  port=port)
    return pool
