DROP TABLE IF EXISTS url_checks CASCADE;
DROP TABLE IF EXISTS urls CASCADE;

CREATE TABLE urls
(
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(255) UNIQUE NOT NULL,
    created_at DATE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE url_checks
(
    id          SERIAL PRIMARY KEY,
    url_id      INTEGER REFERENCES urls (id),
    status_code INTEGER,
    created_at  DATE DEFAULT CURRENT_TIMESTAMP
);
