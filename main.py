import pandas as pd
import numpy as np
import matplotlib as plt
import pprint

import clean


def timedeltas_hist_bylength(later, before):
    """
    later: later datetimes, before: previous datetimes
    """
    intervals = [x for x in list(later-before)]
    intervals = pd.to_numeric(intervals, errors='ignore')
    intervals = pd.DataFrame({'interval': intervals})
    intervals = ((1/60) * intervals / np.timedelta64(1, 's')).astype(int)
    print("\n"+"#"*50)
    print("Intervals:")
    print(intervals)
    ax = intervals.hist(bins=20)
    title, xlabel, ylabel = "Time spent at the X-ray unit", "minutes", "patients"
    clean.customizehistogram(ax, title, xlabel, ylabel)
    return None


def timedeltas_hist_times_total(df, error_values=[999]):
    """
    Show histograms by hour, weekday, etc.
    Criteria: list of criteria in another column
    """
    df_ = clean.splitdatetime(df, 'entry_date')
    df__ = clean.clean_column_pair(df_, 'age', 'entry_date', error_values)

    ax1 = df__.hist(column='hour', bins=24)
    title, xlabel, ylabel = "All patients entering the X-ray unit by hour", "hour", "patients"
    clean.customizehistogram(ax1, title, xlabel, ylabel)

    ax2 = df__.hist(column='weekday', bins=7)
    title, xlabel, ylabel = "All patients entering the X-ray unit by weekday", "weekday", "patients"
    clean.customizehistogram(ax2, title, xlabel, ylabel)



def timedeltas_hist_times_by_criteria(df, error_values=[999], criteria_name=None, criteria=None):
    """
    Show histograms by hour, weekday, etc.
    Criteria: list of criteria in another column
    """
    df_ = clean.splitdatetime(df, 'entry_date')
    df__ = clean.clean_column_pair(df_, 'age', 'entry_date', error_values)

    if criteria_name is not None and criteria is not None:
        # Show criteria
        print(criteria_name)
        pprint.pprint(criteria)

        for c in criteria:
            key = list(c.keys())[0]
            value = c[key]

            # Don't make empty charts
            if df[df[criteria_name]==key].count()[criteria_name] > 0:
                print("Filtering by criteria:", criteria_name, "=", "(", key, ",", value, ")")
                d_sub = df__.loc[df[criteria_name] == key]

                ax = d_sub.hist(column='hour', bins=24)
                title, xlabel, ylabel = str(key) + " " + value, "hour", "patients"
                clean.customizehistogram(ax, title, xlabel, ylabel)

                ax = d_sub.hist(column='weekday', bins=7)
                title, xlabel, ylabel = str(key) + " " + value, "weekday", "patients"
                clean.customizehistogram(ax, title, xlabel, ylabel)

    else:
        # If no criteria are provided, then it will just return the total
        timedeltas_hist_times_total(df, error_values)

    return None


def timedeltas_bars_times_total(df, error_values=[999]):
    """
    Show bar chart by hour, weekday, etc.
    Criteria: list of criteria in another column
    """
    df_ = clean.splitdatetime(df, 'entry_date')
    df__ = clean.clean_column_pair(df_, 'age', 'entry_date', error_values)

    title, x_axisname, y_axisname = "All patients entering the X-ray unit by weekday", "weekday", "patients"
    ax1 = clean.build_count_barchart(df__, title, x_axisname, y_axisname)
    clean.customizechart(ax1, title, x_axisname, y_axisname)

    title, x_axisname, y_axisname = "All patients entering the X-ray unit by hour", "hour", "patients"
    ax2 = clean.build_count_barchart(df__, title, x_axisname, y_axisname)
    clean.customizechart(ax2, title, x_axisname, y_axisname)



def main ():
    FILENAME = 'xrays_visits.csv'
    DELIMITER = ","
    ERROR_VALUES = [999]
    DEPARTMENTS = clean.read_txt("departments.txt")

    d = clean.convert(FILENAME, DELIMITER)
    df1 = clean.getdatetimes(d[0], 'entry_date', 'exit_date', ERROR_VALUES)

    timedeltas_hist_bylength(df1[1], df1[0])
    timedeltas_hist_times_total(d[0], ERROR_VALUES)
    # timedeltas_hist_times_by_criteria(d[0], ERROR_VALUES, "department", DEPARTMENTS)

    timedeltas_bars_times_total(d[0], ERROR_VALUES)


if __name__ == '__main__':
    main()
