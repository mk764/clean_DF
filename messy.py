import pandas as pd
from clean_DF import Clean_DF

# Load the messy CSV file
df = pd.read_csv('rawdata/messy.csv')

print("="*60)
print("ORIGINAL DATAFRAME")
print("="*60)
print(f"Shape: {df.shape}")
print(f"\nColumn names:\n{df.columns.tolist()}")
print(f"\nNull values per column:\n{df.isnull().sum()}")
print(f"\nFirst few rows:\n{df.head()}")
print(f"\nDuplicate rows: {df.duplicated().sum()}")

# Clean the dataframe using Clean_DF function
cleaned_df = Clean_DF(df, drop_duplicates=True, handle_nulls='drop')

print("\n" + "="*60)
print("CLEANED DATAFRAME")
print("="*60)
print(f"Shape: {cleaned_df.shape}")
print(f"\nColumn names:\n{cleaned_df.columns.tolist()}")
print(f"\nNull values per column:\n{cleaned_df.isnull().sum()}")
print(f"\nFirst few rows:\n{cleaned_df.head()}")
print(f"\nDuplicate rows: {cleaned_df.duplicated().sum()}")

# Optional: Save the cleaned dataframe
cleaned_df.to_csv('rawdata/messy_cleaned.csv', index=False)
print("\n✓ Cleaned dataframe saved to: rawdata/messy_cleaned.csv")
