create schema if not exists staging;

SET search_path TO staging,public;
ALTER ROLE etl SET search_path TO staging,public;

create table if not exists staging.watching_movies(
    id bigint generated always AS IDENTITY primary key,
    user_id uuid,
    movie_id uuid,
    frameno bigint,
    timestamp timestamp
);

create table if not exists staging.likes_movies(
    id bigint generated always AS IDENTITY primary key,
    user_id uuid,
    movie_id uuid,
    score int check ( score >= 0 AND score <= 10 ),
    timestamp timestamp
);

create table if not exists staging.dlq(
    id bigint generated always AS IDENTITY primary key,
    obj TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS staging.film_work
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

create table IF NOT EXISTS staging.genre
(
    id          UUID PRIMARY KEY,
    name        TEXT NOT NULL,
    description TEXT,
    created     TIMESTAMP WITH TIME ZONE,
    modified    TIMESTAMP WITH TIME ZONE
);

create table IF NOT EXISTS staging.person
(
    id        UUID PRIMARY KEY,
    full_name TEXT NOT NULL,
    created   TIMESTAMP WITH TIME ZONE,
    modified  TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS staging.genre_film_work
(
    id           UUID PRIMARY KEY,
    film_work_id UUID NOT NULL REFERENCES film_work(id) ON DELETE CASCADE,
    genre_id     UUID NOT NULL REFERENCES genre(id) ON DELETE CASCADE,
    created      TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS staging.person_film_work
(
    id           UUID PRIMARY KEY,
    film_work_id UUID NOT NULL REFERENCES film_work(id) ON DELETE CASCADE,
    person_id    UUID NOT NULL REFERENCES person(id) ON DELETE CASCADE,
    role         TEXT NOT NULL,
    created      TIMESTAMP WITH TIME ZONE
);
