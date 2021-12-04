import pynt
import subprocess
from pathlib import Path

from spoons_scraper import MIGRATIONS_PATH


PROJECT_ROOT_PATH = Path(__file__, '..'). resolve()


@pynt.task()
def check_for_flyway():
    process = subprocess.run(
        [
            "which",
            "flyway"
        ]
    )
    assert process.returncode == 0, "Please install flyway"


@pynt.task(check_for_flyway)
def migrate_database():
    subprocess.run(
        [
            "flyway",
            "migrate",
            "-url=jdbc:postgresql://localhost:5432/spoons",
            "-user=root",
            "-password=root",
            "-locations=filesystem:{path}".format(path=MIGRATIONS_PATH.relative_to(PROJECT_ROOT_PATH))
        ]
    )
