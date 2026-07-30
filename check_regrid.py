import numpy as np
import xarray as xr

ace = xr.open_dataset("forcing_data/forcing_2020.nc")
sst = xr.open_dataset("sst_mean_ace_grid.nc")
ice = xr.open_dataset("sea_ice_mean_6h_ace_grid.nc")

for name, ds in [("sst", sst), ("ice", ice)]:
    print(name)
    print("orientation:", ds.latitude.values[[0, -1]])
    print(
        "max latitude difference:",
        np.max(np.abs(ds.latitude.values - ace.latitude.values)),
    )
    print(
        "close:",
        np.allclose(
            ds.latitude.values,
            ace.latitude.values,
            rtol=0,
            atol=1e-10,
        ),
    )
