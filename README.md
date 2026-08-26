# labelproduct

Labelling each entry for tables including various products and specifications regarding them

The raw data which used for this study included information of; date of importation, active pharmaceutical ingredient (API), brand name, product quantity for the related importation, manufacturer's name, and name of the market authorization holder. For the purpose of the study, import dates, APIs, and quantities are extracted to an excel table. And then each entry labelled regarding the name of the API using an algorithm, which is shown below, in Python, version 3.9.7.

```

import pandas as pd

dict = {}

df = pd.read_excel("filename.xlsx")

product_code = 0

for index, row in df.iterrows():
    active_ingredient = str(row['Active Ingredient']).strip().upper()
    if(active_ingredient in dict):
        df.at[index,'Product Code'] = dict[active_ingredient]
        
    else:
        dict[active_ingredient] = product_code
        df.at[index,'Product Code'] = product_code
        product_code += 1
        
df.to_excel('./result.xlsx', index=False)

```

Also for labelling each pharmaceutical product according to its API and manufacturer:

```

import pandas as pd
import numpy as np

dict = {}

df = pd.read_excel("filename.xlsx")

product_code = 0

for index, row in df.iterrows():
        
    active_ingredient = str(row['Active Ingredient']).strip().upper()
    if(active_ingredient in dict):
        numbered_ingredient = dict[active_ingredient]
        exporter = str(row['Exporter']).strip().upper()
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
        exporter = str(row['Exporter']).strip().upper()
        numbered_ingredient[exporter] = product_code
        df.at[index,'Product Code'] = product_code
        product_code += 1
        dict[active_ingredient] = numbered_ingredient
    
df.to_excel('./albaniaimport_result.xlsx', index=False)

```

## Installation

```
pip install -r requirements.txt
```

## Usage

1. Place your input table as `filename.xlsx` next to the script (required
   columns: `Active Ingredient`; also `Exporter` for the API+manufacturer
   variant).
2. Run `python labelbyapi.py` (labels by API) or
   `python "labelbyapi andmanufacturer.py"` (labels by API + exporter).
3. Output is written to `./result.xlsx` (or `./albaniaimport_result.xlsx`)
   with an integer `Product Code` column. Keys are stripped and
   upper-cased before labelling; rows with a missing key are reported with a
   warning.
