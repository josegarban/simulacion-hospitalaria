import pandas as pd
import matplotlib as mpl
import pprint

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


def clean_column(df, column_name, error_values=[999]):
    """
    error_values is a list to be removed from column df[column_name]
    returns a dataframe with just one column
    """
    # Similar to cleaned = [x for x in df['age'] if x != 999]
    column = list(df[column_name][~df[column_name].isin([error_values])])
    # Creating a new dataframe
    cleaned = pd.DataFrame({column_name: column})
    return cleaned


def customdescribe(df, column_name, error_values=[999]):
    """
    Returns a custom description
    """
    cleaned = clean_column(df, column_name, error_values)
    cleaned.hist(bins=20)
    return None


def getdatetimes(df, column_name1, column_name2, error_values=[999]):
    """
    Converts two columns containing datetimes as strings to dataframes containing datetimes
    """
    column1 = clean_column(df, column_name1, error_values)
    column2 = clean_column(df, column_name2, error_values)

    dates1 = pd.to_datetime(column1[column_name1], format='%Y-%m-%d %H:%M:%S')
    dates2 = pd.to_datetime(column2[column_name2], format='%Y-%m-%d %H:%M:%S')

    print(column_name1)
    print(dates1)
    print("\n")
    print(column_name2)
    print(dates2)

    return (dates1, dates2)


def main ():
    FILENAME = 'xrays_visits.csv'
    DELIMITER = ","
    ERROR_VALUES = [999]

    d = convert(FILENAME, DELIMITER)
    customdescribe(d[0], 'age', ERROR_VALUES)
    getdatetimes(d[0], 'entry_date', 'exit_date', ERROR_VALUES)

if __name__ == '__main__':
    main()
