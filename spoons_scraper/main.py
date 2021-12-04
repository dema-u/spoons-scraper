import click

from spoons_scraper.postgres.client import PostgresClient

@click.command()
def main():
    pg_client = PostgresClient.bootstrap_from_settings()


if __name__ == '__main__':
    pass
