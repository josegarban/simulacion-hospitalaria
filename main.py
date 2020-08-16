import pandas as pd
import numpy as np
import matplotlib as plt
import pprint

import clean

MESSAGES = {
            "Filtering by criteria:":
                {"en":"Filtering by criteria:", "es":"Filtrando por criterios"},
            "Time spent at the X-ray unit":
                {"en":"Time spent at the X-ray unit", "es":"Tiempo en la unidad de rayos X"},
            "minutes":
                {"en":"minutes", "es":"minutos"},
            "Intervals:":
                {"en":"Intervals:", "es":"Intervalos:"},
            "patients":
                {"en":"patients", "es":"pacientes"},
            "All patients entering the X-ray unit by age":
                {"en":"All patients entering the X-ray unit by age", "es":"Pacientes entrando a la unidad de rayos X por edad"},
            "All patients entering the X-ray unit by hour":
                {"en":"All patients entering the X-ray unit by hour", "es":"Pacientes entrando a la unidad de rayos X por hora"},
            "All patients entering the X-ray unit by weekday":
                {"en":"All patients entering the X-ray unit by weekday", "es":"Pacientes entrando a la unidad de rayos X por dia de la semana"},
            "weekday":
                {"en":"weekday", "es":"dia de la semana"},
            "age":
                {"en":"age", "es":"edad"},
            "hour":
                {"en":"hour", "es":"hora"},
            "incoming patients":
                {"en":"incoming patients", "es":"pacientes entrantes"},
            "All incoming patients by ":
                {"en":"All incoming patients by ", "es":"Todos los pacientes entrantes por "},
            "Error: no list of columns to chart were provided in input.":
                {"en":"Error: no list of columns to chart were provided in input.", "es":"No se ingresó una lista de columnas para graficar."},
            "No criteria or columns were given, the total will be used.":
                {"en":"No criteria or columns were given, the total will be used.", "es":"No se aportaron criterios o columnas, se usará el total."},
            }


def timedeltas_hist_bylength(later, before, lang="en", messages=MESSAGES):
    """
    Total of everything in a histogram
    later: later datetimes, before: previous datetimes
    """
    intervals = [x for x in list(later-before)]
    intervals = pd.to_numeric(intervals, errors='ignore')
    intervals = pd.DataFrame({'interval': intervals})
    intervals = ((1/60) * intervals / np.timedelta64(1, 's')).astype(int)
    print("\n"+"#"*50)
    print(messages["Intervals:"][lang])
    print(intervals)
    ax = intervals.hist(bins=20)
    title, xlabel, ylabel = messages["Time spent at the X-ray unit"][lang], messages["minutes"][lang], messages["patients"][lang]
    clean.customizehistogram(ax, title, xlabel, ylabel)
    return None


def timedeltas_hist_times_total(df, error_values=[999], language="en", messages=MESSAGES):
    """
    Show histograms by hour, weekday, etc.
    Criteria: list of criteria in another column
    """
    df_ = clean.splitdatetime(df, clean.COLUMN_NAMES['entry_date'][language])
    df__ = clean.clean_column_pair(df_, clean.COLUMN_NAMES['age'][language], clean.COLUMN_NAMES['entry_date'][language], error_values)

    ax1 = df__.hist(column=clean.COLUMN_NAMES['hour'][language], bins=24)
    title, xlabel, ylabel = messages["All patients entering the X-ray unit by hour"][language],\
                            messages["hour"][language], messages["patients"][language]
    clean.customizehistogram(ax1, title, xlabel, ylabel)

    ax2 = df__.hist(column=clean.COLUMN_NAMES['weekday'][language], bins=7)
    title, xlabel, ylabel = messages["All patients entering the X-ray unit by weekday"]["language"],\
                            messages["weekday"][language], messages["patients"][language]
    clean.customizehistogram(ax2, title, xlabel, ylabel)

    ax3 = df__.hist(column=clean.COLUMN_NAMES['age'][language], bins=20)
    title, xlabel, ylabel = messages["All patients entering the X-ray unit by weekday"]["language"],\
                            messages["weekday"][language], messages["patients"][language]
    clean.customizehistogram(ax3, title, xlabel, ylabel)



def timedeltas_hist_times_by_criteria(df, error_values=[999], criteria_name=None, criteria=None, language="en", messages=MESSAGES):
    """
    Show histograms by hour, weekday, etc.
    Criteria: list of criteria in another column
    """
    df_ = clean.splitdatetime(df, clean.COLUMN_NAMES['entry_date'][language])
    df__ = clean.clean_column_pair(df_, clean.COLUMN_NAMES['age'][language], clean.COLUMN_NAMES['entry_date'][language], error_values)

    if criteria_name is not None and criteria is not None:
        # Show criteria
        print(criteria_name)
        pprint.pprint(criteria)

        for c in criteria:
            key = list(c.keys())[0]
            value = c[key]

            # Don't make empty charts
            if df[df[criteria_name]==key].count()[criteria_name] > 0:
                print(messages["Filtering by criteria:"][language], criteria_name, "=", "(", key, ",", value, ")")
                d_sub = df__.loc[df[criteria_name] == key]

                ax = d_sub.hist(column=clean.COLUMN_NAMES['hour'][language], bins=24)
                title, xlabel, ylabel = str(key) + " " + value, messages["hour"][language], messages["patients"][language]
                clean.customizehistogram(ax, title, xlabel, ylabel)

                ax = d_sub.hist(column=clean.COLUMN_NAMES['weekday'][language], bins=7)
                title, xlabel, ylabel = str(key) + " " + value, messages["weekday"][language], messages["patients"][language]
                clean.customizehistogram(ax, title, xlabel, ylabel)

    else:
        # If no criteria are provided, then it will just return the total
        timedeltas_hist_times_total(df, error_values)

    return None



