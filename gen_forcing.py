from pathlib import Path

import xarray as xr


TEMPLATE = "forcing_data/forcing_2020.nc"
SST_FILE = "sst_mean.nc"
ICE_FILE = "sea_ice_mean_6h.nc"

OUTPUT = Path("ecmwf_forcing/forcing_2020-01-01.nc")
OUTPUT.parent.mkdir(exist_ok=True)

template = xr.open_dataset(TEMPLATE)
sst_ds = xr.open_dataset(SST_FILE)
ice_ds = xr.open_dataset(ICE_FILE)

sst = sst_ds["sst"].isel(forecast_reference_time=0, drop=True)
ice = (
    ice_ds["siconc"]
    .isel(
        forecast_reference_time=0,
        drop=True,
    )
    .clip(0.0, 1.0)
)

valid_times = sst_ds["valid_time"].values

sst = sst.isel(latitude=slice(None, None, -1)).assign_coords(
    latitude=template.latitude,
    longitude=template.longitude,
)

ice = ice.isel(latitude=slice(None, None, -1)).assign_coords(
    latitude=template.latitude,
    longitude=template.longitude,
)

sst = sst.rename(forecast_period="time").assign_coords(time=valid_times)
ice = ice.rename(forecast_period="time").assign_coords(time=valid_times)

all_times = template.time.sel(time=slice("2020-01-01T00:00:00", valid_times[-1]))

out = template.sel(time=all_times).copy()

out["sea_ice_fraction"].loc[{"time": valid_times}] = ice

out["surface_temperature"].loc[{"time": valid_times}] = xr.where(
    sst.notnull(),
    sst,
    out["surface_temperature"].sel(time=valid_times),
)

encoding = {name: {"zlib": True, "complevel": 4} for name in out.data_vars}

encoding["time"] = {
    key: template["time"].encoding[key]
    for key in ("units", "calendar", "dtype")
    if key in template["time"].encoding
}

out.to_netcdf(OUTPUT, encoding=encoding)
