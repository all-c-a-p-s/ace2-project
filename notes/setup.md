# Setup (assuming correct hardware, basic deps e.g. python installed etc)

The following should be sufficient to set everything up from scratch, if needed.

## Other Deps/Stuff

### Miniforge

```
wget \ https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
bash Miniforge3-Linux-x86_64.sh
source ~/.bashrc
```

### venv

```
conda create -n ace2 python=3.11 -y
conda activate ace2
```

### Torch/FME

```
python -m pip install --upgrade pip setuptools wheel
pip install torch
pip install fme huggingface_hub
```

## Obtaining Data

Historical initial conditions/forcing data can all be found [here](https://huggingface.co/allenai/ACE2-ERA5).

example to download from terminal:

to download forcing data/initial conditions from 2020 into a directory called `ace2`:

```
hf download allenai/ACE2-ERA5 \
    initial_conditions/ic_2020.nc \
    forcing_data/forcing_2020.nc \
    --local-dir ~/ace2
```
