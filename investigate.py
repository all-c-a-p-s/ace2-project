import xarray as xr


print("INITIAL CONDITIONS:")

ds = xr.open_dataset("initial_conditions/ic_2020.nc")
print(ds)

_ = input("\ninput anything to inspect forcing data\n\n")

print("FORCING DATA:")

ds = xr.open_dataset("forcing_data/forcing_2020.nc")
print(ds)


paths = [
    "autoregressive_predictions.nc",
    "annual_diagnostics.nc",
    "autoregressive_target.nc",
    "initial_condition.nc",
    "mean_diagnostics.nc",
    "power_spectrum_diagnostics.nc",
    "restart.nc",
    "time_mean_diagnostics.nc",
    "monthly_mean_predictions.nc",
    "monthly_mean_target.nc",
]

for path in paths:
    _ = input("\ninput anything to inspect next file\n\n")

    rel_path = "sample_output/" + path

    print(f"OUTPUT FILE '{path}':")

    ds = xr.open_dataset(rel_path)
    print(ds)
