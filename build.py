import platform
import subprocess
from pathlib import Path

import pynt

from spoons_scraper import MIGRATIONS_PATH
from spoons_scraper.settings import Settings

PROJECT_ROOT_PATH = Path(__file__, "..").resolve()


@pynt.task()
def check_flyway():
    process = subprocess.run(["which", "flyway"], shell=platform.system() == "Windows")
    assert process.returncode == 0, "Flyway is not installed"


@pynt.task(check_flyway)
def migrate_database():

    settings = Settings()

    process = subprocess.run(
        [
            "flyway",
            "migrate",
            f"-url=jdbc:postgresql://{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}",
            f"-user={settings.DB_USER}",
            f"-password={settings.DB_PASS}",
            f"-locations=filesystem:{MIGRATIONS_PATH.relative_to(PROJECT_ROOT_PATH)}",
        ],
        shell=platform.system() == "Windows",
    )
    assert process.returncode == 0, "Failed database migration"


@pynt.task()
def install_git_hooks():

    process = subprocess.run(
        ["poetry", "run", "pre-commit", "install"], shell=platform.system() == "Windows"
    )
    assert process.returncode == 0, "Failed installing pre-commit hooks"
