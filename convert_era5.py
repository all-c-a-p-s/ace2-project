import xarray as xr

ds = xr.open_dataset("era5_precip_jfm_1993_2020.nc")

monthly = ds["avg_tprate"] * 86400.0
monthly.name = "precipitation"
monthly.attrs["units"] = "mm/day"

monthly.to_netcdf("era5_monthly_precip_mm_day.nc")

print(monthly)
