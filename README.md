# Wetherspoons Locations Scraper

Downloads all wetherspoon pubs locations to a postgres database.

## Requirements

- [Flyway](https://flywaydb.org/)
- [Docker](https://www.docker.com/)
- [Poetry](https://python-poetry.org/)


## Usage

To spin up a local postgres database required to run the scraper, run the docker-compose file:

```
docker-compose up
```

This will initalize the database as well as pgAdmin which you can access on port 8080 on your machine. The credentials to login to your local database and pgAdmin can be found in ```docker-compose.yaml```. If connecting through pgAdmin you need to use the container name of the postgres db (it's just 'db') as pgAdmin is on the docker network.


After the database has been initialized run the migrations on the database to create the required tables:

```
poetry run pynt migrate_database
```

After this is done, you can populate your database by running:

```
poetry run spoons_scraper
```

If for whatever reason you actually want this in a remote database, you can add a ```.env``` file in the root of the project specifying the connection details. The env variables have to match the names in ```settings.py```, more information in [pydantic documentation](https://pydantic-docs.helpmanual.io/usage/settings/#dotenv-env-support).

---

If you can't be bothered to do any of this, the ```spoons.csv``` file contains some sample data.
