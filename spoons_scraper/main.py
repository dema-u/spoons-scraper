import click

from spoons_scraper.postgres.client import PostgresClient
from spoons_scraper.types import SpoonsLocation


@click.command()
def main():
    pg_client = PostgresClient.bootstrap_from_settings()
    pass

if __name__ == '__main__':
    main()
