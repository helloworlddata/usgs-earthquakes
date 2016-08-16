from settings import FETCHED_DIR as SRC_DIR
from csv import DictReader, DictWriter
from sys import stdout, argv

US_LATITUDES = [24.6, 50]
US_LONGITUDES = [-125, -65]

def main(start_datestr="0000", end_datestr="9999"):
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
                date = row['time']

                if lat >= US_LATITUDES[0] and lat <= US_LATITUDES[1]\
                and lng >= US_LONGITUDES[0] and lng <= US_LONGITUDES[1]\
                and date >= start_datestr and date < end_datestr:
                    outcsv.writerow(row)

if __name__ == '__main__':

    x = argv[1] if len(argv) > 1 else '0000'
    y = argv[2] if len(argv) > 2 else '9999'
    main(x, y)
