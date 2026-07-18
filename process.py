import xarray as xr

"""
Process ECMWF data as downloaded from CDS
This takes the mean of the 51 ensemble members and LERPs the sea ice values,
which are only given at 24hr frequency
"""


SST_INPUT = "sst.nc"
ICE_INPUT = "sea_ice.nc"

SST_OUTPUT = "sst_mean.nc"
ICE_OUTPUT = "sea_ice_mean_6h.nc"


sst_ds = xr.open_dataset(
    SST_INPUT,
    chunks={
        "number": 1,
        "forecast_reference_time": 1,
        "forecast_period": 10,
    },
)

ice_ds = xr.open_dataset(
    ICE_INPUT,
    chunks={
        "number": 1,
        "forecast_reference_time": 1,
        "forecast_period": 5,
    },
)


sst_mean = sst_ds["sst"].mean("number", skipna=True)
ice_mean = ice_ds["siconc"].mean("number", skipna=True)


ice_mean_6h = ice_mean.interp(
    forecast_period=sst_mean["forecast_period"],
)

ice_mean_6h = ice_mean_6h.bfill("forecast_period")

ice_mean_6h = ice_mean_6h.clip(0.0, 1.0)


sst_output = sst_mean.to_dataset(name="sst")
ice_output = ice_mean_6h.to_dataset(name="siconc")


sst_output["sst"].attrs = sst_ds["sst"].attrs
ice_output["siconc"].attrs = ice_ds["siconc"].attrs


compression = {
    "zlib": True,
    "complevel": 4,
    "dtype": "float32",
}


sst_output.to_netcdf(
    SST_OUTPUT,
    encoding={"sst": compression},
)

ice_output.to_netcdf(
    ICE_OUTPUT,
    encoding={"siconc": compression},
)


print("Saved:", SST_OUTPUT)
print(sst_output)

print("\nSaved:", ICE_OUTPUT)
print(ice_output)
