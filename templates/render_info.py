# Displays infobox and overview for a given player based on his/her information.

import pandas as pd
import ast
import pickle
from jinja2 import Environment, FileSystemLoader

# This function checks whether the given input is a valid one(Not nan)
def is_valid_string(attribute_value):
    if not isinstance(attribute_value, str) and not isinstance(attribute_value, float) and not isinstance(attribute_value, type(None)):
        return True
    return not (attribute_value == None or pd.isnull(attribute_value) or str(attribute_value) == "" or str(attribute_value) == "nan")

# Evaluates given entity
def get_literal(q):
    try:
        return ast.literal_eval(q)
    except:
        return 'nan'
    
# Returns the date from the list
# List is in the format [year,date,opponent team]
def date(row):
    if not is_valid_string(row):
        return 'nan'
    row = get_literal(row)
    if row == 'nan':
        return row
    return row[1]


# Converts the height into int
def height(row):
    if not is_valid_string(row):
        return 'nan'
    row = int(row)
    return row


# Returns the crininfo url of the player as a string
def get_source(profile_ref, player_name):
    return profile_ref + " " + player_name + " ప్రొఫైల్"


# Returns the crininfo url of the player as a reference in tewiki.
def get_profile_ref(profile_ref, player_name):
    if len(profile_ref) == 0:
        return ''
    return " <ref>[" + profile_ref + " " + player_name + " ప్రొఫైల్]</ref>"


# Returns the year from the list
# List is in the format [year,date,opponent team]
def year(row):
    if not is_valid_string(row):
        return 'nan'
    row = get_literal(row)
    if row == 'nan':
        return row
    return row[0]


# Returns the opponent team from the list
# List is in the format [year,date,opponent team]
def against(row):
    if not is_valid_string(row):
        return 'nan'
    row = get_literal(row)
    if row == 'nan':
        return row
    return row[-1]

# This function concates birth date of the player which is in the form of list into a string
def concate_birth(date):
    if len(date) == 1:
        return date[0]
    elif len(date) == 0:
        return "nan"
    else:
        li = ','.join(date)
        return li.rstrip()

# This function converts string list into list
def conv(t):
    t = get_literal(t)
    return t
# Returns a dict which contains the required information to render the jinja template
def getData(row):
    birth_date = row['Telugu_Birth_Date'].values[0]
    if not isinstance(birth_date, str):
        birth_date = '-1'
    birth_overview = row['Telugu_Birth_Date'].values[0]
    if not isinstance(birth_overview, str):
        birth_overview = '-1'
    if birth_date != '-1':
        birth_date = get_literal(row['Telugu_Birth_Date'].values[0])
        if birth_date != 'nan':
            birth_date = concate_birth(birth_date)
            birth_overview = birth_date.split(",")
            if len(birth_overview) == 2:
                if birth_overview[0].find('0') != -1:
                    birth_overview[0] = birth_overview[0].replace('0', '')
    pr = get_literal(row['References'].values[0])
    profile_ref = 'nan'
    if pr != 'nan':
        profile_ref = pr[0]
    AWARDS = row["awards_telugu"].values[0]
    if AWARDS != 'nan':
        AWARDS = AWARDS.split(',, ')
    data = {
        'Full_Name': row['Full_Name_Telugu'].values[0],
        'full_name_english': ' (' + row['Full Name'].values[0] + ')',
        'Wikipedia_image_link': row['Wikipedia_image_link'].values[0],
        'Player_Name': row['Player_Name_Telugu'].values[0],
        'Nationality': row['Nationality_Telugu'].values[0].strip(),
        'Born': birth_date,
        'Birth_place': row['Birth_Place_Telugu'].values[0],
        'Born_ov': birth_overview,
        'age': row['Age_telugu'].values[0],
        'Died': row['Died_telugu'].values[0],
        'Relations': row['Telugu_Relations'].values[0],
        'career_span': row['career_span'].values[0],
        'Batting_Style': row['Batting_Style_telugu'].values[0],
        'Bowling_Style': row['Bowling_Style_telugu'].values[0],
        'height_in_feets': height(row['height_in_feets'].values[0]),
        'height_in_inches': height(row['height_in_inches'].values[0]),
        'height_in_meters': row['height_in_meters'].values[0],
        'Gender': row['Gender'].values[0],

        'Playing_Role': row['Playing Role_Telugu'].values[0],
        'Teams': row['teams_ov_telugu_y'].values[0],
        'testdebutdate': date(row['Test_info_Matches_debut_Telugu'].values[0]),
        'testdebutyear': year(row['Test_info_Matches_debut_Telugu'].values[0]),
        'testdebutagainst': against(row['Test_info_Matches_debut_Telugu'].values[0]),
        'odidebutdate': date(row['ODI_info_Matches_debut_Telugu'].values[0]),
        'odidebutyear': year(row['ODI_info_Matches_debut_Telugu'].values[0]),
        'odidebutagainst': against(row['ODI_info_Matches_debut_Telugu'].values[0]),
        'T20Idebutdate': date(row['T20I_info_Matches_debut_Telugu'].values[0]),
        'T20Idebutyear': year(row['T20I_info_Matches_debut_Telugu'].values[0]),
        'T20Idebutagainst': against(row['T20I_info_Matches_debut_Telugu'].values[0]),
        'lasttestdate': date(row['Test_info_Matches_last_appearance_telugu'].values[0]),
        'lasttestyear': year(row['Test_info_Matches_last_appearance_telugu'].values[0]),
        'lasttestagainst': against(row['Test_info_Matches_last_appearance_telugu'].values[0]),
        'lastodidate': date(row['ODI_info_Matches_last_appearance_telugu'].values[0]),
        'lastodiyear': year(row['ODI_info_Matches_last_appearance_telugu'].values[0]),
        'lastodiagainst': against(row['ODI_info_Matches_last_appearance_telugu'].values[0]),
        'lastT20Idate': date(row['T20I_info_Matches_last_appearance_telugu'].values[0]),
        'lastT20Iyear': year(row['T20I_info_Matches_last_appearance_telugu'].values[0]),
        'lastT20Iagainst': against(row['T20I_info_Matches_last_appearance_telugu'].values[0]),
        'Major_trophies': row['trophy_names_Telugu'].values[0],
        "AWARDS": AWARDS,
        'profile_ref': profile_ref


    }
    return data

cricket_players_DF = pd.DataFrame()
with open('./data/final_cricket_players_translated_dataset_with_images.pkl', 'rb') as f:
    cricket_players_DF = pickle.load(f)
# Takes player cricinfo id as argument and returns corresponding template string associated with infobox and overview section.
def main1(_id):
    file_loader = FileSystemLoader('./')
    env = Environment(loader=file_loader)
    template = env.get_template('./templates/info.j2')
    glob = {'get_profile_ref': get_profile_ref, 'get_source': get_source, 'conv': conv, 'is_valid_string': is_valid_string}
    template.globals.update(glob)
    cricket_players_DF.fillna(value="nan", inplace=True)
    row = cricket_players_DF.loc[cricket_players_DF['Cricinfo_id'] == _id]
    return template.render(getData(row))
