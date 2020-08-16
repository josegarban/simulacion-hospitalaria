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
            "divisions":
                {"en":"divisions", "es":"divisiones"},
            "count":
                {"en":"count", "es":"cuenta"},
            "Histogram bins:":
                {"en":"Histogram bins:", "es":"Rangos del histograma:"},
            }


def timedeltas_hist_bylength(later, before, lang="en", messages=MESSAGES, print_intermediate=True):
    """
    Total of everything in a histogram
    later: later datetimes, before: previous datetimes
    """
    intervals = [x for x in list(later-before)]
    intervals = pd.to_numeric(intervals, errors='ignore')
    intervals = pd.DataFrame({'interval': intervals})
    intervals = ((1/60) * intervals / np.timedelta64(1, 's')).astype(int)

    if print_intermediate:
        print("\n"+"#"*50)
        print(messages["Intervals:"][lang])
        print(intervals)
        print("\n")

    ax = intervals.hist(bins=20)
    title, xlabel, ylabel = messages["Time spent at the X-ray unit"][lang], messages["minutes"][lang], messages["patients"][lang]
    clean.customizehistogram(ax, title, xlabel, ylabel)

    count, divisions = np.histogram(intervals)
    columns = [messages["divisions"][lang], messages["count"][lang]]
    data = np.concatenate( ([[x] for x in divisions.tolist()[1:]] , [[x] for x in count.tolist()]) , axis=1)
    output = pd.DataFrame(data=data, index=rows, columns=columns)

    if print_intermediate:
        print(messages["Histogram bins:"][lang])
        print(output)
        print("\n")
    return output


def timedeltas_hist_times_total(df, error_values=[999], language="en", messages=MESSAGES, column_names=clean.COLUMN_NAMES):
    """
    Show histograms by hour, weekday, etc.
    Criteria: list of criteria in another column
    """
    df_ = clean.splitdatetime(df, column_names['entry_date'][language], language, column_names, print_intermediate)
    df__ = clean.clean_column_pair(df_, column_names['age'][language], column_names['entry_date'][language], error_values)

    ax1 = df__.hist(column=column_names['hour'][language], bins=24)
    title, xlabel, ylabel = messages["All patients entering the X-ray unit by hour"][language],\
                            messages["hour"][language], messages["patients"][language]
    clean.customizehistogram(ax1, title, xlabel, ylabel)

    ax2 = df__.hist(column=column_names['weekday'][language], bins=7)
    title, xlabel, ylabel = messages["All patients entering the X-ray unit by weekday"]["language"],\
                            messages["weekday"][language], messages["patients"][language]
    clean.customizehistogram(ax2, title, xlabel, ylabel)

    ax3 = df__.hist(column=column_names['age'][language], bins=20)
    title, xlabel, ylabel = messages["All patients entering the X-ray unit by weekday"]["language"],\
                            messages["weekday"][language], messages["patients"][language]
    clean.customizehistogram(ax3, title, xlabel, ylabel)



def timedeltas_hist_times_by_criteria(  df,
                                        error_values=[999],
                                        criteria_name=None,
                                        criteria=None,
                                        language="en",
                                        messages=MESSAGES,
                                        column_names=clean.COLUMN_NAMES,
                                        print_intermediate=True):
    """
    Show histograms by hour, weekday, etc.
    Criteria: list of criteria in another column
    """
    df_ = clean.splitdatetime(df, column_names['entry_date'][language], language, column_names, print_intermediate)
    df__ = clean.clean_column_pair(df_, column_names['age'][language], column_names['entry_date'][language], error_values, print_intermediate)

    if criteria_name is not None and criteria is not None:
        # Show criteria
        if print_intermediate:
            print(criteria_name)
            pprint.pprint(criteria)

        for c in criteria:
            key = list(c.keys())[0]
            value = c[key]

            # Don't make empty charts
            if df[df[criteria_name]==key].count()[criteria_name] > 0:
                print("\n")
                print(messages["Filtering by criteria:"][language], criteria_name, "=", "(", key, ",", value, ")")
                d_sub = df__.loc[df[criteria_name] == key]

                ax = d_sub.hist(column=column_names['hour'][language], bins=24)
                title, xlabel, ylabel = str(key) + " " + value, messages["hour"][language], messages["patients"][language]
                clean.customizehistogram(ax, title, xlabel, ylabel)

                ax = d_sub.hist(column=column_names['weekday'][language], bins=7)
                title, xlabel, ylabel = str(key) + " " + value, messages["weekday"][language], messages["patients"][language]
                clean.customizehistogram(ax, title, xlabel, ylabel)

    else:
        # If no criteria are provided, then it will just return the total
        timedeltas_hist_times_total(df, error_values)

    return None



