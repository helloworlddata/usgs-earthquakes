"""
Does a single month query of the USGS site for earthquake data

Sample query:
http://earthquake.usgs.gov/fdsnws/event/1/query.csv\
?starttime=2016-08-09%2000:00:00\
&endtime=2016-08-16%2000:00:00\
&orderby=time-asc

"""
from settings import FETCHED_DIR as DEST_DIR
from copy import copy
from dateutil import rrule
from datetime import datetime, timedelta
from pathlib import Path
from sys import argv
import requests


SRC_DATA_URL = "http://earthquake.usgs.gov/fdsnws/event/1/query.csv"

START_DATE = datetime(1970, 1, 1)
END_DATE = datetime(2016,9,1) # script will end at the month before

BASE_PARAMS = {'orderby': 'time-asc'}

def fetch_by_month(year, month):
    startdate = datetime(year, month, 1)
    r = rrule.rrule(rrule.MONTHLY, dtstart=startdate)
    parms = copy(BASE_PARAMS)
    # datetime objects automatically convert to %Y-%m-%d %H:%M:%S
    # but let's be explicit
    parms['starttime'] = r[0].strftime('%Y-%m-%d %H:%M:%S')
    parms['endtime'] = r[1].strftime('%Y-%m-%d %H:%M:%S')
    resp = requests.get(SRC_DATA_URL, params = parms)
    return resp


def fetch_and_save(start_date, end_date):

    timespan = rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date)
    for dt in timespan:
        resp = fetch_by_month(dt.year, dt.month)
        # Save the resulting text
        # as: "2015-05.csv"
        destpath = DEST_DIR / dt.strftime("%Y-%m.csv")
        destpath.write_text(resp.text)
        print("Fetched:", destpath)


if __name__ == '__main__':
    if len(argv) > 1 and len(argv) <= 3:
        startdate = datetime.strptime(argv[1], '%Y-%m')
        enddate = startdate if len(argv) < 3 else datetime.strptime(argv[2], '%Y-%m')
        fetch_and_save(startdate, enddate)
    else:
        print("""
            expects: fetch_archives.py 2016-02
            or:      fetch_archives.py 2016-02 2016-05""")
