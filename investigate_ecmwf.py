import xarray as xr

ds = xr.open_dataset("ecmwf.nc")
print(ds)
