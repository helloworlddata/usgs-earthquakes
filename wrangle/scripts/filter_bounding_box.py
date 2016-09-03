from csv import DictReader, DictWriter
from sys import stdout
import argparse

def filter(row, x0, y0, x1, y1):
    lat = float(row['latitude'])
    lng = float(row['longitude'])
    return lat >= y0 and lat <= y1 and lng >= x0 and lng <= x1

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Filter csv-latitude/longitude data by x0 y0 x1 y1 filename/stdin")
    parser.add_argument('x0', type=float)
    parser.add_argument('y0', type=float)
    parser.add_argument('x1', type=float)
    parser.add_argument('y1', type=float)
    parser.add_argument('infile', type=argparse.FileType('r'))
    args = parser.parse_args()

    csvin = DictReader(args.infile)
    headers = csvin.fieldnames
    if not all(attr in headers for attr in ['latitude', 'longitude']):
        raise IOError("Input data must be CSV formatted and have `latitude` and `longitude` headers")
    else:
        csvout = DictWriter(stdout, fieldnames=headers)
        csvout.writeheader()
        for row in csvin:
            # ignore subsequent headers if files are being concatenated
            if not row['latitude'] == 'latitude':
                if filter(row, args.x0, args.y0, args.x1, args.y1):
                    csvout.writerow(row)
