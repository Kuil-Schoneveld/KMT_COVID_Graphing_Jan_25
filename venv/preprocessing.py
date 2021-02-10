import pandas as pd

def read_n_clean(rivm_dataframe):

    # Converting csv file into a pandas dataframe
    #rivm_dataframe = pd.read_csv("COVID-19_aantallen_gemeente_cumulatief.csv", sep=";", quotechar='"')
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    # Removing whitespace, apostrophes, other characters from municipality names
    rivm_dataframe['Municipality_name'] = rivm_dataframe['Municipality_name'].str.replace(' ', '_')
    rivm_dataframe['Municipality_name'] = rivm_dataframe['Municipality_name'].str.replace('\'', ',')
    rivm_dataframe['Municipality_name'] = rivm_dataframe['Municipality_name'].str.replace('(', '')
    rivm_dataframe['Municipality_name'] = rivm_dataframe['Municipality_name'].str.replace(')', '')
    rivm_dataframe['Municipality_name'] = rivm_dataframe['Municipality_name'].str.replace('.', '')

