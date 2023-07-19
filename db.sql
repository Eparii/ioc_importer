DROP TABLE IF EXISTS ip_t;
DROP TABLE IF EXISTS url_t;
DROP TABLE IF EXISTS source_t;


CREATE TABLE source_t
(
    id SERIAL PRIMARY KEY,
    name VARCHAR(64)
);

CREATE TABLE ip_t
(
    id SERIAL PRIMARY KEY,
    ip_address inet,

    id_source INT REFERENCES source_t(id) ON DELETE CASCADE
);

CREATE TABLE url_t
(
    id SERIAL PRIMARY KEY,
    url TEXT,

    id_source INT REFERENCES source_t(id) ON DELETE CASCADE
);
