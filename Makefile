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
	docker compose -f ./docker/state/docker-compose.yml down --remove-orphans -v

add-variables:
	docker cp variables.json airflow-webserver:/home/airflow/variables.json
	docker exec airflow-webserver bash -c "airflow variables import /home/airflow/variables.json"

add-conn-movies:
	docker exec airflow-webserver bash -c "airflow connections add \"movies\" --conn-json '{\
    \"conn_type\": \"postgres\",\
    \"login\": \"app\",\
    \"password\": \"qwe123\",\
    \"host\": \"movies\",\
    \"port\": \"5432\",\
    \"schema\": \"movies_database\",\
    \"extra\": {\"sslmode\": \"disable\"}\
}'"

add-conn-state:
	docker exec airflow-webserver bash -c "airflow connections add \"state\" --conn-json '{\
    \"conn_type\": \"redis\",\
    \"host\": \"state\",\
    \"port\": \"6379\",\
    \"schema\": \"0\"\
}'"

add-conn-staging:
	docker exec airflow-webserver bash -c "airflow connections add \"staging\" --conn-json '{\
    \"conn_type\": \"postgres\",\
    \"login\": \"etl\",\
    \"password\": \"123qwe\",\
    \"host\": \"staging\",\
    \"port\": \"5432\",\
    \"schema\": \"etl\",\
    \"extra\": {\"sslmode\": \"disable\"}\
}'"

start-all: 0-start-staging 0-start-state 0-start-movies 0-start-airflow 0-start-clickhouse 0-start-elasticsearch 0-start-kafka
