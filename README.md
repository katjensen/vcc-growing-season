# vcc-growing-season
An open-source project investigating regional changes in the growing season across the US.

Temperature data is sourced from the [NCEI nClimGrid-Daily ](https://www.ncei.noaa.gov/products/land-based-station/nclimgrid-daily) product


---
## Installation

This project's dependencies are managed with Poetry. Learn more about its basic usage [here](https://python-poetry.org/docs/basic-usage/)! 

If you prefer to not use Poetry and opt for a quick installation, you can simply use the `requirements.txt` with `pip` or `conda`

### 1. Clone Repo
```bash
git clone git@github.com:katjensen/vcc-growing-season.git
```
### 2. Install Poetry (if not already installed on system) 
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 3. Set up Python environment
Create and activate a fresh, new python environment using your Python manager of choice (e.g conda or pyenv). This project requires Python version 3.9 or greater.

```bash
conda create -n vcc-growing-season python=3.9
conda activate vcc-growing-season
```

### 4. Install package

You can install project dependencies, along with pre-commit git hooks, by:
```bash
make install
```

If you want, you may install this `vcc-growing-season` library in editable mode once dependencies have been installed (and your environment is activated) by:
```bash
pip install -e .
```

### 6. Some additional tips about Poetry
To add a package to your project using poetry CLI,
```bash
poetry add "[your_package]"
```

You can also manually update `pyproject.toml` to include a new dependency (or change Python verions or existing dependency versions) manually. This will require you to recreate the `poetry.lock` file in the project, which you can do by following the command below. 
```bash
poetry update
```
