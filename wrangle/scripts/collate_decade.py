from settings import FETCHED_DIR as SRC_DIR


from sys import argv, stdout

def glob_decade(decade):
    filenames = SRC_DIR.glob('%s*-*.csv' % decade[0:3])
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
    decade = argv[1] # e.g. 1980
    for line in glob_decade(decade):
        stdout.write(line)
