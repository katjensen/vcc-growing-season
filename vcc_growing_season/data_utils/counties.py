from pathlib import Path
from typing import Union

import pandas as pd


def load_counties_by_state(
    year: int, month: int, variable_name: str, state: str, workdir: Union[str, Path]
) -> pd.DataFrame:

    # Create header
    # Add day-of-month'
    days = [str(n) for n in range(1, 32)]
    colnames = ["typ", "id", "name", "year", "month", "variable"] + days

    # Build filename and load dataframe
    year = str(year)
    month = str(month).zfill(2)

    typ = "scaled.csv"
    filename = "-".join([variable_name, year + month, "cty", typ])

    df = pd.read_csv(workdir.joinpath(filename), names=colnames, na_values=-999.99)

    # Filter dataframe to those with a US state name containing state kwarg
    if state is None:
        pass
    else:
        df = df[df["name"].str.contains(state)]

    # Transpose and then convert the index to timestamps
    df = df.set_index("name").T
    df = df.loc["1":]
    timestamps = ["-".join([year, month, day.zfill(2)]) for day in df.index]

    # Return dataframe
    df["date"] = timestamps
    df = df.set_index("date")

    return df.astype(float)
