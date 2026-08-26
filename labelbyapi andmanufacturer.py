import pandas as pd
import numpy as np

dict = {}

df = pd.read_excel("filename.xlsx")

product_code = 0
nan_key_rows = 0

def normalize_key(value):
    """Strip/case-normalize labelling keys; NaN is returned as-is (counted and warned about below)."""
    if pd.isna(value):
        return value
    return str(value).strip().upper()

for index, row in df.iterrows():
    if pd.isna(row['Active Ingredient']) or pd.isna(row['Exporter']):
        nan_key_rows += 1
        
    active_ingredient = normalize_key(row['Active Ingredient'])
    if(active_ingredient in dict):
        numbered_ingredient = dict[active_ingredient]
        exporter = normalize_key(row['Exporter'])
        code = 0
        if(exporter in numbered_ingredient):
            code = numbered_ingredient[exporter]
        else:
            code = product_code
            numbered_ingredient[exporter] = code
            dict[active_ingredient] = numbered_ingredient
            product_code += 1
        
        df.at[index,'Product Code'] = code
    else:
        numbered_ingredient = {}
        exporter = normalize_key(row['Exporter'])
        numbered_ingredient[exporter] = product_code
        df.at[index,'Product Code'] = product_code
        product_code += 1
        dict[active_ingredient] = numbered_ingredient

if nan_key_rows:
    print(f"Warning: {nan_key_rows} row(s) have a missing 'Active Ingredient' or 'Exporter' and were labelled without normalization.", flush=True)

df['Product Code'] = df['Product Code'].astype(int)
    
df.to_excel('./albaniaimport_result.xlsx', index=False)
