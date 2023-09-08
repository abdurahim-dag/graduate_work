FROM postgres:14

RUN localedef -i ru_RU -c -f UTF-8 -A /usr/share/locale/locale.alias ru_RU.UTF-8
ENV LANG ru_RU.utf8

COPY ../../sql/ddl/ods.sql /docker-entrypoint-initdb.d/0-init.sql
COPY ../../sql/ddl/views.sql /docker-entrypoint-initdb.d/1-views.sql

RUN chmod +rx /docker-entrypoint-initdb.d/0-init.sql
RUN chmod +rx /docker-entrypoint-initdb.d/1-views.sql
