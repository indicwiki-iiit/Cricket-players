import pandas as pd
import pickle
import ast
import json

def get_prefix(prefix):
    if prefix == '':
        return ''
    non_num_idx = len(prefix)
    for j in range(len(prefix)):
        p = prefix[j]
        if not (p >= '0' and p <= '9'):
            non_num_idx = j
            break
    return prefix[:non_num_idx] + ' వ స్థానం.'

def get_suffix(suffix):
    if suffix == '':
        return ''
    s = suffix[1:-1]
    if s.endswith('*') or s.endswith('+'):
        return suffix
    if s.endswith('th') or s.endswith('nd') or s.endswith('st') or s.endswith('rd'):
        s = s[:-2]
        return '(' + s + ' వ వికెట్)'
    if 'y' in s and 'd' in s:
        year_num = s.split(" ")[0][:-1]
        day_num = s.split(" ")[1][:-1]
        return '(' + year_num + ' సంవత్సరాల ' + day_num + ' రోజులు)'
    if '/' in s:
        if not s.endswith('d'):
            return suffix
        s = s[:-1]
        return '(' + s + ' డిక్లేర్డ్)'
    return suffix
    
def is_valid_string(attribute_value):
    if not isinstance(attribute_value, str):
        return True
    return not (attribute_value == None or pd.isnull(attribute_value) or str(attribute_value) == "" or str(attribute_value) == "nan")

a = pd.read_excel("cricket_players_records.xlsx")
a.drop(columns=["Player_Name_Telugu","Gender","References"], inplace=True)
a.fillna(value="nan", inplace=True)
cols = [c for c in a.columns.tolist() if not "telugu" in c.lower() and c != 'Cricinfo_id']
all_seconds = set()
all_lasts = set()
all_second_lasts = set()
all_first = set()
all_sentences = set()
bracks = set()
wah = set()
bla = set()
senti = set()
suffixes = set()
prefixes = set()
# bb = set()

sentences_list = []
df_cols = ['Category', 'English', 'Telugu']

sent_with_prefix_only = set()
sent_with_suffix_only = set()
sent_with_prefix_and_suffix = set()
sent_without_prefix_or_suffix = set()

edge_cases = [
    ' 1000 runs and 100 wickets ', ' 200 runs and 10 wicketkeeping dismissals in a series ', 
    ' 250 runs and 10 wickets in a series ', ' 99 not out (and 199, 299 etc) (299*)', 
    ' 99 not out (and 199, 299 etc) (199*)', ' 2000 runs and 100 wicketkeeping dismissals ', 
    ' 100 runs and 10 wickets in a match ', ' 300 runs and 15 wicketkeeping dismissals in a series ', 
    ' 250 runs and 20 wickets in a series ', ' 5000 runs and 50 fielding dismissals ', 
    ' 1000 runs, 50 wickets and 50 catches ', ' 99 not out (and 199, 299 etc) (99*)',
    '1st Fewest ducks in career '
]

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
                # bb.add(ele[f_o:end_index])
            elif open_c == 1 and ele[ele.find("("):][1] >= '0' and ele[ele.find("("):][1] <= '9':
                end_index = ele.find("(")
            # all_first.add(current_val[0])
            # all_lasts.add(current_val[-1])
            # all_seconds.add(current_val[1])
            # all_second_lasts.add(current_val[-2])
            if len(ele) != end_index:
                s = ele[end_index:]
                s = s[1:-1]
                if s.endswith('th') or s.endswith('nd') or s.endswith('st') or s.endswith('rd'):
                    # print(ele)
                    pass
                suffixes.add(s)
            # all_sentences.add(ele[start_index:end_index])
            prefix_length = start_index
            prefixes.add(ele[:start_index])
            suffix_length = len(ele) - end_index
            if prefix_length == 0 and suffix_length == 0:
                sent_without_prefix_or_suffix.add(ele[start_index:end_index])
            if prefix_length == 0 and suffix_length > 0:
                print(ele)                    
                sent_with_suffix_only.add(ele[start_index:end_index])
            if prefix_length > 0 and suffix_length == 0:
                sent_with_prefix_only.add(ele[start_index:end_index])
            if prefix_length > 0 and suffix_length > 0:
                sent_with_prefix_and_suffix.add(ele[start_index:end_index])
# print(prefixes)

# for b in bb:
#     print(b)
# for s in suffixes:
#     s = s[1:-1]
#     if s.endswith('*') or s.endswith('+'):
#         continue
#     if s.endswith('th') or s.endswith('nd') or s.endswith('st') or s.endswith('rd'):
#         continue
#     if 'y' in s and 'd' in s:
#         continue
#     if '/' in s:
#         continue
#         if s.endswith('d'):
#             pass
#     try:
#         val = float(s)
#     except:
#         pass
    
        # print(s)
# print(len(sent_without_prefix_or_suffix))
# print()
# print(sent_without_prefix_or_suffix)
# print()
# print()

# print(len(sent_with_prefix_only))
# print()
# print(sent_with_prefix_only)
# print()
# print()

# print(len(sent_with_suffix_only))
# print()
# print(sent_with_suffix_only)
# print()
# print()

# print(len(sent_with_prefix_and_suffix))
# print()
# print(sent_with_prefix_and_suffix)
# print()
# print()

# for s in sent_without_prefix_or_suffix:
#     sentences_list.append(['No rank, no statistic', s, ''])
# for s in sent_with_prefix_only:
#     sentences_list.append(['Only rank', s, ''])
# for s in sent_with_suffix_only:
#     sentences_list.append(['Only statistic', s, ''])
# for s in sent_with_prefix_and_suffix:
#     sentences_list.append(['Both rank and statistic present', s, ''])
# rows_1 = sentences_list[:80]
# rows_2 = sentences_list[80:160]
# rows_3 = sentences_list[160:]
# a = pd.DataFrame(rows_1, columns=df_cols)
# b = pd.DataFrame(rows_2, columns=df_cols)
# c = pd.DataFrame(rows_3, columns=df_cols)
# print(a.shape)
# print(b.shape)
# print(c.shape)
# a.to_excel("Hrudai_records_translation.xlsx")
# b.to_excel("Sowmya_records_translation.xlsx")
# c.to_excel("Komal_records_translation.xlsx")







# Prefix (rank) + structure + suffix (statistic)

# Example -  
# 33rd Best figures in a match on debut (8)
# structure: Best figures in a match on debut 
# prefix: 33rd
# suffix: (8)



# Idea - 
# Translated_structure + suffix + prefix
# అరంగేట్రం లో ఉత్తమ గణాంకాల జాబితా లో 33 వ స్థానం సాధించాడు.


