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

This will spin up the database as well as pgAdmin which you can access on port 8080 on your machine. The default credentials can be found in ```settings.py```.


After the database has been initialized run the migrations on the database to create the required tables:

```
poetry run pynt migrate_database
```

After this is done, you can populate your database by running:

```
poetry run spoons_scraper
```