def timedeltas_bars_times_total(df,
                                columns=None,
                                error_values=[999],
                                language="en",
                                messages=MESSAGES,
                                column_names=clean.COLUMN_NAMES,
                                print_intermediate=True):
    """
    Show bar chart by hour, weekday, etc.
    columns: columns to show
    Criteria: list of criteria in another column
    Output: list of dataframes and related information
    """
    output = []

    if columns is not None:
        df_ = clean.splitdatetime(df, column_names['entry_date'][language], language, column_names, print_intermediate)
        df__ = clean.clean_column_pair(df_, column_names['age'][language], column_names['entry_date'][language], error_values, print_intermediate)

        # Create tables to be exported
        for c in columns:
            d_tab = df__.groupby(c)[column_names['duration'][language]].agg(['sum', 'min', 'mean', 'max', 'std'])
            output.append(d_tab)
        if print_intermediate:
            print(d_tab)

        for column in columns:
            title, x_axisname, y_axisname = messages["All incoming patients by "][language]+column, column, messages["patients"][language]
            ax1 = clean.build_count_barchart(df__, title, x_axisname, y_axisname)
            clean.customizechart(ax1, title, x_axisname, y_axisname)

        return output

    else:
        print(messages["Error: no list of columns to chart were provided in input."][language])
        return None


def timedeltas_bars_times_by_criteria(  df,
                                        columns=None,
                                        error_values=[999],
                                        criteria_name=None,
                                        criteria=None,
                                        language="en",
                                        messages=MESSAGES,
                                        column_names=clean.COLUMN_NAMES,
                                        print_intermediate=True):
    """
    Show bar charts by hour, weekday, etc.
    Criteria: list of criteria in another column
    Returns a list of dataframes that can be later styled
    """
    output = []

    if columns is not None:
        df_ = clean.splitdatetime(df, column_names['entry_date'][language], language, column_names, print_intermediate)
        df__ = clean.clean_column_pair(df_, column_names['age'][language], column_names['entry_date'][language], error_values, print_intermediate)
    else:
        print(messages["Error: no list of columns to chart were provided in input."][language])

    if criteria_name is not None and criteria is not None:

        # Get categories in the whole chart, not the filtered one
        for column in columns:
            categories = [ x for x in pd.unique(pd.Series(df__[column])) ]
            categories.sort()

            # Show criteria
            if print_intermediate:
                print(criteria_name)
                pprint.pprint(criteria)

            for c in criteria:
                key = list(c.keys())[0]
                value = c[key]

                # Don't make empty charts
                if df__[df__[criteria_name]==key].count()[criteria_name] > 0:
                    print("\n")
                    print(messages["Filtering by criteria:"][language]+" {0} = ({1}, {2})".format(criteria_name, key, value))
                    d_sub = df__.loc[df__[criteria_name] == key]
                    d_tab = d_sub.groupby("dia de la semana")['duración'].agg(['sum', 'min', 'mean', 'max', 'std'])
                    print(d_tab)
                    # Later: d_tab.styles
                    output.append([criteria_name, c, d_tab])

                    title, x_axisname, y_axisname = "{0} {1}: {2} by {3}".format(\
                        criteria_name.capitalize(), key, value, column), column, messages["incoming patients"][language]
                    ax1 = clean.build_count_barchart(d_sub, title, x_axisname, y_axisname, categories)
                    clean.customizechart(ax1, title, x_axisname, y_axisname)

    else:
        # If no criteria are provided, then it will just return the total
        print(messages["No criteria or columns were given, the total will be used."][language])
        timedeltas_bars_times_total(df, error_values, columns)

    return output



def main (language="es", messages=MESSAGES, column_names=clean.COLUMN_NAMES, print_intermediate=False):

    FILENAME = 'xrays_visits.csv'
    DELIMITER = ","
    ERROR_VALUES = [999]

    COLUMNS_4 = [column_names["weekday"][language],
                 column_names["hour"][language],
                 column_names["age"][language],
                 column_names["gender"][language],
                ]
    COLUMNS_2 = [column_names["weekday"][language],
                 column_names["hour"][language]]

    COLUMN_CRITERIA = column_names["department"][language]
    COLUMN_CRITERIA_CATEGORIES = clean.read_txt("departments.txt", print_intermediate)

    d = clean.convert(FILENAME, DELIMITER, print_intermediate)
    d_t = clean.column_translator(d[0], language, column_names, print_intermediate)
    # Add processed date fields
    df1 = clean.getdatetimes(d_t,
                             column_names['entry_date'][language],
                             column_names['exit_date'][language],
                             ERROR_VALUES, print_intermediate)

    # Total of everything
    histo_lbl = timedeltas_hist_bylength(df1[1],
                                         df1[0],
                                         language, messages, print_intermediate)

    # Totals by COLUMNS_4
    tables_totals = timedeltas_bars_times_total(d_t,
                                                COLUMNS_4,
                                                ERROR_VALUES,
                                                language, messages, column_names, print_intermediate)

    # Charts by COLUMNS_2 by department
    tables_by_criteria = timedeltas_bars_times_by_criteria( d_t,
                                                            COLUMNS_2,
                                                            ERROR_VALUES,
                                                            COLUMN_CRITERIA,
                                                            COLUMN_CRITERIA_CATEGORIES,
                                                            language, messages, column_names, print_intermediate)
    return (histo_lbl, tables_totals, tables_by_criteria)

if __name__ == '__main__':
    main()
