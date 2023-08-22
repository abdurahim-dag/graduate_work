create schema if not exists staging;

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
