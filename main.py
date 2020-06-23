import pandas as pd
import numpy as np
import matplotlib as mpl
import pprint

import clean


def timedeltas_hist_bylength(later, before):
    """
    later: later datetimes, before: previous datetimes
    """
    intervals = [x for x in list(later-before)]
    intervals = pd.to_numeric(intervals, errors='ignore')
    intervals = pd.DataFrame({'interval': intervals})
    intervals = (intervals / np.timedelta64(1, 's')).astype(int)
    print("\n"+"#"*50)
    print("Intervals:")
    print(intervals)
    intervals.hist(bins=20)
    return None


def timedeltas_hist_byhour(later, before):
    """
    later: later datetimes, before: previous datetimes
    """

    return None



def main ():
    FILENAME = 'xrays_visits.csv'
    DELIMITER = ","
    ERROR_VALUES = [999]

    d = clean.convert(FILENAME, DELIMITER)

    dt1 = clean.getdatetimes(d[0], 'entry_date', 'exit_date', ERROR_VALUES)
    timedeltas_hist_bylength(dt1[1], dt1[0])

    dt2 = clean.clean_column_pair(d[0], 'entry_date', 'age', ERROR_VALUES)
    ax1 = dt2.plot.scatter(x='age', y='entry_date', c='DarkBlue')

if __name__ == '__main__':
    main()
