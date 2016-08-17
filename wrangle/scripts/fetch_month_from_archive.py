"""
Does a single month query of the USGS site for earthquake data

Sample query:
http://earthquake.usgs.gov/fdsnws/event/1/query.csv\
?starttime=2016-08-09%2000:00:00\
&endtime=2016-08-16%2000:00:00\
&orderby=time-asc

"""
from copy import copy
from dateutil import rrule
from datetime import datetime
from pathlib import Path
from sys import argv, stdout
import requests
import re

SRC_DATA_URL = "http://earthquake.usgs.gov/fdsnws/event/1/query.csv"

BASE_PARAMS = {'orderby': 'time-asc'}

def fetch_monthly_archive(year, month):
    """
    year integer
    month: integer
    Returns: string, entire text tresponse from usgs server
    """
    startdate = datetime(year, month, 1)
    # let rrule do the work of calculating the next month
    r = rrule.rrule(rrule.MONTHLY, dtstart=startdate)

    parms = copy(BASE_PARAMS)
    # datetime objects automatically convert to %Y-%m-%d %H:%M:%S
    # but let's be explicit
    parms['starttime'] = r[0].strftime('%Y-%m-%d %H:%M:%S')
    parms['endtime'] = r[1].strftime('%Y-%m-%d %H:%M:%S')
    resp = requests.get(SRC_DATA_URL, params = parms)
    return resp.text



if __name__ == '__main__':
    if len(argv) == 2 and re.match(r'\d{4}-\d{2}', argv[1]):
        year, month = [int(v) for v in argv[1].split('-')]
        for line in fetch_monthly_archive(year, month):
            stdout.write(line)
    else:
        raise TypeError("Expects a single string argument to be passed in: YYYY-MM; e.g. 2015-03")
