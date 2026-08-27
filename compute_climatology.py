import xarray as xr

INPUT = "era5_monthly_precip_mm_day.nc"
OUTPUT = "era5_monthly_climatology.nc"

ds = xr.open_dataset(INPUT)

precip = ds["precipitation"]

climatology = precip.groupby("valid_time.month").mean("valid_time")

climatology.name = "precipitation_climatology"
climatology.attrs = precip.attrs

climatology.to_netcdf(OUTPUT)

print(f"Saved {OUTPUT}")
print(climatology)
