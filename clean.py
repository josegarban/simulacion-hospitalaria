import pprint, datetime

import pandas as pd
import numpy as np
import matplotlib as mpl
from matplotlib.ticker import StrMethodFormatter
from matplotlib import axes

def read_txt(filename):
    """
    Enter a txt file with alternate lines with keys(integers) and names,
    and convert it into a list of the form [{int: str}]
    """
    file = open(filename, 'r')
    temp = [line.replace("\n", "") for line in file.readlines()]
    result = []
    for t in list(range(len(temp))):
        if t % 2 == 0:
            result.append({int(temp[t]): temp[t+1]})
    pprint.pprint(result)
    return result


def convert(filename, delimiter=","):
    """
    Returns a tuple with the dataframe and the column names
    """
    # Get dataframe and headers from csv
    df = pd.read_csv(filename, delimiter,header=0)
    header_list = list(df.columns)

    # Print what we got
    print("\nObtained a dataframe with the following fields:")
    print("\n", df.dtypes, "\n")
    print("\nDataframe description:")
    print("#"*100+"\n", df, "\n"+"#"*100+"\n")
    print("\nHeaders:")
    print("#"*100,"\n", header_list, "\n"+"#"*100+"\n")

    return (df, header_list)


def customizechart(chart, title, xlabel, ylabel):
    """
    Custom chart style
    """
    chart = chart[0]
    for x in chart:

        # Despine
        x.spines['right'].set_visible(False)
        x.spines['top'].set_visible(False)
        x.spines['left'].set_visible(False)

        # Switch off ticks
        x.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")

        # Draw horizontal axis lines
        vals = x.get_yticks()
        for tick in vals:
            x.axhline(y=tick, linestyle='dashed', alpha=0.4, color='#eeeeee', zorder=1)

        # Remove title
        x.set_title(title)

        # Set x-axis label
        x.set_xlabel(xlabel, labelpad=20, weight='bold', size=12)
        # Set y-axis label

        x.set_ylabel(ylabel, labelpad=20, weight='bold', size=12)
        # Format y-axis label
        x.yaxis.set_major_formatter(StrMethodFormatter('{x:,g}'))



def clean_column(df, column_name, error_values=[999]):
    """
    error_values is a list to be removed from column df[column_name]
    returns a dataframe with just one column
    """
    # Similar to cleaned = [x for x in df['age'] if x != 999]
    column = list(df[column_name][~df[column_name].isin(error_values)])
    # Creating a new dataframe
    cleaned = pd.DataFrame({column_name: column})
    # cleaned.columns = ['column_name']
    return cleaned


def clean_column_pair(df, column_name1, column_name2=None, error_values=[999]):
    """
    Create a single dataframe with just two columns
    """
    indexNames = []

    df = df[df[column_name1] != 999]
    if column_name2 is not None:
        df = df[df[column_name2] != 999]

    # if column_name2 is not None:
    #     df = df [[column_name1, column_name2]]
    #     indices = df.index.values.tolist()
    #     if column_name1 == column_name2:
    #         for e in error_values:
    #             indexNames = indexNames + [x for x in indices if df.iloc[x, 0] == e]
    #     else:
    #         for e in error_values:
    #             indexNames = indexNames + [x for x in indices if df.loc[x, column_name1] == e]
    #             indexNames = indexNames + [x for x in indices if df.loc[x, column_name2] == e]
    # else:
    #     df = df [[column_name1]]
    #     indices = df.index.values.tolist()
    #     for e in error_values:
    #         indexNames = indexNames + [x for x in indices if df.loc[x, column_name1] == e]
    # df = df.drop(indexNames)
    # print("Rows with error values:", indexNames)

    print("\nAbridged dataframe:")
    print("#"*100+"\n", df, "\n"+"#"*100+"\n")

    return df


def customdescribe(df, column_name, error_values=[999]):
    """
    Returns a custom description
    """
    cleaned = clean_column(df, column_name, error_values)
    cleaned.hist(bins=20)
    return None


def getdatetimes(df, column_name1, column_name2=None, error_values=[999]):
    """
    Converts one or two columns containing datetimes as strings to dataframes containing datetimes
    """
    column1 = clean_column(df, column_name1, error_values=[""])
    dates1 = pd.to_datetime(column1[column_name1], format='%Y-%m-%d %H:%M:%S')
    print(column_name1)
    print(dates1)

    if column_name2 is not None:
        column2 = clean_column(df, column_name2, error_values=[""])
        dates2 = pd.to_datetime(column2[column_name2], format='%Y-%m-%d %H:%M:%S')
        print("\n")
        print(column_name2)
        print(dates2)
        return (dates1, dates2)

    else:
        return dates1


def splitdatetime(df, column_name):
    """
    Add columns to dataframe with year, month, weekday, hour
    column_name: column containing datetime objects
    """
    df[column_name] = getdatetimes(df, column_name)
    df['year']  = [d.year for d in df[column_name]]
    df["month"] = [d.month for d in df[column_name]]
    # df["weekday"]  = [datetime.date(d.year, d.month, d.day).strftime("%A") for d in df[column_name]]
    df["weekday"]  = [datetime.date(d.year, d.month, d.day).isoweekday() for d in df[column_name]]
    df["hour"]  = [d.hour for d in df[column_name]]

    print("\nProcessed datetimes:")
    # pd.set_option('display.max_columns', None)
    # pd.set_option('display.max_rows', None)
    print("#"*100+"\n", df, "\n"+"#"*100+"\n")
    return df


def main ():
    """
    Test some functions
    """
    FILENAME = 'xrays_visits.csv'
    DELIMITER = ","
    ERROR_VALUES = [999]
    read_txt("departments.txt")
    # d = convert(FILENAME, DELIMITER)
    # customdescribe(d[0], 'age', ERROR_VALUES)
    #
    #
    # dt1 = getdatetimes(d[0], 'entry_date', 'exit_date', ERROR_VALUES)
    # dt2 = clean_column_pair(d[0], 'age', 'entry_date', ERROR_VALUES)
    #
    # dt3 = splitdatetime(d[0], 'entry_date')
    # dt4 = clean_column_pair(dt3, 'age', 'entry_date', ERROR_VALUES)

if __name__ == '__main__':
    main()
