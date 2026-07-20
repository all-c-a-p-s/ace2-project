import numpy as np
import matplotlib.pyplot as plt
import xarray as xr

VAR = "PRATEsfc"

real = xr.open_dataset("with_real_forcing/autoregressive_predictions.nc")[VAR]

artificial = xr.open_dataset("with_artificial_forcing/autoregressive_predictions.nc")[
    VAR
]

real, artificial = xr.align(real, artificial, join="exact")

lat = "latitude" if "latitude" in real.dims else "lat"
lon = "longitude" if "longitude" in real.dims else "lon"

weights = np.cos(np.deg2rad(real[lat]))

rmse = np.sqrt(((artificial - real) ** 2).weighted(weights).mean((lat, lon)))
rmse = rmse.squeeze(drop=True)

lead_days = rmse["time"] / (1e9 * 60 * 60 * 24)
rmse_mm_day = rmse * 86400

plt.plot(lead_days, rmse_mm_day)
plt.title("Precipitation difference: artificial vs real forcing")
plt.xlabel("Forecast lead time (days)")
plt.ylabel("Spatial RMSE (mm/day)")
plt.tight_layout()
plt.savefig("precipitation_difference.png", dpi=150)
plt.show()
