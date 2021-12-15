import pandas as pd

dict = {}

df = pd.DataFrame()
data = pd.read_excel("filename.xlsx")
df = df.append(data)

product_code = 0

for index, row in df.iterrows():
    active_ingredient = row['Active Ingredient']
    if(active_ingredient in dict):
        df.at[index,'Product Code'] = dict[active_ingredient]
        
    else:
        dict[active_ingredient] = product_code
        df.at[index,'Product Code'] = product_code
        product_code += 1
        
df.to_excel('./result.xlsx')
