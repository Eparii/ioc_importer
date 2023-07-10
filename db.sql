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

CREATE TABLE source_t
(
    id SERIAL PRIMARY KEY,
    name VARCHAR(64)
)