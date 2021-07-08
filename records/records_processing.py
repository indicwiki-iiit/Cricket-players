# Script for identifying the count and type of unique sentence structures in records attribute of dataset

import pandas as pd
import pickle
import ast
import json
 
# Checks if given argument is indeed a valid string in the dataset   
def is_valid_string(attribute_value):
    if not isinstance(attribute_value, str):
        return True
    return not (attribute_value == None or pd.isnull(attribute_value) or str(attribute_value) == "" or str(attribute_value) == "nan")

a = pd.read_excel("cricket_players_records.xlsx")
a.drop(columns=["Player_Name_Telugu","Gender","References"], inplace=True)
a.fillna(value="nan", inplace=True)
cols = [c for c in a.columns.tolist() if not "telugu" in c.lower() and c != 'Cricinfo_id']
suffixes = set()
prefixes = set()
sent_with_prefix_only = set()
sent_with_suffix_only = set()
sent_with_prefix_and_suffix = set()
sent_without_prefix_or_suffix = set()

# list of corner cases in sentence structures
edge_cases = [
    ' 1000 runs and 100 wickets ', ' 200 runs and 10 wicketkeeping dismissals in a series ', 
    ' 250 runs and 10 wickets in a series ', ' 99 not out (and 199, 299 etc) (299*)', 
    ' 99 not out (and 199, 299 etc) (199*)', ' 2000 runs and 100 wicketkeeping dismissals ', 
    ' 100 runs and 10 wickets in a match ', ' 300 runs and 15 wicketkeeping dismissals in a series ', 
    ' 250 runs and 20 wickets in a series ', ' 5000 runs and 50 fielding dismissals ', 
    ' 1000 runs, 50 wickets and 50 catches ', ' 99 not out (and 199, 299 etc) (99*)',
    '1st Fewest ducks in career '
]

# Extracting the rank, stat value and sentence structure for a given record sentence
for attribute in cols:
    for i, row in a.iterrows():
        if not is_valid_string(a.at[i, attribute]):
            continue
        if pd.isnull(a.at[i, attribute]):
            continue
        if str(a.at[i, attribute]) == "":
            continue
        given_list = ast.literal_eval(a.at[i, attribute])
        for ele in given_list:
            if ele in edge_cases:
                sent_without_prefix_or_suffix.add(ele)
                continue
            current_val = ele.split(" ")
            if len(current_val) == 0:
                continue
            start_index = ele.find(current_val[0]) + len(current_val[0])
            end_index = len(ele)
            open_c = ele[ele.find("("):].count('(')
            if open_c == 2:
                f_o = ele.find("(")
                end_index = ele[f_o+1:].find("(") + f_o + 1
            elif open_c == 1 and ele[ele.find("("):][1] >= '0' and ele[ele.find("("):][1] <= '9':
                end_index = ele.find("(")
            if len(ele) != end_index:
                s = ele[end_index:]
                s = s[1:-1]
                suffixes.add(s)
            prefix_length = start_index
            prefixes.add(ele[:start_index])
            suffix_length = len(ele) - end_index
            # Segregating sentences based on the presence/absence of prefix, suffix
            if prefix_length == 0 and suffix_length == 0:
                sent_without_prefix_or_suffix.add(ele[start_index:end_index])
            if prefix_length == 0 and suffix_length > 0:
                print(ele)                    
                sent_with_suffix_only.add(ele[start_index:end_index])
            if prefix_length > 0 and suffix_length == 0:
                sent_with_prefix_only.add(ele[start_index:end_index])
            if prefix_length > 0 and suffix_length > 0:
                sent_with_prefix_and_suffix.add(ele[start_index:end_index])

