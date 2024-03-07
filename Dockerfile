FROM postgres

COPY ./sql/* /docker-entrypoint-initdb.d

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=blog

EXPOSE 5434:5432
