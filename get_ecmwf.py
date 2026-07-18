import cdsapi


"""
Notes:
dd/mm/yy = date on which the predictions were made
leadtime_hour = lead of predictions
hence we use up to 24 * 90 = 2160 lead time 
"""

# just use one year/month for first test

years = ["2020"]
months = [str(x) for x in range(1, 2)]
times = [str(x * 6) for x in range(1, 361)]

dataset = "seasonal-original-single-levels"
request = {
    "originating_centre": "ecmwf",
    "system": "51",
    "year": years,
    "month": months,
    "day": ["01"],
    "leadtime_hour": times,
    "data_format": "netcdf",
}

client = cdsapi.Client()

for variable, filename in [
    ("sea_surface_temperature", "sst.nc"),
    ("sea_ice_cover", "sea_ice.nc"),
]:
    client.retrieve(
        dataset,
        {
            **request,
            "variable": [variable],
        },
    ).download(filename)
