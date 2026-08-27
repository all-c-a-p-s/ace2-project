import numpy as np
import xarray as xr


PREDICTIONS = "with_real_forcing/monthly_mean_predictions.nc"
ERA5 = "era5_monthly_precip_ace_grid.nc"
CLIMATOLOGY = "era5_monthly_climatology_ace_grid.nc"


pred_ds = xr.open_dataset(PREDICTIONS)
era5_ds = xr.open_dataset(ERA5)
clim_ds = xr.open_dataset(CLIMATOLOGY)


# ---------------- Load and standardise ----------------

raw_prediction = (
    pred_ds["PRATEsfc"]
    .isel(sample=0, drop=True)
    .rename({"lat": "latitude", "lon": "longitude"})
)

months = pred_ds["valid_time"].isel(sample=0).dt.month.values

prediction = (
    (raw_prediction * 86400.0)
    .assign_coords(month=("time", months))
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


# ---------------- Metadata ----------------

print("=== UNITS ===")
print("ACE2 raw:", raw_prediction.attrs.get("units"))
print("ERA5:", observation.attrs.get("units"))
print("Climatology:", climatology.attrs.get("units"))
print("ACE2 conversion used: ×86400 -> mm/day")

print("\n=== MONTHS ===")
print("Prediction:", prediction.month.values)
print("Observation:", observation.month.values)
print("Climatology:", climatology.month.values)


# ---------------- Grid checks ----------------

print("\n=== GRID ===")
for name, field in [
    ("prediction", prediction),
    ("observation", observation),
    ("climatology", climatology),
]:
    print(
        f"{name:12}",
        field.sizes["latitude"],
        "x",
        field.sizes["longitude"],
        "lat endpoints:",
        field.latitude.values[[0, -1]],
        "lon endpoints:",
        field.longitude.values[[0, -1]],
    )

for name, field in [
    ("observation", observation),
    ("climatology", climatology),
]:
    print(
        f"{name} max latitude mismatch:",
        float(np.max(np.abs(field.latitude.values - prediction.latitude.values))),
    )
    print(
        f"{name} max longitude mismatch:",
        float(np.max(np.abs(field.longitude.values - prediction.longitude.values))),
    )

# Remove only harmless CDO coordinate-rounding differences.
observation = observation.assign_coords(
    latitude=prediction.latitude,
    longitude=prediction.longitude,
)
climatology = climatology.assign_coords(
    latitude=prediction.latitude,
    longitude=prediction.longitude,
)

prediction, observation, climatology = xr.align(
    prediction,
    observation,
    climatology,
    join="exact",
)


# ---------------- Data checks ----------------

print("\n=== DATA QUALITY ===")

for name, field in [
    ("prediction", prediction),
    ("observation", observation),
    ("climatology", climatology),
]:
    print(f"\n{name}")
    print("  NaNs:", int(field.isnull().sum()))
    print("  min:", float(field.min()))
    print("  max:", float(field.max()))
    print("  mean:", float(field.mean()))
    print("  negative cells:", int((field < 0).sum()))


# ---------------- Area-weighted monthly means ----------------

weights = np.cos(np.deg2rad(prediction.latitude))


def area_mean(field):
    return field.weighted(weights).mean(("latitude", "longitude"))


print("\n=== AREA-WEIGHTED MONTHLY MEANS (mm/day) ===")

pred_mean = area_mean(prediction)
obs_mean = area_mean(observation)
clim_mean = area_mean(climatology)

for month in prediction.month.values:
    print(f"\nMonth {int(month)}")
    print(f"  ACE2:       {float(pred_mean.sel(month=month)):.3f}")
    print(f"  ERA5:       {float(obs_mean.sel(month=month)):.3f}")
    print(f"  Climatology:{float(clim_mean.sel(month=month)):.3f}")


# ---------------- Error recomputation ----------------

pred_error = prediction - observation
clim_error = climatology - observation

pred_rmse = np.sqrt(area_mean(pred_error**2))
clim_rmse = np.sqrt(area_mean(clim_error**2))
skill = 1.0 - pred_rmse**2 / clim_rmse**2

print("\n=== RECOMPUTED SCORES ===")

for month in prediction.month.values:
    print(f"\nMonth {int(month)}")
    print(f"  ACE2 RMSE:        {float(pred_rmse.sel(month=month)):.3f}")
    print(f"  Climatology RMSE: {float(clim_rmse.sel(month=month)):.3f}")
    print(f"  Skill:            {float(skill.sel(month=month)):+.3f}")


# ---------------- Basic sanity assertions ----------------

assert np.array_equal(prediction.month, observation.month)
assert np.array_equal(prediction.month, climatology.month)

assert prediction.sizes["latitude"] == observation.sizes["latitude"]
assert prediction.sizes["longitude"] == observation.sizes["longitude"]

assert int(prediction.isnull().sum()) == 0
assert int(observation.isnull().sum()) == 0
assert int(climatology.isnull().sum()) == 0

assert float(prediction.min()) >= -1e-5
assert float(observation.min()) >= -1e-5
assert float(climatology.min()) >= -1e-5

print("\nAll structural sanity checks passed.")
