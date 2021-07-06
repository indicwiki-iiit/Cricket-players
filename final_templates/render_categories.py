import pickle
import random
import ast
from jinja2 import Environment, FileSystemLoader
import pandas as pd
from functools import cmp_to_key

all_attributes = []
famous_countries = {
    'India': 'భారతీయ', 
    'Australia': 'ఆస్ట్రేలియా', 
    'England': 'ఇంగ్లాండు', 
    'West Indies': 'వెస్ట్‌ఇండీస్', 
    'Pakistan': 'పాకిస్తాన్', 
    'South Africa': 'దక్షిణాఫ్రికా', 
    'Sri Lanka': 'శ్రీలంక' 
}

translated_names = {
    "Span": "వ్యవధి",
    "Test": "టెస్ట్",
    "ODI": "వన్డే ఇంటర్నేషనల్‌",
    "T20": "టీ20",
    "T20I": "అంతర్జాతీయ టీ20",
    "FC": "ఫస్ట్ క్లాస్",
    "List A": "లిస్ట్ ఏ"
}    

def is_valid_string(attribute_value):
    return not (attribute_value == None or pd.isnull(attribute_value) or str(attribute_value) == "" or str(attribute_value) == "nan")
            
def get_nationality(nation):
    nation = nation.strip()
    nations = {
        'Pakistan': 'పాకిస్తాన్', 
        'Japan': 'జపాన్', 
        'Canada': 'కెనడా', 
        'India': 'భారతదేశం', 
        'Belgium': 'బెల్జియం', 
        'P.N.G.': 'పాపువా న్యూ గిని', 
        'Oman': 'ఒమన్', 
        'Austria': 'ఆస్ట్రియా', 
        'West Indies': 'వెస్ట్ ఇండీస్', 
        'Kuwait': 'కువైట్', 
        'E&C Africa': 'ఇ & సి ఆఫ్రికా', 
        'Bermuda': 'బెర్ముడా', 
        'Fiji': 'ఫిజి', 
        'Chile': 'చిలీ', 
        'Denmark': 'డెన్మార్క్', 
        'Malaysia': 'మలేషియా', 
        'Bangladesh': 'బంగ్లాదేశ్', 
        'Germany': 'జర్మనీ', 
        'U.A.E.': 'యునైటెడ్ అరబ్ ఎమిరేట్స్', 
        'Hong Kong': 'హాంగ్ కొంగ', 
        'Malta': 'మాల్టా',
        'Zimbabwe': 'జింబాబ్వే', 
        'Scotland': 'స్కాట్లాండ్', 
        'Singapore': 'సింగపూర్', 
        'Sri Lanka': 'శ్రీలంక', 
        'England': 'ఇంగ్లాండ్', 
        'Gibraltar': 'గిబ్రాల్టర్', 
        'Argentina': 'అర్జెంటీనా', 
        'Uganda': 'ఉగాండా', 
        'Italy': 'ఇటలీ', 
        'Kenya': 'కెన్యా', 
        'Nepal': 'నేపాల్', 
        'Netherlands': 'నెదర్లాండ్స్', 
        'South Africa': 'దక్షిణ ఆఫ్రికా', 
        'Ireland': 'ఐర్లాండ్', 
        'U.S.A.': 'యునైటెడ్ స్టేట్స్ ఆఫ్ అమెరికా', 
        'Afghanistan': 'ఆఫ్ఘనిస్తాన్', 
        'Cayman Is': 'కేమెన్ ఐలాండ్స్', 
        'New Zealand': 'న్యూజీలాండ్', 
        'Namibia': 'నమీబియా', 
        'Australia': 'ఆస్ట్రేలియా'
    }
    if not nation in nations.keys():
        return ''
    return nations[nation]
            
def get_year(given_date):
    if not is_valid_string(given_date):
        return -1
    given_date = ast.literal_eval(given_date)
    if len(given_date) != 2:
        return -1
    try:
        return int(given_date[-1][:5])
    except:
        return -1
    
def get_country_player(nationality, gender):
    global famous_countries
    country_string = get_nationality(nationality)
    if nationality in famous_countries.keys():
        country_string = famous_countries[nationality]
    if gender.startswith("F"):
        return "[[వర్గం:" + country_string + " మహిళా క్రికెట్ క్రీడాకారులు" + "]]\n"
    return "[[వర్గం:" + country_string + " క్రికెట్ క్రీడాకారులు" + "]]\n"

