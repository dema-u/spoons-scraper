import logging
from typing import List

import click

from spoons_scraper.postgres.client import PostgresClient
from spoons_scraper.settings import Settings
from spoons_scraper.types import SpoonsLocation
from spoons_scraper.website import get_locations_generator


def bootstrap_logger(log_debug: bool) -> logging.Logger:
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.DEBUG if log_debug else logging.INFO,
    )
    return logging.getLogger(__name__)


@click.command()
@click.option("--log-debug", default=False, is_flag=True)
def main(log_debug: bool):

    settings = Settings()
    logger = bootstrap_logger(log_debug)

    pg_client = PostgresClient.bootstrap_from_settings()
    existing_locations: List[SpoonsLocation] = pg_client.get_all_locations()

    locations_generator = get_locations_generator(
        base_url=settings.SPOONS_BASE_URL, locations_path=settings.SPOONS_LOCATIONS_PATH
    )

    for location in locations_generator:

        if location in existing_locations:
            logger.info(f"Already inserted: {location}")
            continue

        pg_client.save_locations([location])
        logger.info(f"Saved new location: {location}")


if __name__ == "__main__":
    main()
