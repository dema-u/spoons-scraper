import pynt

from spoons_scraper.postgres.migrations import MIGRATIONS_PATH


@pynt.task()
def check_for_flyway():
    pass


@pynt.task(check_for_flyway)
def migrate_database():
    print(MIGRATIONS_PATH)
