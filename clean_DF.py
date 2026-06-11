import pandas as pd
import re


def Clean_DF(df, drop_duplicates=True, handle_nulls='drop', null_threshold=0.5):
    """
    Clean a dataframe by handling null values, removing duplicates, 
    and standardizing column names to snake_case.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe to clean
    drop_duplicates : bool, default=True
        Whether to remove duplicate rows. If True, keeps the first occurrence.
    handle_nulls : str, default='drop'
        How to handle null values:
        - 'drop': Remove rows with any null values
        - 'drop_cols': Remove columns with more nulls than threshold
        - 'forward_fill': Forward fill null values
        - 'mean': Fill numeric columns with mean (numeric only)
    null_threshold : float, default=0.5
        When handle_nulls='drop_cols', remove columns where null % > threshold.
        Range: 0 to 1 (e.g., 0.5 means remove if >50% nulls)
    
    Returns:
    --------
    pd.DataFrame
        Cleaned dataframe with standardized column names
    
    Example:
    --------
    >>> df = pd.read_csv('messy.csv')
    >>> clean_df = Clean_DF(df, drop_duplicates=True, handle_nulls='drop')
    """
    
    # Create a copy to avoid modifying the original dataframe
    df = df.copy()
    
    # Step 1: Standardize column names to snake_case
    df.columns = [_to_snake_case(col) for col in df.columns]
    
    # Step 2: Handle null values
    if handle_nulls == 'drop':
        df = df.dropna()
    elif handle_nulls == 'drop_cols':
        null_percentage = df.isnull().sum() / len(df)
        cols_to_drop = null_percentage[null_percentage > null_threshold].index
        df = df.drop(columns=cols_to_drop)
    elif handle_nulls == 'forward_fill':
        df = df.fillna(method='ffill').fillna(method='bfill')
    elif handle_nulls == 'mean':
        numeric_cols = df.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            df[col] = df[col].fillna(df[col].mean())
    
    # Step 3: Remove duplicate rows (keeping first occurrence)
    if drop_duplicates:
        df = df.drop_duplicates(keep='first')
    
    # Reset index after cleaning
    df = df.reset_index(drop=True)
    
    return df


def _to_snake_case(text):
    """
    Convert column name to snake_case format.
    
    Parameters:
    -----------
    text : str
        Column name to convert
    
    Returns:
    --------
    str
        Column name in snake_case
    
    Example:
    --------
    >>> _to_snake_case('Employee_ID')
    'employee_id'
    >>> _to_snake_case('FirstName')
    'first_name'
    """
    # Replace spaces, dashes with underscores
    text = re.sub(r'[\s\-]+', '_', text)
    # Insert underscore before uppercase letters preceded by lowercase
    text = re.sub(r'([a-z])([A-Z])', r'\1_\2', text)
    # Convert to lowercase
    text = text.lower()
    # Remove extra underscores
    text = re.sub(r'_+', '_', text)
    # Strip leading/trailing underscores
    text = text.strip('_')
    return text