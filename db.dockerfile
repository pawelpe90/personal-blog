FROM postgres

COPY ./sql/* /docker-entrypoint-initdb.d

EXPOSE 5432:5432
