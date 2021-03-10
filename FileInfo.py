# Get index info from nc file
from netCDF4 import Dataset
import numpy as np
import os
import xarray as xr


class NCFileInfoCRU:
    def __init__(self, directory, file_name):
        self.file_name = file_name
        self.ds = Dataset(directory + file_name, mode="r", format="NetCDF4")
        # print(self.ds)
        self.dataset_name = self.get_dataset_name()
        self.index = self.get_index()
        self.month = self.get_month()
        self.year = self.get_year()
        self.date = self.get_date()
        self.grid = self.get_grid()
        self.mask = self.get_mask()
        self.time_var = self.get_time_var()
        # print(self.time_var)
        self.lat = self.ds['lat'][:].tolist()
        # self.lon = np.roll(self.ds['lon'][:], int(len(self.ds['lon'][:])/2))
        # self.lon[:int(len(self.lon)/2)] = self.lon[:int(len(self.lon)/2)] - 360
        self.lon = self.ds['lon'][:].tolist()
        print("lon",len(self.lon))
        self.coordinate = self.get_coordinate()
        self.geojson = self.get_geojson()

    def get_dataset_name(self):
        return self.file_name[:-3].split(".")[0][:-1]

    def get_index(self):
        return self.file_name[:-3].split(".")[4]

    def get_month(self):
        return list(range(1,13))

    def get_year(self):
        # years = self.file_name[:-3].split(".")[2]
        start = int(self.file_name[:-3].split(".")[2])
        end = int(self.file_name[:-3].split(".")[3])
        # print(self.file_name)
        return list(range(start, end+1, 1))

    def get_date(self):
        times = self.ds['time'][:].data
        # dates = []
        # print(times)
        # for i in times:
        #     # print(i)
        #     temp_dt = (datetime.datetime.fromordinal(i) + relativedelta(years=1899)).strftime("%Y-%m-%d")
        #     dates.append(temp_dt)
        return times

    def get_grid(self):
        grids = 1
        return {"lon_step": float(grids), "lat_step": float(grids)}

    def get_mask(self):
        return self.file_name[:-3].split(".")[-1]

    def get_time_var(self):
        # Availavle time variable
        variables = list(self.ds.variables.keys())[3:-1]
        return variables

    def get_coordinate(self):
        lon = np.arange(-179.5, 179.6, 1)
        lat = np.arange(-89.5, 89.6, 1)
        # temp_lat = np.repeat(np.arange(-89.5, 89.6, 1),360)
        # temp_lon = np.tile(np.arange(-179.5, 179.6, 1),180)
        # create (x, y) = (lon, lat) cartesian product
        lon_lat = np.transpose(
            [np.tile(lon, 180), np.repeat(lat, 360)]
        )
        print(len(lon_lat.tolist()))
        return lon_lat.tolist()

    def get_geojson(self):
        coordinate_feature = []
        for i in self.coordinate:
            coordinate_feature.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": i
                }
            })
        geojson_obj = {
            'type': 'FeatureCollection',
            'features': coordinate_feature
        }
        return geojson_obj

class NCFileInfoamip:
    def __init__(self, directory, file_name):
        self.file_name = file_name
        self.ds = Dataset(directory + file_name, mode="r", format="NetCDF4")
        # print(self.ds)
        self.dataset_name = self.get_dataset_name()
        self.index = self.get_index()
        self.month = self.get_month()
        self.date = self.get_date()
        self.year = self.get_year()
        self.mask = self.get_mask()
        self.time_var = self.get_time_var()
        self.lat = self.ds['lat'][:].tolist()
        # self.lon = self.ds['lon'][:].tolist()
        self.lon = np.roll(self.ds['lon'][:], int(len(self.ds['lon'][:])/2))
        self.lon[:int(len(self.lon)/2)] = self.lon[:int(len(self.lon)/2)] - 360
        self.lon = self.lon.tolist()
        # print(len(self.lon))
        self.grid = self.get_grid()
        self.coordinate = self.get_coordinate()
        # print("coor",len(self.coordinate))
        self.geojson = self.get_geojson()

    def get_dataset_name(self):
        return self.file_name[:-3].split("_")[2]

    def get_index(self):
        return self.file_name[:-3].split("_")[0]

    def get_date(self):
        times = self.ds['time'][:].data
        return times

    def get_year(self):
        years = self.file_name[:-3].split("_")[6].split("-")
        start = int(years[0][:4])
        end = int(years[1][:-4])
        # print("start",start)
        return list(range(start, end+1, 1))

    def get_grid(self):
        # grid = np.array(self.lon)
        grids = self.lon[-1] - self.lon[-2]
        return {"lon_step": float(grids), "lat_step": float(grids)}

    def get_mask(self):
        return self.file_name[:-3].split("_")[3]

    def get_month(self):
        range_m = self.file_name[:-3].split("_")[6].split("-")
        start = int(range_m[0][-1])
        end = int(range_m[1][-2:])
        # print(start)
        # print(end)
        return list(range(start, end+1, 1))

    def get_time_var(self):
        # Availavle time variable
        variables = list(self.ds.variables.keys())[-1:]
        return variables

    def get_coordinate(self):
        # lon = np.array(self.lon)
        # lat = np.array(self.lat)
        lat = np.arange(-90, 90, 0.705)
        lon = np.arange(-180, 180,  0.705)
        # create (x, y) = (lon, lat) cartesian product
        lon_lat = np.transpose(
            [np.tile(lon, len(lat)), np.repeat(lat, len(lon))]
        )
        # print(lon)
        # print(len(lon_lat.tolist()))
        return lon_lat.tolist()

    def get_geojson(self):
        coordinate_feature = []
        for i in self.coordinate:
            coordinate_feature.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": i
                }
            })
        geojson_obj = {
            'type': 'FeatureCollection',
            'features': coordinate_feature
        }
        return geojson_obj

