create view ods.v_movies as
with genres as (
    select
        g.id,
        g.created,
        g.modified,
        g.name,
        gfw.film_work_id
    from ods.genre g
             left join ods.genre_film_work gfw
                       on gfw.genre_id = g.id
),
     agg_genre as (
         select
             g.film_work_id,

             json_agg (
                     json_build_object(
                             'id'::text, g.id::text,
                             'name'::text, g.name::text
                         )
                 ) as "genres"
         from genres g
         group by
             g.film_work_id
     ),
     persons as (
         select
             p.full_name,
             pfw.film_work_id,
             pfw.role,
             p.id,
             p.created,
             p.modified
         from ods.person p
                  left join ods.person_film_work pfw
                            on p.id = pfw.person_id
     ),
     directors as (
         select
             persons.film_work_id,
             json_agg (
                     json_build_object(
                             'id'::text, persons.id::text,
                             'name'::text, persons.full_name::text
                         )
                 ) as "directors"
         from persons
         where persons.role = 'director'
         group by persons.film_work_id
     ),
     writers as (
         select
             persons.film_work_id,
             json_agg (
                     json_build_object(
                             'id'::text, persons.id::text,
                             'name'::text, persons.full_name::text
                         )
                 ) as "writers"
         from persons
         where persons.role = 'writer'
         group by persons.film_work_id
     ),
     actors as (
         select
             persons.film_work_id,
             json_agg (
                     json_build_object(
                             'id', persons.id,
                             'name', persons.full_name
                         )
                 ) as "actors"
         from persons
         where persons.role = 'actor'
         group by persons.film_work_id
     ),
     actors_names as (
         select
             persons.film_work_id,
             json_agg (
                     persons.full_name::text
                 )
                 as "actors_names"
         from persons
         where persons.role = 'actor'
         group by persons.film_work_id
     ),
     writers_names as (
         select
             persons.film_work_id,
             json_agg (
                     persons.full_name::text
                 )
                 as "writers_names"
         from persons
         where persons.role = 'writer'
         group by persons.film_work_id
     ),
     ids as (
         select id
         from ods.film_work f
         union
         select p.film_work_id as "id"
         from persons p
         union
         select g.film_work_id as "id"
         from genres g
     )
select
    json_build_object('id', fw.id,
                      'imdb_rating', coalesce(fw.rating,0),
                      'title', fw.title,
                      'description', coalesce(fw.description, ''),
                      'directors', coalesce(directors.directors, '[]'),
                      'writers', coalesce(writers.writers,'[]'),
                      'actors', coalesce(actors.actors,'[]'),
                      'actors_names', coalesce(actors_names.actors_names,'[]'),
                      'writers_names', coalesce(writers_names.writers_names,'[]'),
                      'genre', coalesce(agg_genre.genres,'[]')) as "obj",
    fw.modified as "modified"
from ods.film_work fw
         left join directors on directors.film_work_id = fw.id
         left join writers on writers.film_work_id = fw.id
         left join actors on actors.film_work_id = fw.id
         left join actors_names on actors_names.film_work_id = fw.id
         left join writers_names on writers_names.film_work_id = fw.id
         left join agg_genre on agg_genre.film_work_id = fw.id
where fw.id in (select id from ids);

create view ods.v_genres as
with genres as (
    select
        id,
        created,
        modified,
        name,
        description
    from ods.genre
)
select
    json_build_object('id', g.id,
                      'name', coalesce(g.name, ''),
                      'description', coalesce(g.description, '')
        ) as "obj",
    g.modified as "modified"
from genres g;

create view ods.v_persons as
with persons as (
    select
        p.id,
        p.created,
        p.modified,
        p.full_name,
        pfw.role,
        json_agg (
                pfw.film_work_id::text
            ) as "film_ids"
    from ods.person p
             inner join ods.person_film_work pfw on pfw.person_id = p.id
    group by
        p.id,
        p.created,
        p.modified,
        p.full_name,
        pfw.role
    order by p.id
)
select
    json_build_object('id', p.id,
                      'full_name', p.full_name,
                      'role', p.role,
                      'film_ids', coalesce(p.film_ids,'[]')
        ) as "obj",
    p.modified as "modified"
from persons p
