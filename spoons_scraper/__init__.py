from pathlib import Path

MIGRATIONS_PATH = Path(__file__, '..', 'postgres', 'migrations').resolve()
BS4_PARSER = 'lxml'