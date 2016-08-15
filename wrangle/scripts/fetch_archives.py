"""
Does a month-by-month query of the USGS site for earthquake data
"""
from dateutil import rrule
from datetime import datetime, timedelta
from pathlib import Path
import requests

SRC_DATA_URL = "http://earthquake.usgs.gov/fdsnws/event/1/query.csv"
DEST_DIR = Path('wrangle', 'corral', 'fetched')
DEST_DIR.mkdir(exist_ok=True, parents=True)

START_DATE = datetime(1970, 1, 1)
END_DATE = datetime(2016,9,1) # script will end at the month before


def main():
    timespan = rrule.rrule(rrule.MONTHLY, dtstart=START_DATE, until=END_DATE)
    u_params = {'orderby': 'time-asc'}
    u_params['starttime'] = START_DATE
    for dt in timespan[1:]:
        u_params['endtime'] = dt
        # call the API
        resp = requests.get(SRC_DATA_URL, params = u_params)
        # Save the resulting text
        # as: "2015-05.csv"
        destpath = DEST_DIR / u_params['starttime'].strftime("%Y-%m.csv")
        destpath.write_text(resp.text)
        print("Saved:", destpath)
        # set the starttime to the next date for the next iteration
        u_params['starttime'] = u_params['endtime']



if __name__ == '__main__':
    main()
