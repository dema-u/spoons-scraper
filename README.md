# Wetherspoons Locations Scraper

Downloads all wetherspoon pubs locations to a postgres database.

## Requirements

- [Flyway](https://flywaydb.org/)
- [Docker](https://www.docker.com/)
- [Poetry](https://python-poetry.org/)

To spin up the postgres database required to run the scraper, spin up the docker-compose:

```
docker-compose up
```

This will spin up the database as well as pgAdmin which you can access on port 8080 on your machine. The credentials to login to your local database and pgAdmin can be found in ```docker-compose.yaml```. If connecting through pgAdmin you need to use the container name of the postgres db as pgAdmin is on the docker network.


After the database has been initialized run the migrations on the database to create the required tables:

```
poetry run pynt migrate_database
```

After this is done, you can populate your database by running:

```
poetry run spoons_scraper
```
