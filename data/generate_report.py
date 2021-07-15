# Generates sweetviz report for dataset - for detailed analysis
import pandas as pd
import sweetviz as sv

a = pd.read_excel("final_cricket_players_translated_dataset_with_images.xlsx")
a = a.applymap(str)
report = sv.analyze(a, pairwise_analysis='off')
report.show_html()

