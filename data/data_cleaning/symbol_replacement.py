import pandas as pd
import sweetviz as sv
b = pd.read_csv("final_cricket_players.csv", low_memory=False)
b = b.replace(to_replace="-",value="")
b = b.replace(to_replace="[]",value="")
b = b.replace(to_replace="{}",value="")

b.drop(b.columns[b.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
b.to_csv('Cleaned_dataset.csv', index=False)
report = sv.analyze(b, pairwise_analysis='off')
report.show_html()