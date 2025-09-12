import pandas as pd
import os.path

def load_data(filename):
    if not os.path.exists(filename):
        print(f"{filename} does not exist")
        return None
    try:
        pd_data = pd.read_csv(filename)
        return pd_data
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

filename = "./Social_Network_Ads.csv"
data = load_data(filename=filename)
if data is not None:
    print(data.head())
    print(data.tail())


def count_by_group(data, column):
    if column == "": 
        return {col: data[col].value_counts() for col in data.columns}
    else:              
        return data[column].value_counts()

pd_data = data.copy()
pd_data.set_index("User ID", inplace=True)

pd_data = data.copy()
result = count_by_group(pd_data, "Gender")
print(result)
print()

result_all = count_by_group(pd_data, "")
print(result_all)
print()

dirty_data = pd.read_csv("dirty_str_house_prices.csv")
dirty_data.set_index("Id", inplace=True)
del dirty_data["Unnamed: 0"]

def clean_dataframe(df):
    df_clean = df.copy()
    for col in df_clean.columns:
        df_clean[col] = (df_clean[col]
                         .astype(str)
                         .str.upper()
                         .str.replace(r'[^A-Z0-9]', '', regex=True)
                         .str.strip())
    return df_clean

dirty_data = pd.read_csv("dirty_str_house_prices.csv")
dirty_data.set_index("Id", inplace=True)
del dirty_data["Unnamed: 0"]

pd_dirty_data = clean_dataframe(dirty_data)
print(pd_dirty_data.head())

def compare_dataframes(pd_data, pd_dirty_data):
    comparison = {}
    for col in pd_data.columns:
        same = (pd_data[col].astype(str) == pd_dirty_data[col].astype(str)).mean() * 100
        comparison[col] = same
    return pd.Series(comparison, name="(%) same")

pd_data = pd.read_csv("str_house_prices.csv")
pd_data.set_index("Id", inplace=True)

comparison = compare_dataframes(pd_data, pd_dirty_data)
print(comparison)
print("Good Job!")
