from netCDF4 import Dataset
from FileInfo import NCFileInfoCRU,NCFileInfoamip,AllFileInfo
import numpy as np
import pandas as pd
from pathlib import Path
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from cftime import num2date
import cftime
import function
import xarray as xr

# branch = 'current'

datasets = "CNRM-ESM2-1"
# datasets = "MPI-ESM1-2-LR"
p = "C:/Mew/Project/"
# folder_name = "./{}_{}/".format(datasets)
folder_name = p + datasets
ROOT = Path(folder_name)
files = list(sorted(ROOT.glob("*")))

# print(f'{datasets}_file')
dst_folder = Path(f'{datasets}_h_file'.lower())
dst_folder.mkdir(parents=True, exist_ok=True)

for file_name in os.listdir(folder_name):
    print(file_name)

    f = AllFileInfo(f"{folder_name}/", file_name)
    ds = xr.open_dataset(f"{folder_name}/{file_name}")

    if f.mask == 'dat':
        # date = np.array(list(map(lambda x: (datetime.date.fromordinal(x) + relativedelta(years=1899)).strftime("%Y-%m-%d") ,time)))
        date = [function.gregorian2date(d) for d in f.date]
        date = np.array(date)
    elif f.mask == 'amip':
        if f.index == 'pr':
            ds = ds.resample(time='m').sum()
        else:
            ds = ds.resample(time='m').mean()
        date = [function.gregorian2date1(d) for d in f.date]
        date = np.array(date)

    value_old = ds[f.time_var][:].data
    time = ds['time'][:].data
    lats = np.array(ds['lat'])
    lons = np.array(ds['lon'])

    if lons[0] == 0:
        print("shiftlon")
        lons = function.shift_lon(lons)
        # print("old : ",value_old[0])
        value = np.array([function.shift_data(value_old[d]) for d in range(value_old.shape[0])])
        # print("shift value : ",value[0])
        if f.time_var == 'pr':
            print("<<<<<<<<>>>>>>>>>>>>>>>")
            value = np.array([data * 86400 for data in value]) 
            print(value[0])
            print(np.nanmax(value))
        else:
            value = np.array([data - 273 for data in value])    
    else:
        value = value_old

    rangr_y = (int(date[-1][:4])-int(date[0][:4]))+1

    m, lat, lon = value.shape
    down_size = 0

    value = np.where(value > 1E20, np.nan, value)

    if down_size != 0 :
        # down data
        data_re = value.reshape((m, lat//down_size, down_size, lon//down_size, down_size)) #(90,4,180,4)
        data = np.nanmean(data_re, axis=2)#.mean(1)
        data = np.nanmean(data, axis=3)
        print("shape data",data.shape)
        print("size data",data.size)

        # down lat lon
        new_shape = np.array([len(lats) // down_size, len(lons) // down_size])
        end_index = new_shape * down_size
        old_lons = lons[:end_index[1]]
        old_lats = lats[:end_index[0]]
        new_lons = np.linspace(np.min(old_lons), np.max(old_lons), new_shape[1])
        new_lats = np.linspace(np.min(old_lats), np.max(old_lats), new_shape[0])
        print("lat shape",new_lats.shape)
        print("lat size",new_lats.size)

    else:
        data = value
        new_lats = lats
        new_lons = lons
        print("lon size",new_lons.size)
        print("lat size",new_lats.size)
        
    offset = 0
    for i in range(rangr_y):
        offset = i * 12
        np.savez(f'{dst_folder}/{f.index}' + '-'+ str(int(date[0][:4]) + i), value = data[offset + 0 : offset + 12], time = date[offset + 0 : offset + 12], lat = new_lats, lon = new_lons)
        print(f"created: {f.dataset_name} {f.index} {int(date[0][:4]) + i}")