def get_country_test_details(nationality, played_test, gender):
    global famous_countries
    if not played_test:
        return ''
    country_string = get_nationality(nationality)
    if nationality in famous_countries.keys():
        country_string = famous_countries[nationality]
    if gender.startswith("F"):
        return "[[వర్గం:" + country_string + " మహిళా టెస్ట్ క్రికెట్ క్రీడాకారులు" + "]]\n"
    return "[[వర్గం:" + country_string + " టెస్ట్ క్రికెట్ క్రీడాకారులు" + "]]\n"
    
def get_country_odi_details(nationality, played_ODI, gender):
    global famous_countries
    if not played_ODI:
        return ''
    country_string = get_nationality(nationality)
    if nationality in famous_countries.keys():
        country_string = famous_countries[nationality]
    if gender.startswith("F"):
        return "[[వర్గం:" + country_string + " మహిళా వన్డే క్రికెట్ క్రీడాకారులు" + "]]\n" + "[[వర్గం:వన్డే క్రికెట్ క్రీడాకారులు]]\n"
    return "[[వర్గం:" + country_string + " వన్డే క్రికెట్ క్రీడాకారులు" + "]]\n" + "[[వర్గం:వన్డే క్రికెట్ క్రీడాకారులు]]\n"

def get_country_t20_details(nationality, played_t20, gender):
    global famous_countries
    if not played_t20:
        return ''
    t20_f = 'ట్వంటీ-20'
    if nationality != 'India':
        t20_f = 'టీ20'
    country_string = get_nationality(nationality)
    if nationality in famous_countries.keys():
        country_string = famous_countries[nationality]
    if gender.startswith("F"):
        return "[[వర్గం:" + country_string + " మహిళా " + t20_f + " క్రికెట్ క్రీడాకారులు" + "]]\n" + "[[వర్గం:ట్వంటీ-20 క్రికెటర్లు]]\n"
    return "[[వర్గం:" + country_string + " " + t20_f + " క్రికెట్ క్రీడాకారులు" + "]]\n" + "[[వర్గం:ట్వంటీ-20 క్రికెటర్లు]]\n"

def get_wk_category(player_role):
    if not player_role.startswith('W'):
        return ''
    return "[[వర్గం:వికెట్ కీపర్లు]]\n"

def getData(row):
    data = {
        #{%- macro get_categories_list(player_role, birth_year, death_year, nationality, gender, played_ODI, played_test, played_t20) -%}
        'birth_year': get_year(row['Birth_Date']),
        'death_year': get_year(row['Death_Date']),
        'nationality': row['Nationality'],
        'gender': row['Gender'],
        'played_ODI' : row['Batting_ODI_Mat'] > 0 or row['Bowling_ODI_Mat'] > 0, 
        'played_test': row['Batting_Test_Mat'] > 0 or row['Bowling_Test_Mat'] > 0, 
        'played_t20': row['Batting_T20I_Mat'] > 0 or row['Bowling_T20I_Mat'] > 0 or row['Batting_T20_Mat'] > 0 or row['Bowling_T20_Mat'] > 0,
        'player_role': row['Playing Role']
	}
    return data

cricket_players_DF = pd.DataFrame()
with open('../data_collection/data/final_cricket_players_translated_dataset_with_images.pkl', 'rb') as f:
    cricket_players_DF = pickle.load(f)
    cricket_players_DF.fillna(value="nan", inplace=True)
    
def main6(_id):
    global all_attributes
    file_loader = FileSystemLoader('./')
    env = Environment(loader=file_loader)
    template = env.get_template('categories.j2')
    
    func_dict = {        
        "get_country_player": get_country_player,
        "get_country_test_details": get_country_test_details,
        "get_country_odi_details": get_country_odi_details,
        "get_country_t20_details": get_country_t20_details,
        "get_wk_category": get_wk_category
    }
    template.globals.update(func_dict)
    required_player = cricket_players_DF.loc[cricket_players_DF['Cricinfo_id'] == _id]
    for j, row in required_player.iterrows():
        return template.render(getData(row))
