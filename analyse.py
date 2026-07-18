import matplotlib.pyplot as plt
import numpy as np
import xarray as xr


REGULAR = "forcing_data/forcing_2020.nc"
ARTIFICIAL = "ecmwf_forcing/forcing_2020-01-01.nc"

regular = xr.open_dataset(REGULAR)
artificial = xr.open_dataset(ARTIFICIAL)

regular = regular.sel(time=artificial.time)
weights = np.cos(np.deg2rad(artificial.latitude))


def analyse(variable):
    difference = artificial[variable] - regular[variable]

    mean_difference = difference.weighted(weights).mean(("latitude", "longitude"))

    mean_absolute_difference = (
        abs(difference).weighted(weights).mean(("latitude", "longitude"))
    )

    return mean_difference, mean_absolute_difference


fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

for axis, variable, unit in [
    (axes[0], "surface_temperature", "K"),
    (axes[1], "sea_ice_fraction", "fraction"),
]:
    mean, mean_absolute = analyse(variable)

    axis.plot(artificial.time, mean, label="Mean difference")
    axis.plot(
        artificial.time,
        mean_absolute,
        label="Mean absolute difference",
    )

    axis.set_ylabel(unit)
    axis.set_title(variable)
    axis.legend()
    axis.grid()

axes[-1].set_xlabel("Time")

plt.tight_layout()
plt.savefig("forcing_differences.png", dpi=150)
plt.show()
