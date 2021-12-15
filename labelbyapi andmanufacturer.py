import pandas as pd
import numpy as np

dict = {}

df = pd.DataFrame()
data = pd.read_excel("filename.xlsx")
df = df.append(data)

product_code = 0

for index, row in df.iterrows():
        
    active_ingredient = row['Active Ingredient']
    if(active_ingredient in dict):
        numbered_ingredient = dict[active_ingredient]
        exporter = row['Exporter']
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
        exporter = row['Exporter']
        numbered_ingredient[exporter] = product_code
        df.at[index,'Product Code'] = product_code
        product_code += 1
        dict[active_ingredient] = numbered_ingredient
    
df.to_excel('./albaniaimport_result.xlsx')
