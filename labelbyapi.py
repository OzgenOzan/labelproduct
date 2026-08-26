import pandas as pd

dict = {}

df = pd.read_excel("filename.xlsx")

product_code = 0
nan_key_rows = 0

for index, row in df.iterrows():
    value = row['Active Ingredient']
    if pd.isna(value):
        nan_key_rows += 1
        active_ingredient = value  # keep previous behavior for missing keys
    else:
        active_ingredient = str(value).strip().upper()
    if(active_ingredient in dict):
        df.at[index,'Product Code'] = dict[active_ingredient]
        
    else:
        dict[active_ingredient] = product_code
        df.at[index,'Product Code'] = product_code
        product_code += 1

if nan_key_rows:
    print(f"Warning: {nan_key_rows} row(s) have a missing 'Active Ingredient' and were labelled without normalization.", flush=True)

df['Product Code'] = df['Product Code'].astype(int)
        
df.to_excel('./result.xlsx', index=False)
