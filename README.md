# labelproduct

Labelling each entry for tables including various products and specifications regarding them

The raw data which used for this study included information of; date of importation, active pharmaceutical ingredient (API), brand name, product quantity for the related importation, manufacturer’s name, and name of the market authorization holder. For the purpose of the study, import dates, APIs, and quantities are extracted to an excel table. And then each entry labelled regarding the name of the API using an algorithm, which is shown below, in Python, version 3.9.7.

```

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

```

Also for labelling each pharmaceutical product according to its API and manufacturer:

```

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

``` 

