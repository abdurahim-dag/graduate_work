CREATE SCHEMA if not exists content;

SET search_path TO content,public;
ALTER ROLE app SET search_path TO content,public;

CREATE TABLE IF NOT EXISTS content.film_work
(
    id            UUID PRIMARY KEY,
    title         TEXT NOT NULL,
    description   TEXT,
    creation_date DATE,
    rating        FLOAT,
    type          TEXT NOT NULL,
    created       TIMESTAMP WITH TIME ZONE,
    modified      TIMESTAMP WITH TIME ZONE
);

create table IF NOT EXISTS content.genre
(
    id          UUID PRIMARY KEY,
    name        TEXT NOT NULL,
    description TEXT,
    created     TIMESTAMP WITH TIME ZONE,
    modified    TIMESTAMP WITH TIME ZONE
);

create table IF NOT EXISTS content.person
(
    id        UUID PRIMARY KEY,
    full_name TEXT NOT NULL,
    created   TIMESTAMP WITH TIME ZONE,
    modified  TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.genre_film_work
(
    id           UUID PRIMARY KEY,
    film_work_id uuid not null REFERENCES film_work(id) ON DELETE CASCADE,
    genre_id     UUID NOT NULL REFERENCES genre(id) ON DELETE CASCADE,
    created      TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.person_film_work
(
    id           UUID PRIMARY KEY,
    film_work_id UUID NOT NULL REFERENCES film_work(id) ON DELETE CASCADE,
    person_id    UUID NOT NULL REFERENCES person(id) ON DELETE CASCADE,
    role         TEXT NOT NULL,
    created      TIMESTAMP WITH TIME ZONE
);

CREATE INDEX CONCURRENTLY IF NOT EXISTS film_work_title_like_idx ON content.film_work(title varchar_pattern_ops);
CREATE INDEX CONCURRENTLY IF NOT EXISTS film_work_title_idx ON content.film_work (title);
CREATE INDEX CONCURRENTLY IF NOT EXISTS film_work_rating_idx ON content.film_work (rating);
CREATE INDEX CONCURRENTLY IF NOT EXISTS film_work_creation_date_idx ON content.film_work (creation_date);

CREATE UNIQUE INDEX CONCURRENTLY IF NOT EXISTS genre_film_work_unique_idx ON content.genre_film_work (genre_id, film_work_id);
CREATE UNIQUE INDEX CONCURRENTLY IF NOT EXISTS person_film_work_unique_idx ON content.person_film_work (person_id, film_work_id, role);
