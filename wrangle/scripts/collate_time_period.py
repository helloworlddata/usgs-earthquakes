from settings import FETCHED_DIR as SRC_DIR


from sys import argv, stdout

def glob_years(start_year, end_year):
    filenames = [f for f in SRC_DIR.glob('*.csv') if f.stem >= start_year and f.stem < end_year]

    headers = None
    for fname in filenames:
        for lineno, line in enumerate(fname.open('r')):
            if lineno == 0 and not headers:
                headers = line
                yield headers
            elif lineno == 0 and headers:
                pass
            else:
                yield line


if __name__ == '__main__':
    startyr = argv[1] # e.g. 1980
    endyr = argv[2] # e.g. 1981
    for line in glob_years(startyr, endyr):
        stdout.write(line)
