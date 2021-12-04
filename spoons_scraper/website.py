from typing import Generator, Set, Callable, Tuple
from pydantic import HttpUrl, ValidationError
import logging
from urllib.parse import urljoin
import backoff
import re
from bs4 import BeautifulSoup
from pydantic.fields import T
import requests

from spoons_scraper import BS4_PARSER
from spoons_scraper.types import SpoonsLocation
from spoons_scraper.exceptions import WebsiteParseError


logger = logging.getLogger(__name__)


def parse_error_handler(func: Callable) -> Callable:
    
    if func.__name__.beginswith('_get'):
        element = func.__name__[len('_get')+1:]
    else:
        element = func.__name__
        
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            raise WebsiteParseError(
                f"Unexpected error when parsing {element}"
            ) from exc
            
    return wrapper


def get_spoons_locations(base_url: HttpUrl, locations_path: str) -> Generator[SpoonsLocation, None, None]:

    soup = _get_soup(base_url, locations_path)
    
    try:
        location_paths = _get_locations_paths(soup)
    except WebsiteParseError:
        logger.exception(f'Could not parse location paths @ {locations_path}. Stopping...')
        return
    
    for pub_name, location_path in location_paths:
        
        if pub_name is None:
            logger.warning(f'Path {location_path} does not have a pub name')
            continue
        
        soup = _get_soup(base_url, location_path)
        
        try:
            street_address, locality, region, post_code = _get_location_details(soup)
            yield SpoonsLocation(
                pub_name=pub_name,
                street_address=street_address,
                locality=locality,
                region=region,
                post_code=post_code
            )
        except WebsiteParseError:
            logger.warning(f'Could not parse data @ {location_path}', exc_info=True)
        except ValidationError:
            logger.warning(f'Could not validate data @ {location_path}', exc_info=True)
        finally:
            continue


@backoff.on_exception(
    backoff.expo,
    (
        requests.exceptions.RequestException,
        requests.exceptions.ConnectionError,
        requests.exceptions.HTTPError,
        requests.exceptions.Timeout
    ),
    max_time=30
)
def _get_soup(base_url: HttpUrl, path: str):
    response = requests.get(urljoin(base_url, path))
    response.raise_for_status()
    return BeautifulSoup(response.content, BS4_PARSER)


@parse_error_handler
def _get_location_details(soup: BeautifulSoup) -> Tuple[str, str, str, str]:
    street_address = _process_string(soup.find('span', itemprop='streetAddress').string)
    locality = _process_string(soup.find('span', itemprop='addressLocality').string)
    region = _process_string(soup.find('span', itemprop='addressRegion').string)
    post_code = _process_string(soup.find('span', itemprop='postalCode').string)
    return street_address, locality, region, post_code


@parse_error_handler
def _get_locations_paths(soup: BeautifulSoup) -> Set[Tuple[str, str]]:
    return set(
        (tag.string, tag.get('href')) for tag
        in soup.find_all('a', href=re.compile(r'^\/pubs\/all-pubs\/'))
    )

def _process_string(string: str) -> str:
    processed_string = string.strip(' ').strip('\n').strip(':')
    return processed_string