from pathlib import Path

FETCHED_DIR = Path('wrangle', 'corral', 'fetched')
FETCHED_DIR.mkdir(exist_ok=True, parents=True)
COLLATED_DIR = Path('wrangle', 'corral', 'collated')
COLLATED_DIR.mkdir(exist_ok=True, parents=True)
