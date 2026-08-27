import cdsapi


DATASET = "reanalysis-era5-single-levels-monthly-means"
OUTPUT = "era5_precip_jfm_1993_2020.nc"

request = {
    "product_type": ["monthly_averaged_reanalysis"],
    "variable": ["mean_total_precipitation_rate"],
    "year": [str(year) for year in range(1993, 2021)],
    "month": ["01", "02", "03"],
    "time": ["00:00"],
    "data_format": "netcdf",
    "download_format": "unarchived",
}

client = cdsapi.Client()
client.retrieve(DATASET, request).download(OUTPUT)

print(f"Saved {OUTPUT}")
