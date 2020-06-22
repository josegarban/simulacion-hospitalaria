import pandas as pd
import matplotlib as mpl
import pprint

def convert(filename, delimiter=","):
    """
    Returns a tuple with the dataframe and the column names
    """
    df = pd.read_csv(filename, delimiter,header=0)
    header_list = list(df.columns)
    print("Obtained the following dataframe:")
    print("\n", df.dtypes, "\n")
    print(df)
    return (df, header_list)

def customdescribe(df, column_name=""):
    """
    Returns a custom description
    """
    print("Dataframe description:")
    print(df.describe())

    # Similar to cleaned = [x for x in df['age'] if x != 999]
    column = list(df[column_name][~df[column_name].isin([999])])

    # Creating a new dataframe
    cleaned = pd.DataFrame({column_name: column})
    cleaned.hist(bins=20)
    # print(type(hist))


def main ():
    FILENAME = 'xrays_visits.csv'
    DELIMITER = ","
    d = convert(FILENAME, DELIMITER)
    customdescribe(d[0], 'age')

if __name__ == '__main__':
    main()
