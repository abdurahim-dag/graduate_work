FROM postgres:14

RUN localedef -i ru_RU -c -f UTF-8 -A /usr/share/locale/locale.alias ru_RU.UTF-8
ENV LANG ru_RU.utf8

COPY ../../sql/ddl/movies_database.sql /docker-entrypoint-initdb.d/movies_database.sql
RUN chmod +rx /docker-entrypoint-initdb.d/movies_database.sql
