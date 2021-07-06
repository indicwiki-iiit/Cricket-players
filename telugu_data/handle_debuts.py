import pandas as pd
import sweetviz as sv
import pickle
import random
import ast
import json
from jinja2 import Environment, FileSystemLoader
import translators as ts
import pandas as pd
from deeptranslit import DeepTranslit
from functools import cmp_to_key
from deep_translator import GoogleTranslator
from google_trans_new import google_translator
from google.transliteration import transliterate_word, transliterate_text

translator = google_translator()
trans = DeepTranslit('telugu').transliterate

month_names = {
    'February': 'ఫిబ్రవరి', 'December': 'డిసెంబర్', 'May': 'మే', 'October': 'అక్టోబర్', 
    'January': 'జనవరి', 'November': 'నవంబర్', 'April': 'ఏప్రిల్', 'March': 'మార్చి', 
    'September': 'సెప్టెంబర్', 'June': 'జూన్', 'August': 'ఆగస్టు', 'July': 'జూలై'
}

def is_valid_string(attribute_value):
    if not isinstance(attribute_value, str):
        return True
    return not (attribute_value == None or pd.isnull(attribute_value) or str(attribute_value) == "" or str(attribute_value) == "nan")

def getTransliteratedDescription(description):
    if not is_valid_string(description):
        return ''
    try:
        current_attribute_value = description
        # anu_title = telugu.anuvaad(row.title.values[0])
        deep = trans(current_attribute_value)[0]
        description = deep['pred']
    except:
        try:
            return transliterate_text(description, lang_code='te')
        except:
            pass
    return description

def change_abbr(h):
    alpha = {
        "A":"ఏ",      
        "B":"బీ",
        "C":"సీ",  
        "D":"డీ",
        "E":"ఈ",
        "F":"ఎఫ్",
        "G":"జీ",
        "H":"హెచ్",
        "I":"ఐ",
        "J":"జే",       
        "K":"కే",
        "L":"ఎల్",
        "M":"ఎం",
        "N":"ఎన్",
        "O":"ఓ",
        "P":"పీ",
        "Q":"క్యూ",
        "R":"ఆర్",   
        "S":"ఎస్",
        "T":"టీ",
        "U":"యూ",
        "V":"వీ",
        "W":"డబల్యూ",
        "X":"ఎక్స్",
        "Y":"వై",
        "Z":"జెడ్"
    }
    return ''.join([alpha[i] + '.' for i in h])[:-1]

def get_token_translation(token):
    non_alphas = {
        "QuettaR": 'క్వెట్టా',
        "NAM": 'నమీబియా',
        "AFG": 'ఆఫ్ఘనిస్తాన్',
        "GER": 'జర్మనీ',
        "BDESH": 'బంగ్లాదేశ్',
        'World-XI': 'వరల్డ్-XI',
        'C&C': 'సీ&సీ',
        'T&T': 'టీ&టీ',
        'XI': 'XI',
        'UCB-BCB': change_abbr('UCB') + '-' + change_abbr('BCB'),
        'SL': 'శ్రీలంక',
        'PAK': 'పాకిస్తాన్',
        'USA': 'యునైటెడ్ స్టేట్స్ ఆఫ్ అమెరికా',
        'UAE': 'యునైటెడ్ అరబ్ ఎమిరేట్స్',
        'ENG': 'ఇంగ్లాండ్',
        'PNG': 'పాపువా న్యూ గిని',
        'LIONS': 'లయన్స్',
        'NZ': 'న్యూజీలాండ్',
        'PNJB': 'పంజాబ్',
        'OMAN': 'ఒమన్',
        'HKG': 'హాంగ్ కొంగ',
        'WI': 'వెస్ట్ ఇండీస్',
        'AUS': 'ఆస్ట్రేలియా',
        'SA': 'దక్షిణ ఆఫ్రికా',
        'BIHAR': 'బిహార్',
        'IND': 'ఇండియా'
    }
    if token in non_alphas.keys():
        return non_alphas[token]
    return change_abbr(token)

# all_vals = set()
# team_names = set()
# att = set()
# vss = set()

# def add_to_team_names(debb):
#     global team_names
#     global att
#     global vss
#     deb = debb.split(" ")
#     team_1 = ""
#     team_2 = ""
#     vs_c = 0
#     at_c = 0
#     for j in range(len(deb)):
#         if deb[j] == "vs":
#             vs_c = j
#             break
#     for j in range(len(deb)):
#         if deb[j] == "at":
#             at_c = j
#             break
#     team_1 = ' '.join(deb[:vs_c])
#     team_2 = ' '.join(deb[vs_c + 1:at_c])
#     team_names.add(team_1)
#     team_names.add(team_2)
#     if "at" in team_1:
#         att.add(team_1)
#     if "at" in team_2:
#         att.add(team_2)
#     if "vs" in team_1:
#         vss.add(team_1)
#     if "vs" in team_2:
#         vss.add(team_2)    
    

def get_debut_string(deb):
    global month_names
    if not is_valid_string(deb) or deb == None or pd.isnull(deb):
        return ''
    deb = deb.replace(" vs ", " versus ")
    months_in_deb = [month for month in month_names.keys() if month in deb]
    for month in months_in_deb:
        deb = deb.replace(month, month_names[month])
    tokens = deb.split(" ")
    for j in range(len(tokens)):
        tok = tokens[j]
        if len(tok) > 0 and tok[-1] >= 'A' and tok[-1] <= 'Z':
            tokens[j] = get_token_translation(tok)
    deb = ' '.join(tokens)
    occ = deb.find(" at ")
    if occ == -1:
        return getTransliteratedDescription(deb)
    deb = deb[:occ] + ', ' + deb[occ:]
    occ = deb.find(" at ")
    occ2 = deb[occ:].find(" - ") + occ
    if occ2 == -1:
        occ2 = len(deb)
    curr_sub = deb[occ:occ2]
    tokens = curr_sub.split(' ')
    tokens.append('లో ')
    deb = deb.replace(curr_sub, ' '.join(tokens[2:]))
    return getTransliteratedDescription(deb)
          
a = pd.read_csv("professional_life_trans.csv", low_memory=False)
a.fillna(value="nan", inplace=True)
cols = [c for c in a.columns.tolist() if "debut" in c.lower() and not "telugu" in c.lower()]
# print(cols)

for attribute in cols:
    print()
    print(attribute)
    print()
    new_list = []
    for i, row in a.iterrows():
        if i % 100 == 0:
            print(f'{i} players done')
        new_list.append(get_debut_string(a.at[i, attribute]))
    a[attribute + '_Telugu'] = new_list
a = a.drop_duplicates()
a = a.drop_duplicates('Cricinfo_id')
a.drop(a.columns[a.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
a.to_csv('professional_life_trans.csv', index=False)



