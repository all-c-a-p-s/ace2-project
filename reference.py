import numpy as np
import matplotlib.pyplot as plt
import xarray as xr

VAR = "PRATEsfc"
SECONDS_PER_DAY = 86_400
MICROSECONDS_PER_DAY = 86_400 * 1e6

runs = {
    "Real forcing": xr.open_dataset("with_real_forcing/autoregressive_predictions.nc")[
        VAR
    ],
    "Artificial forcing": xr.open_dataset(
        "with_artificial_forcing/autoregressive_predictions.nc"
    )[VAR],
}

for label, rain in runs.items():
    rain = rain.squeeze(drop=True) * SECONDS_PER_DAY
    weights = np.cos(np.deg2rad(rain["lat"]))
    lead_days = rain["time"].values / MICROSECONDS_PER_DAY

    global_mean = rain.weighted(weights).mean(("time", "lat", "lon"))

    zero_rmse = np.sqrt((rain**2).weighted(weights).mean(("lat", "lon")))

    mean_rmse = np.sqrt(
        ((rain - global_mean) ** 2).weighted(weights).mean(("lat", "lon"))
    )

    plt.plot(lead_days, zero_rmse, label=f"{label}: zero")
    plt.plot(lead_days, mean_rmse, label=f"{label}: global mean")

    print(f"{label} global mean: {global_mean.item():.3f} mm/day")

plt.xlabel("Forecast lead time (days)")
plt.ylabel("Spatial RMSE (mm/day)")
plt.title("Reference prediction errors")
plt.legend()
plt.tight_layout()
plt.savefig("reference_rmse.png", dpi=150)
plt.show()
