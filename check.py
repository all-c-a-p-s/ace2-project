import xarray as xr

ace = xr.open_dataset("forcing_data/forcing_2020.nc")
sst = xr.open_dataset("sst_mean.nc")
ice = xr.open_dataset("sea_ice_mean_6h.nc")

for ds, name in [
    (ace, "surface_temperature"),
    (ace, "sea_ice_fraction"),
    (sst, "sst"),
    (ice, "siconc"),
]:
    print(name, ds[name].attrs)
