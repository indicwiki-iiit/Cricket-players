# Performs a secondary level data cleaning based on defects observed on dataset obtained after initial cleaning

import pandas as pd
import sweetviz as sv
b = pd.read_csv("final_cricket_players.csv", low_memory=False)

# Replacing empty lists, dictionarities etc to null strings for easier processing
b = b.replace(to_replace="-",value="")
b = b.replace(to_replace="[]",value="")
b = b.replace(to_replace="{}",value="")

b.drop(b.columns[b.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
b.to_csv('Cleaned_dataset.csv', index=False)
report = sv.analyze(b, pairwise_analysis='off')
report.show_html()