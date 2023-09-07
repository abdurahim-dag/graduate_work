create schema if not exists ods;

SET search_path TO ods,public;
ALTER ROLE etl SET search_path TO ods,public;

create table if not exists ods.watching_movies(
    id bigint generated always AS IDENTITY primary key,
    user_id uuid,
    movie_id uuid,
    frameno bigint,
    timestamp timestamp
);

create table if not exists ods.likes_movies(
    id bigint generated always AS IDENTITY primary key,
    user_id uuid,
    movie_id uuid,
    score int check ( score >= 0 AND score <= 10 ),
    timestamp timestamp
);

create table if not exists ods.dlq(
    id bigint generated always AS IDENTITY primary key,
    obj TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ods.film_work
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

create table IF NOT EXISTS ods.genre
(
    id          UUID PRIMARY KEY,
    name        TEXT NOT NULL,
    description TEXT,
    created     TIMESTAMP WITH TIME ZONE,
    modified    TIMESTAMP WITH TIME ZONE
);

create table IF NOT EXISTS ods.person
(
    id        UUID PRIMARY KEY,
    full_name TEXT NOT NULL,
    created   TIMESTAMP WITH TIME ZONE,
    modified  TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS ods.genre_film_work
(
    id           UUID PRIMARY KEY,
    film_work_id UUID NOT NULL REFERENCES film_work(id) ON DELETE CASCADE,
    genre_id     UUID NOT NULL REFERENCES genre(id) ON DELETE CASCADE,
    created      TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS ods.person_film_work
(
    id           UUID PRIMARY KEY,
    film_work_id UUID NOT NULL REFERENCES film_work(id) ON DELETE CASCADE,
    person_id    UUID NOT NULL REFERENCES person(id) ON DELETE CASCADE,
    role         TEXT NOT NULL,
    created      TIMESTAMP WITH TIME ZONE
);
