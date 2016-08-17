from sys import argv, stdout
from pathlib import Path
import re
"""ugh this is crap"""


def glob_years(datadir, start_year, end_year):
    """
    expects datadir to be a Path containing files in this format:
    datadir/
        |__1990.csv
        |__1991.csv

    Yields: string, line of text
    """
    tx = str(start_year)
    ty = str(end_year)
    filenames = [f for f in datadir.glob('*.csv') if f.stem >= tx and f.stem < ty \
                                                     and re.match(r'\d{4}-\d{2}\.csv', f.name)]

    if not filenames:
        raise RuntimeWarning("No files that matched {0}/YYYY.csv between {1} and {2}".format(datadir, start_year, end_year))
    else:
        headers = None
        for fname in filenames:
            with fname.open('r') as f:
                headline = f.readline()
                if not headers:
                    headers = headline # set this once
                    yield headers
                for line in f: # read the remainder
                    yield line

if __name__ == '__main__':
    yrrx = re.compile(r'\d{4}')
    if len(argv) == 4 and yrrx.match(argv[1]) and yrrx.match(argv[2]):
        datadir = Path(argv[3])
        if datadir.is_dir():
            for line in glob_years(datadir, argv[1], argv[2]):
                stdout.write(line)
        else:
            raise IOError("`%s` is not a directory." % datadir)
    else:
        raise TypeError("Expected arguments: start_year end_year dirname; e.g. 1980 1981 mydata/fetched")



