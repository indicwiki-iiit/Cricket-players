import pandas as pd
import pickle
import ast
import json

structures = {}
categories = {}

def get_prefix(prefix):
    if prefix == '':
        return ''
    non_num_idx = len(prefix)
    for j in range(len(prefix)):
        p = prefix[j]
        if not (p >= '0' and p <= '9'):
            non_num_idx = j
            break
    return prefix[:non_num_idx] + ' వ స్థానం'

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

def handle_gender(ele, gender):
    g = 0
    if gender == "Female":
        g = 1
    replace_english = ['handle_gender_5', 'handle_gender_4', 'handle_gender_3', 'handle_gender_2', 'handle_gender_1', 'handle_gender']
    telugu_words = ['నిలిచాడు/నిలిచింది', 'వహించాడు/వహించింది', 'ప్రారంభించాడు/ప్రారంభించింది', 'సాధించాడు/సాధించింది', 'అయ్యాడు/అయింది', 'చేసాడు/చేసింది']
    for j in range(6):
        ele = ele.replace(replace_english[j], telugu_words[j].split('/')[g])
    return ele

def create_dicts():
    global structures
    global categories
    df1 = pd.read_excel("Hrudai_records_translation.xlsx")
    df2 = pd.read_excel("Sowmya_records_translation.xlsx")
    df3 = pd.read_excel("Komal_records_translation.xlsx")
    for i, row in df1.iterrows():
        structures[row['English']] = row['Telugu']
        categories[row['English']] = row['Category']
    for i, row in df2.iterrows():
        structures[row['English']] = row['Telugu']
        categories[row['English']] = row['Category']
    for i, row in df3.iterrows():
        structures[row['English']] = row['Telugu']
        categories[row['English']] = row['Category']
    structures[' 99 not out (and 199, 299 etc) '] = '99 నాట్ అవుట్ (199, 299 ఎట్సిట్రా) గా నిలిచినా ఆటగాళ్ల'
    categories[' 99 not out (and 199, 299 etc) '] = 'Both rank and statistic present'
    
def get_sentence(ele):
    current_val = ele.split(" ")
    if len(current_val) == 0:
        return ''
    start_index = ele.find(current_val[0]) + len(current_val[0])
    end_index = len(ele)
    open_c = ele[ele.find("("):].count('(')
    if open_c == 2:
        f_o = ele.find("(")
        end_index = ele[f_o+1:].find("(") + f_o + 1
    elif open_c == 1 and ele[ele.find("("):][1] >= '0' and ele[ele.find("("):][1] <= '9':
        end_index = ele.find("(")
    prefix = ele[:start_index]
    structure = ele[start_index:end_index]
    suffix = ele[end_index:]
    return prefix, structure, suffix

def get_transformed_record(ele, gender):
    global structures
    global categories
    prefix, structure, suffix = get_sentence(ele)
    prefix = get_prefix(prefix)
    prefix = prefix.strip()
    translated_structure = structures[structure].strip()
    suffix = get_suffix(suffix)
    suffix = suffix.strip()
    if categories[structure] == 'No rank, no statistic':
        return handle_gender(translated_structure + '.', row['Gender'])
    if categories[structure] == 'Only rank':
        return translated_structure + " జాబితా లో " + prefix + "."
    if categories[structure] == 'Only statistic':
        return handle_gender(translated_structure + " " + suffix + '.', row['Gender'])
    return translated_structure + " జాబితా లో " + prefix + " " + suffix + '.'
    
    
english_cols = ['Records', 'Test Records', 'ODI Records', 'T20I Records']
telugu_cols = ['records_telugu', 'test_records_telugu', 'odi_records_telugu', 't20i_records_telugu']
new_telugu_lists = [[], [], [], []]

a = pd.read_excel("cricket_players_records.xlsx")
a.drop(columns=["Player_Name_Telugu","References"], inplace=True)
a.fillna(value="nan", inplace=True)
create_dicts()

for j in range(4):
    attribute = english_cols[j]
    for i, row in a.iterrows():
        if i % 500 == 0:
            print(f'{i} players done')
        if not is_valid_string(a.at[i, attribute]):
            new_telugu_lists[j].append('[]')
            continue
        if pd.isnull(a.at[i, attribute]):
            new_telugu_lists[j].append('[]')
            continue
        if str(a.at[i, attribute]) == "":
            new_telugu_lists[j].append('[]')
            continue
        given_list = ast.literal_eval(a.at[i, attribute])
        given_list = [g for g in given_list if not "worst" in g.lower()]
        a.at[i, attribute] = str(given_list)
        unique_structures = []
        player_record_list = []
        for ele in given_list:
            record_prefix, record_structure, record_suffix = get_sentence(ele)
            record_structure = record_structure.strip()
            if record_structure in unique_structures:
                continue
            unique_structures.append(record_structure)
            transformed_record = get_transformed_record(ele, row["Gender"])
            if transformed_record != '':
                transformed_record = transformed_record.strip()
                player_record_list.append(transformed_record)
        player_record_list = list(set(player_record_list))
        new_telugu_lists[j].append(str(player_record_list))
    a[telugu_cols[j]] = new_telugu_lists[j]
    
a = a.drop_duplicates()
a = a.drop_duplicates('Cricinfo_id')
a.drop(a.columns[a.columns.str.contains(
    'unnamed', case=False)], axis=1, inplace=True)
print(a.shape)
print(a.columns.tolist())
a.to_excel("final_cricket_players_records.xlsx", index=False)



