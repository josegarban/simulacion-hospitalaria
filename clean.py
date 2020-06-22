import pandas as pd
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

    df['age'].hist(bins=1000)
    # print(type(hist))


def main ():
    FILENAME = 'xrays_visits.csv'
    DELIMITER = ","
    d = convert(FILENAME, DELIMITER)
    customdescribe(d[0])

if __name__ == '__main__':
    main()
