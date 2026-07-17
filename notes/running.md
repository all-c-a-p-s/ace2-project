# Running/Config

## Model Config

- most params are quite obvious
- `forward_steps_in_memory: N` = the last `N` autoregressive steps will be saved to the output file
- `num_data_workers: N` for the forcing loader = `N` background processes will load forcing data (`nproc` = 4 on this VM)
- `save_monthly_files` = should we save mean values of variables over each month (YES)
- `save_prediction_files` = shoudl we save autoregressive predictions (as well as diagnostics and maybe monthly predictions)

## Running the model
- activate venv: `conda activate ace2`
- validate input data (using `test.yaml` for config): `python -m fme.ace.validate_config test.yaml --config_type inference`
- actually run the model (using `test.yaml` for config): `python -m fme.ace.inference test.yaml`
