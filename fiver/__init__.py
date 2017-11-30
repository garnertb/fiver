#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of unit-utilization.
# https://github.com/garnertb/fiver

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2017, Tyler Garner <garnertb@prominentedge.com>
from __future__ import division

import click
import os
import numpy as np
import pandas as pd
import sys

from datetime import datetime, time, timedelta, date
from multiprocessing import Pool

def create_data_frame(file_path, timezone):
    df = pd.read_csv(file_path)

    # Drop nan values.
    df = df.dropna(axis=0, how='any')

    # Tranform measures to times only instead of datetime.
    df['dispatched'] = pd.to_datetime(df['dispatched'], utc=True)
    df['dispatched'] = df['dispatched'].dt.tz_convert(timezone)

    df['available'] = pd.to_datetime(df['available'], utc=True)
    df['available'] = df['available'].dt.tz_convert(timezone)

    return df


def create_results_df(results, units):

    params = {
        'date_time_bin': [row[0] for row in results],
        'counts': [row[1] for row in results],
        'units': [row[2] for row in results],
    }

    if units is not None:
        params['units_available'] = map(lambda n: units - n, params['counts'])
        params['utilization'] = map(lambda n: round((n / units) * 100, 2), params['counts'])

    counts_df = pd.DataFrame(params)

    counts_df.sort_values(by='counts', ascending=False, inplace=True)
    counts_df.index = np.arange(1, len(counts_df) + 1)

    columns = filter(lambda n: n in list(counts_df.columns), ['date_time_bin', 'counts', 'units',
        'units_available', 'utilization'])

    return counts_df[columns]


def estimate_nonavailable(time_range):
    # Transform time range to string.
    date_str = time_range.isoformat()
    sys.stdout.write('\rEvaluating time range: {0}'.format(date_str))
    sys.stdout.flush()

    disp = ((df['dispatched'] > time_range) &
            (df['dispatched'] <= time_range + timedelta(minutes=5)))

    # If available value is between time_range bin.
    av = ((df['available'] > time_range) &
          (df['available'] <= time_range + timedelta(minutes=5)))

    # If time_range is between available and dispatched values.
    between = ((time_range > df['dispatched']) &
               (time_range  < df['available']))

    na_df = df.loc[(disp | av | between)]

    return date_str, na_df.shape[0], ','.join(na_df['unit_id'].unique())

@click.command()
@click.argument('input',  type=click.File('rb'))
@click.argument('start')
@click.argument('end')
@click.option('--pool', default=1,  help='Number of processes to use.')
@click.option('--units', default=None,  help='Total number of units available.', type=int)
@click.option('--count', default=5,  help='Number of results to return.', type=int)
@click.option('--timezone', default='US/Eastern',  help='Timezone of data.')
@click.option('--save/--no-save', default=False,  help='Save the file as a csv.')
def main(input, start, end, pool, units, count, timezone, save):
    """
    Calculates the 5 minute time frame with the most units out of service.
    """
    global df
    df = create_data_frame(input, timezone)

    # Create time bins from a given year.
    time_ranges = pd.date_range(start, end, freq='5min', tz=timezone)[:-1]

    p = Pool(pool)
    results = p.map(estimate_nonavailable, time_ranges)

    # Create results dataframe.
    counts_df = create_results_df(results, units)

    if save:
        print('\nSaving results in csv file...')
        with open('utilization-rate-{0}-{1}.csv'.format(start, end), "w") as f:
            counts_df.to_csv(f)

    print("\n==============================================================\n")
    print(counts_df.head(count))

if __name__ == '__main__':
    main()
