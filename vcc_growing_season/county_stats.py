from typing import List, Tuple

import attrs
import numpy as np
import pandas as pd
from scipy import stats


@attrs.define(slots=True, frozen=True)
class GrowingSeasons:
    county_list: List
    duration_days: pd.DataFrame
    season_start_doy: pd.DataFrame
    season_end_doy: pd.DataFrame

    def get_linear_trends(self, clean_county_string: bool = True) -> pd.DataFrame:
        # apply regression over years per county
        lr_results = []

        for county in self.county_list:
            if clean_county_string:
                county_str = county[4:]  # remove the 'XX: ' part of str for joining with county boundaries
            else:
                county_str = county

            lr_growing_season = stats.linregress(self.duration_days.index, self.duration_days[county])
            lr_season_start = stats.linregress(self.season_start_doy.index, self.season_start_doy[county])
            lr_season_end = stats.linregress(self.season_end_doy.index, self.season_end_doy[county])

            lr_results.append(
                [
                    county_str,
                    lr_growing_season.slope,
                    lr_growing_season.pvalue,
                    lr_season_start.slope,
                    lr_season_start.pvalue,
                    lr_season_end.slope,
                    lr_season_end.pvalue,
                ]
            )

        return pd.DataFrame(
            lr_results,
            columns=[
                "namelsad",
                "growing_season_duration_slope",
                "growing_season_duration_pvalue",
                "season_start_slope",
                "season_start_pvalue",
                "season_end_slope",
                "season_end_pvalue",
            ],
        )


def tmin_to_growing_season(tmin: pd.DataFrame, frost_threshold_celsius: float = 0) -> GrowingSeasons:
    """Given time series data of min daily temperatures, estimate annual growing seasons

    Definition of the growing season is sensitive to threshold used, e.g.
        - mild frost: 0C (32F)
        - moderate frost: -2.22222 (28F)
        - severe frost: -4.44444C (24F)
    """

    growing_season = []
    season_start = []
    season_end = []

    years = np.arange(tmin.index.year.min(), tmin.index.year.max() + 1)

    for year in years:
        # find last spring frost - look at first half of the year (in reverse !)
        tmin_subset = tmin[(tmin.index.year == year) & ((tmin.index.month < 7))][::-1]  # reverse the series HERE !
        last_spring_frost = tmin_subset.index[
            tmin_subset.apply(lambda x: np.argmax(x < frost_threshold_celsius)).values
        ]

        # find first fall frost - look at second half of the year
        tmin_subset = tmin[(tmin.index.year == year) & ((tmin.index.month > 7))]
        first_fall_frost = tmin_subset.index[tmin_subset.apply(lambda x: np.argmax(x < frost_threshold_celsius)).values]

        growing_season_length = (first_fall_frost - last_spring_frost).days

        # save data
        growing_season.append(growing_season_length)
        season_start.append([d.dayofyear for d in last_spring_frost])
        season_end.append([d.dayofyear for d in first_fall_frost])

    return GrowingSeasons(
        county_list=tmin.columns,
        duration_days=pd.DataFrame(growing_season, index=years, columns=tmin.columns),
        season_start_doy=pd.DataFrame(season_start, index=years, columns=tmin.columns),
        season_end_doy=pd.DataFrame(season_end, index=years, columns=tmin.columns),
    )
