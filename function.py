import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta
from cftime import num2date
import cftime

def cartesian(x, y):
    return np.transpose([np.tile(x, len(y)), np.repeat(y, len(x))])

def shift_lon(lons):
    lons = np.roll(lons, int(len(lons)/2))
    lons[:int(len(lons)/2)] -= 360
    return lons

def shift_data(data):
    # print("shape data",data.shape[2])
    # print("old : ",data[0])
    data = np.roll(data, data.shape[1]//2, axis=1)
    # print("new :",data[0])
    return data

def orderpair(x, y):
    return np.array(np.transpose([np.tile(x, len(y)), np.repeat(y, len(x))]))

def gregorian2date(date) -> str:
    # a = (datetime.fromordinal(date) + relativedelta(years=1899)).strftime("%Y-%m-%d")
    # print(a)
    return (datetime.fromordinal(date) + relativedelta(years=1899)).strftime("%Y-%m-%d")

def gregorian2date1(data) -> str:
    # print(units)
    # print(type(units))
    dates = num2date(data, 'days since 1850-01-01 00:00:00', 'gregorian')
    # d = datetime.strptime(str(dates), "%Y-%m-%d")
    # a = str(f'{dates.year}-{dates.month}-{dates.day}')
    # print(dates)
    # print(str(f'{dates.year}-{dates.month}-{dates.day}'))
    # return datetime.datetime(dates.year, dates.month, dates.day).strftime("%Y-%m-%d")
    return str(f'{dates.year}-{dates.month}-{dates.day}')

gregorian2date1(52610.5)