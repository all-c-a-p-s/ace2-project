import numpy as np
import matplotlib.pyplot as plt
import xarray as xr

VAR = "PRATEsfc"
SECONDS_PER_DAY = 86400
MICROSECONDS_PER_DAY = SECONDS_PER_DAY * 1e6

real = xr.open_dataset("with_real_forcing/autoregressive_predictions.nc")[VAR]

artificial = xr.open_dataset("with_artificial_forcing/autoregressive_predictions.nc")[
    VAR
]

real, artificial = xr.align(real, artificial, join="exact")


weights = np.cos(np.deg2rad(real["lat"]))
lead_days = real["time"].values / MICROSECONDS_PER_DAY

real_mm_day = real * SECONDS_PER_DAY
artificial_mm_day = artificial * SECONDS_PER_DAY

rmse = np.sqrt(
    ((artificial_mm_day - real_mm_day) ** 2).weighted(weights).mean(("lat", "lon"))
).squeeze(drop=True)

plt.plot(lead_days, rmse.values)
plt.xlabel("Forecast lead time (days)")
plt.ylabel("Spatial RMSE (mm/day)")
plt.title("Precipitation difference: artificial vs real forcing")
plt.tight_layout()
plt.savefig("precipitation_difference.png", dpi=150)
plt.close()

print("Saved precipitation_difference.png")

real_mean = real_mm_day.weighted(weights).mean(("lat", "lon")).squeeze(drop=True)

artificial_mean = (
    artificial_mm_day.weighted(weights).mean(("lat", "lon")).squeeze(drop=True)
)

plt.plot(lead_days, real_mean.values, label="Real forcing")
plt.plot(lead_days, artificial_mean.values, label="Artificial forcing")
plt.xlabel("Forecast lead time (days)")
plt.ylabel("Global mean rainfall (mm/day)")
plt.title("Global mean predicted rainfall")
plt.legend()
plt.tight_layout()
plt.savefig("global_mean_precipitation.png", dpi=150)
plt.close()

print("Saved global_mean_precipitation.png")