class AllFileInfo:
    def __init__(self, directory, file_name):
        self.file_name = file_name
        self.ds = Dataset(directory + file_name)
        self.dataset_name = self.get_dataset_name()
        self.index = self.get_index()
        self.mask = self.get_mask()
        self.date = self.get_date()
        self.time_var = self.get_time_var()
        self.unit = self.ds.variables["time"].units
        self.lat = self.ds['lat'][:].tolist()
        self.lon = self.ds['lon'][:].tolist()
        # print("lon",len(self.lon))
        # self.coordinate = self.get_coordinate()
        # self.geojson = self.get_geojson()

    def get_dataset_name(self):
        if self.file_name[:-3].split(".")[-1] == 'dat':
            return self.file_name[:-3].split(".")[0][:-1]
        else:
            return self.file_name[:-3].split("_")[2]
 
    def get_index(self):
        if self.file_name[:-3].split(".")[-1] == 'dat':
            if self.file_name[:-3].split(".")[4] == 'tmp':
                return 'tas'
            elif self.file_name[:-3].split(".")[4] == 'tmn':
                return 'tasmin'
            elif self.file_name[:-3].split(".")[4] == 'tmx':
                return 'tasmax'
            elif self.file_name[:-3].split(".")[4] == 'pre':
                return 'pr'
            else:
                pass
        else:
            return self.file_name[:-3].split("_")[0]

    def get_date(self):
        times = self.ds['time'][:].data
        return times

    def get_mask(self):
        if self.file_name[:-3].split(".")[-1] == 'dat':
            return self.file_name[:-3].split(".")[-1]
        else:
            return self.file_name[:-3].split("_")[3]

    def get_time_var(self):
        if self.file_name[:-3].split(".")[-1] == 'dat':
            return list(self.ds.variables.keys())[3]
        else:
            return list(self.ds.variables.keys())[-1]

    def shift_lon(self):
        lons = self.ds['lon'][:].tolist()
        if lons[0] == 0:
            lon = np.roll(self.ds['lon'][:], int(len(self.ds['lon'][:])/2))
            lon[:int(len(lon)/2)] = lon[:int(len(lon)/2)] - 360
            return lon.tolist()
        else:
            return lons




if __name__ == "__main__":
    # directory = "./CRU_TS_current/"
    # for file_name in os.listdir(directory):
    #     f = NCFileInfoCRU(directory, file_name)
    # directory = "./CRU_TS_current/"
    # for file_name in os.listdir(directory):
    #     f = AllFileInfo(directory, file_name)
    
    directory = "C:/Mew/Project/CNRM-ESM2-1/"
    for file_name in os.listdir(directory):
        f = AllFileInfo(directory, file_name)
        data = {
            "name":f.dataset_name,
            "index": f.index,
            "date": f.date,
            # "lat": len(f.lat),
            "lon": f.lon[0],
            # "grid": f.grid,
            # "month": f.month,
            # "year": f.year,
            # "date": f.date,
            "mask": f.mask,
            "time_var": f.time_var,
            # "coor":len(f.coordinate)
        }
        print(data)