def timedeltas_bars_times_total(df, columns=None, error_values=[999], language="en", messages=MESSAGES):
    """
    Show bar chart by hour, weekday, etc.
    columns: columns to show
    Criteria: list of criteria in another column
    """
    if columns is not None:
        df_ = clean.splitdatetime(df, clean.COLUMN_NAMES['entry_date'][language], language)
        df__ = clean.clean_column_pair(df_, clean.COLUMN_NAMES['age'][language], clean.COLUMN_NAMES['entry_date'][language], error_values)

        for column in columns:
            title, x_axisname, y_axisname = messages["All incoming patients by "][language]+column, column, messages["patients"][language]
            ax1 = clean.build_count_barchart(df__, title, x_axisname, y_axisname)
            clean.customizechart(ax1, title, x_axisname, y_axisname)

    else:
        print(messages["Error: no list of columns to chart were provided in input."][language])



def timedeltas_bars_times_by_criteria(df, columns=None, error_values=[999], criteria_name=None, criteria=None, language="en", messages=MESSAGES):
    """
    Show histograms by hour, weekday, etc.
    Criteria: list of criteria in another column
    """

    if columns is not None:
        df_ = clean.splitdatetime(df, clean.COLUMN_NAMES['entry_date'][language], language)
        df__ = clean.clean_column_pair(df_, clean.COLUMN_NAMES['age'][language], clean.COLUMN_NAMES['entry_date'][language], error_values)
    else:
        print(messages["Error: no list of columns to chart were provided in input."][language])

    if criteria_name is not None and criteria is not None:

        # Get categories in the whole chart, not the filtered one
        for column in columns:
            categories = [ x for x in pd.unique(pd.Series(df__[column])) ]
            categories.sort()

            # Show criteria
            print(criteria_name)
            pprint.pprint(criteria)

            for c in criteria:
                key = list(c.keys())[0]
                value = c[key]

                # Don't make empty charts
                if df__[df__[criteria_name]==key].count()[criteria_name] > 0:
                    print(messages["Filtering by criteria:"][language]+" {0} = ({1}, {2})".format(criteria_name, key, value))
                    d_sub = df__.loc[df__[criteria_name] == key]

                    title, x_axisname, y_axisname = "{0} {1}: {2} by {3}".format(\
                        criteria_name.capitalize(), key, value, column), column, messages["incoming patients"][language]
                    ax1 = clean.build_count_barchart(d_sub, title, x_axisname, y_axisname, categories)
                    clean.customizechart(ax1, title, x_axisname, y_axisname)

    else:
        # If no criteria are provided, then it will just return the total
        print(messages["No criteria or columns were given, the total will be used."][language])
        timedeltas_bars_times_total(df, error_values, columns)

    return None



def main (language="es", messages=MESSAGES):

    FILENAME = 'xrays_visits.csv'
    DELIMITER = ","
    ERROR_VALUES = [999]

    COLUMNS_4 = [clean.COLUMN_NAMES["weekday"][language],
                 clean.COLUMN_NAMES["hour"][language],
                 clean.COLUMN_NAMES["age"][language],
                 clean.COLUMN_NAMES["gender"][language],
                ]
    COLUMNS_2 = [clean.COLUMN_NAMES["weekday"][language],
                 clean.COLUMN_NAMES["hour"][language]]

    COLUMN_CRITERIA = clean.COLUMN_NAMES["department"][language]
    COLUMN_CRITERIA_CATEGORIES = clean.read_txt("departments.txt")

    d = clean.convert(FILENAME, DELIMITER)
    d_t = clean.column_translator(d[0], language)
    # Add processed date fields
    df1 = clean.getdatetimes(d_t, clean.COLUMN_NAMES['entry_date'][language], clean.COLUMN_NAMES['exit_date'][language], ERROR_VALUES)

    # Total of everything
    timedeltas_hist_bylength(df1[1], df1[0], language, messages)

    # Totals by COLUMNS_4
    timedeltas_bars_times_total(d_t, COLUMNS_4, ERROR_VALUES, language, messages)

    # Charts by COLUMNS_2 by department
    timedeltas_bars_times_by_criteria(d_t, COLUMNS_2, ERROR_VALUES, COLUMN_CRITERIA, COLUMN_CRITERIA_CATEGORIES, language, messages)


if __name__ == '__main__':
    main()
