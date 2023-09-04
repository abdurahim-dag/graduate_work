0-start-staging:
	docker compose -f ./docker/staging/docker-compose.yml --env-file ./.env.example up -d

0-start-movies:
	docker compose -f ./docker/movies/docker-compose.yml --env-file ./.env.example up -d

0-start-airflow:
	docker compose -f ./docker/airflow/docker-compose.yml --env-file ./.env.example up -d

0-start-elasticsearch:
	docker compose -f ./docker/elasticsearch/docker-compose.yml --env-file ./.env.example up -d

0-start-clickhouse:
	docker compose -f ./docker/clickhouse/docker-compose.yml --env-file ./.env.example up -d

0-start-kafka:
	docker compose -f ./docker/kafka/docker-compose.yml --env-file ./.env.example up -d

0-start-state:
	docker compose -f ./docker/state/docker-compose.yml up -d

elasricsearch-create-indexes:
	curl -X PUT "http://localhost:9200/movies" -H "Content-Type: application/json" -d @./test-data/schemas/es_schema_movies.json
	curl -X PUT "http://localhost:9200/genres" -H "Content-Type: application/json" -d @./test-data/schemas/es_schema_genres.json
	curl -X PUT "http://localhost:9200/persons" -H "Content-Type: application/json" -d @./test-data/schemas/es_schema_persons.json

import-movies:
	docker cp ./test-data/movies/film_work.sql movies:/home/film_work.sql
	docker cp ./test-data/movies/genre.sql movies:/home/genre.sql
	docker cp ./test-data/movies/person.sql movies:/home/person.sql
	docker cp ./test-data/movies/genre_film_work.sql movies:/home/genre_film_work.sql
	docker cp ./test-data/movies/person_film_work.sql movies:/home/person_film_work.sql
	docker exec -it movies bash -c "psql -d movies_database -U app -a -f /home/film_work.sql"
	docker exec -it movies bash -c "psql -d movies_database -U app -a -f /home/genre.sql"
	docker exec -it movies bash -c "psql -d movies_database -U app -a -f /home/person.sql"
	docker exec -it movies bash -c "psql -d movies_database -U app -a -f /home/genre_film_work.sql"
	docker exec -it movies bash -c "psql -d movies_database -U app -a -f /home/person_film_work.sql"


down-all:
	docker compose -f ./docker/staging/docker-compose.yml down --remove-orphans -v
	docker compose -f ./docker/airflow/docker-compose.yml down --remove-orphans -v
	docker compose -f ./docker/movies/docker-compose.yml down --remove-orphans -v
	docker compose -f ./docker/elasticsearch/docker-compose.yml down --remove-orphans -v
	docker compose -f ./docker/clickhouse/docker-compose.yml down --remove-orphans -v
	docker compose -f ./docker/kafka/docker-compose.yml down --remove-orphans -v
	docker compose -f ./docker/redis/docker-compose.yml down --remove-orphans -v

start-all: 0-start-staging 0-start-state 0-start-movies 0-start-airflow 0-start-clickhouse 0-start-elasticsearch 0-start-kafka
