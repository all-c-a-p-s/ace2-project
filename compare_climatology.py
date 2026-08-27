import numpy as np
import xarray as xr


PREDICTIONS = "with_artificial_forcing/monthly_mean_predictions.nc"
ERA5 = "era5_monthly_precip_ace_grid.nc"
CLIMATOLOGY = "era5_monthly_climatology_ace_grid.nc"


pred_ds = xr.open_dataset(PREDICTIONS)
era5_ds = xr.open_dataset(ERA5)
clim_ds = xr.open_dataset(CLIMATOLOGY)


prediction = (
    pred_ds["PRATEsfc"]
    .isel(sample=0, drop=True)
    .rename({"lat": "latitude", "lon": "longitude"})
    * 86400.0
)

months = pred_ds["valid_time"].isel(sample=0).dt.month.values

prediction = (
    prediction.assign_coords(month=("time", months))
    .swap_dims({"time": "month"})
    .drop_vars("time")
)


observation = era5_ds["precipitation"].sel(
    valid_time=era5_ds.valid_time.dt.year == 2020
)

observation = (
    observation.assign_coords(
        month=("valid_time", observation.valid_time.dt.month.values)
    )
    .swap_dims({"valid_time": "month"})
    .drop_vars("valid_time")
    .sel(month=prediction.month)
)


climatology = clim_ds["precipitation_climatology"].sel(month=prediction.month)


observation = observation.assign_coords(
    latitude=prediction.latitude,
    longitude=prediction.longitude,
)

climatology = climatology.assign_coords(
    latitude=prediction.latitude,
    longitude=prediction.longitude,
)


weights = np.cos(np.deg2rad(prediction.latitude))


def area_mean(field):
    return field.weighted(weights).mean(("latitude", "longitude"))


prediction_error = prediction - observation
climatology_error = climatology - observation

prediction_mse = area_mean(prediction_error**2)
climatology_mse = area_mean(climatology_error**2)

prediction_rmse = np.sqrt(prediction_mse)
climatology_rmse = np.sqrt(climatology_mse)

bias = area_mean(prediction_error)

skill = 1.0 - prediction_mse / climatology_mse


for month in prediction.month.values:
    print(f"\nMonth {int(month)}")
    print(f"  ACE2 RMSE:         {float(prediction_rmse.sel(month=month)):.3f} mm/day")
    print(f"  Climatology RMSE:  {float(climatology_rmse.sel(month=month)):.3f} mm/day")
    print(f"  ACE2 bias:         {float(bias.sel(month=month)):+.3f} mm/day")
    print(f"  MSE skill score:   {float(skill.sel(month=month)):+.3f}")
