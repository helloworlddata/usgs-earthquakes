from settings import FETCHED_DIR as SRC_DIR
from csv import DictReader, DictWriter
from sys import stdout

US_LATITUDES = [24.6, 50]
US_LONGITUDES = [-125, -65]

def main():
    filenames = list(SRC_DIR.glob('*.csv'))
    with filenames[0].open('r') as _f:
        headers = _f.readline().strip().split(',')

    outcsv = DictWriter(stdout, fieldnames=headers)
    outcsv.writeheader()

    for fname in filenames:
        with fname.open('r') as rf:
            for row in DictReader(rf):
                lat = float(row['latitude'])
                lng = float(row['longitude'])
                if lat >= US_LATITUDES[0] and lat <= US_LATITUDES[1]\
                and lng >= US_LONGITUDES[0] and lng <= US_LONGITUDES[1]:
                    outcsv.writerow(row)

if __name__ == '__main__':
    main()
