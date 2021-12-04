import click

from spoons_scraper.postgres.client import PostgresClient

@click.command()
def main():
    pg_client = PostgresClient.bootstrap_from_settings()
    all_locs = pg_client.get_all_locations()
    print(all_locs)

if __name__ == '__main__':
    main()
