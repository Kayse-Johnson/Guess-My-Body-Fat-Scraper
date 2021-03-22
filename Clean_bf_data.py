#%%
import pandas as pd
import missingno as msno
from pprint import pprint
def cleaning():
    ''' Recieve the dirty data file and proceed to clean it and visualise it to better understand the data
    before creating a new csv file without missing values and duplicates.
    '''

    # Set option to display more rows for better viewing
    pd.set_option('display.max_rows',100)
    #Read in the dirty csv data file
    df=pd.read_csv('Body_Fat_Reddit_Data.csv')
    #Print the number of duplicates, their rows and remove them
    print(df.duplicated().sum())
    duplicates = df.duplicated(keep=False)
    print(df[duplicates])
    df.drop_duplicates(inplace=True, ignore_index=True)
    pprint(df)
    print()
    #Describe the data set to ensure numbers are reasonable
    pprint(df.describe())
    print()
    #Remove rows that have unrealistic data
    df = df.loc[df['Height(ft)']<9]
    pprint(df)
    print()
    pprint(df.describe())
    print()
    #Determine the number of missing values as a percentage and visualise it
    null_index=df.isnull()
    pprint(null_index.mean()*100)
    print()
    #print(msno.matrix(df))
    #print()
    #Remove rows with missing values
    clean=df.dropna()
    pprint(clean)
    print()
    #Create a new csv file with the cleaned data
    clean.to_csv('Clean_Body_Fat_Reddit_Data.csv', index=False)
    return

