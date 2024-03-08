# french_industry library
import pandas as pd
import numpy as np

def summary(df):
    """
    Provides a summary of the DataFrame with information about the number of unique values, 
    percentage of missing values, data type of each column, mean or mode depending on the data type,
    and potential alerts such as too many missing values or imbalanced categories.
    
    Parameters:
    df (DataFrame): The DataFrame for which the summary is required.
    
    Returns:
    None
    """
    
    table = pd.DataFrame(
        index=df.columns,
        columns=['type_info', '%_missing_values', 'nb_unique_values', 'nb_zero_values','%_zero_values', 'list_unique_values', "mean_or_mode", "flag"])
    
    # Fill in column 'type_info' with data types of each column
    table.loc[:, 'type_info'] = df.dtypes.values
    
    # Calculate the percentage of missing values for each column
    table.loc[:, '%_missing_values'] = np.round((df.isna().sum().values / len(df)) * 100)
    
    # Calculate the number of unique values for each column
    table.loc[:, 'nb_unique_values'] = df.nunique().values

    # Calculate the number of 0 values for each column
    table.loc[:, 'nb_zero_values'] = df.isin([0]).sum().values

    # Calculate the percentage of 0 values for each column
    table.loc[:, '%_zero_values'] = np.round((df.isin([0]).sum().values/len(df)) * 100)
    
    # Function to get the list of unique values for a column, showing "Too many categories..." if there are too many
    def get_list_unique_values(colonne):
        if colonne.nunique() < 11:
            return colonne.unique()
        else:
            return "Too many categories..." if colonne.dtypes == "Object" else "Too many values..."
    
    # Function to get the mean or mode depending on the data type
    def get_mean_mode(colonne):
        if (colonne.dtypes == "O") or (len(colonne.unique()) < 20):
            return colonne.astype('category').mode()[0]
        else: 
            return colonne.mean()
    
    # Function to check for potential alerts such as too many missing values or imbalanced categories
    def alerts(colonne, thresh_na=0.25, thresh_balance=0.8):
        if (colonne.isna().sum()/len(df)) > thresh_na:
            return "Too many missing values!"
        elif colonne.value_counts(normalize=True).values[0] > thresh_balance:
            return "It's imbalanced!"
        else:
            return "Nothing to report"
        
    # Fill in the columns with the respective information
    table.loc[:, 'list_unique_values'] = df.apply(get_list_unique_values)
    table.loc[:, 'mean_or_mode'] = df.apply(get_mean_mode)
    table.loc[:, 'flag'] = df.apply(alerts)
    
    # Display the summary table
    return display(table)

# Data type verification  
def detection_error(element):
    try:
        float(element)
    except ValueError:
        return element


# Function that provides a short summary of DataFrame with information about the number of unique values, 
# percentage of missing values, number of missing values, and the data type of each column.

def summary_short(df):
    """
    Function that provides a short summary of DataFrame with information about the number of unique values, 
    percentage of missing values, number of missing values, and the data type of each column.
    
    Is used with not cleaned DataFrames.
    
    Parameters:
    df (DataFrame): The DataFrame for which the summary is required.
    
    Returns:
    DataFrame with 
    """
    
    tab = pd.DataFrame(index = df.columns, columns = ['nb_unique_values','%_missing_values','nb_missing_values','type'])
    tab.loc[:,'nb_unique_values'] = df.nunique().values
    tab.loc[:,'%_missing_values'] = np.round((df.isna().sum().values / len(df)) * 100)
    tab.loc[:,'nb_missing_values'] = df.isna().sum().values
    tab.loc[:, 'type'] = df.dtypes.values
    
    return display(tab)


def convert_columns_to_lower(df):
    
    """
    Convert column names in the DataFrame to lowercase.
    
    Parameters:
        df (DataFrame): Input DataFrame.
        
    Returns:
        DataFrame: DataFrame with column names converted to lowercase.
    """
    
    df.columns = [col.lower() for col in df.columns]
    return df