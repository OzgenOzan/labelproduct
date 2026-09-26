import pandas as pd

MISSING_KEY = "<MISSING>"  # Sentinel for missing labelling keys (LP-1)

code_map = {}  # Renamed from 'dict' (LP-3: do not shadow the builtin)

df = pd.read_excel("filename.xlsx")

product_code = 0
nan_key_rows = 0

for index, row in df.iterrows():
    value = row['Active Ingredient']
    if pd.isna(value):
        nan_key_rows += 1
        # Map missing keys to an explicit sentinel so every missing row shares
        # ONE deterministic code (LP-1). Previously the raw NaN was used as a
        # dict key; NaN != NaN, so NaN rows could receive different codes.
        active_ingredient = MISSING_KEY
    else:
        active_ingredient = str(value).strip().upper()
    if(active_ingredient in code_map):
        df.at[index,'Product Code'] = code_map[active_ingredient]
        
    else:
        code_map[active_ingredient] = product_code
        df.at[index,'Product Code'] = product_code
        product_code += 1

if nan_key_rows:
    print(f"Warning: {nan_key_rows} row(s) have a missing 'Active Ingredient' and were labelled with the {MISSING_KEY} sentinel.", flush=True)

df['Product Code'] = df['Product Code'].astype(int)
        
df.to_excel('./result.xlsx', index=False)
