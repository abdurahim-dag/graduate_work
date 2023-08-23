FROM clickhouse/clickhouse-server:latest

COPY ./docker/clickhouse/init.sh /home/init.sh
RUN chmod +x /home/init.sh

COPY ./sql/ddl/mart.sql /home/mart.sql
RUN chmod +x /home/mart.sql

COPY ./docker/clickhouse/entrypoint.sh  /docker-entrypoint-initdb.d/entrypoint.sh
RUN sed -i 's/\r$//g' /docker-entrypoint-initdb.d/entrypoint.sh
RUN chmod +x /docker-entrypoint-initdb.d/entrypoint.sh
