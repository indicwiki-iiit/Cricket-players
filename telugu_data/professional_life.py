import pandas as pd
import pickle
import translators as ts
from deeptranslit import DeepTranslit
from deep_translator import GoogleTranslator
from google_trans_new import google_translator
from google.transliteration import transliterate_word, transliterate_text
import ast

translator = google_translator()
trans = DeepTranslit('telugu').transliterate
all_attributes = []

req_str = "Cricinfo_id, Player_Name, Player_Name_Telugu, FC Matches_debut, FC Matches_debut_Telugu, List A Matches_debut, List A Matches_debut_Telugu, T20 Matches_debut, T20 Matches_debut_Telugu, T20I Matches_debut, T20I Matches_debut_Telugu, ODI Matches_debut, ODI Matches_debut_Telugu, Test Matches_debut, Test Matches_debut_Telugu, Playing Role, Playing Role_Telugu, Nationality, Nationality_Telugu, Teams, Teams_Telugu,  trophy_names, trophy_names_Telugu"
cols = req_str.split(', ')
print(cols)


def is_valid_string(attribute_value):
    if not isinstance(attribute_value, str):
        return True
    return not (attribute_value == None or pd.isnull(attribute_value) or str(attribute_value) == "" or str(attribute_value) == "nan")


def getTransliteratedDescription(description):
    try:
        current_attribute_value = description
        # anu_title = telugu.anuvaad(row.title.values[0])
        deep = trans(current_attribute_value)[0]
        description = deep['pred']
    except:
        try:
            return transliterate_text(test_text, lang_code='te')
        except:
            pass
    return description


def getTranslatedDescription(description):
    global translator
    if isinstance(description, str) and not is_valid_string(description):
        return description
    try:
        # print('1')
        return translator.translate(description, lang_src='en', lang_tgt='te')
    except:
        try:
            # print('2')
            return ts.google(query_text=description, from_language='en', to_language='te')
        except:
            try:
                # print('3')
                return GoogleTranslator(source='en', target='te').translate(text=description)
            except:
                return description

def can_consider_trophy_stat(stat_name, all_trophies):
    return len([ke for ke in all_trophies.keys() if stat_name in all_trophies[ke].keys() and is_valid_string(all_trophies[ke][stat_name])]) != 0

def get_trophy_name(description):
    if not is_valid_string(description):
        return ''
    trophy_translations = {
        "Basil D'Oliveira": "బాసిల్ డి'ఒలివెరా",
        'World Cup': 'ప్రపంచ కప్',
        'ICC World Test Champ': 'ఐసిసి ప్రపంచ టెస్ట్ ఛాంపియన్‌షిప్',
        'Frank Worrell Trophy': 'ఫ్రాంక్ వొరెల్ ట్రోఫీ',
        'Border-Gavaskar': 'బోర్డర్-గవాస్కర్ ట్రోఫీ',
        "Men's T20 World Cup": 'టీ20 ప్రపంచ కప్',
        'The Ashes': 'ది యాషెస్',
        'World Cup Qualifier': 'ప్రపంచ కప్ క్వాలిఫైయర్',
        'Chappell-Hadlee': 'చాపెల్-హాడ్లీ',
        'Trans-Tasman Trophy': 'ట్రాన్స్-టాస్మాన్ ట్రోఫీ',
        'WCL Championship': 'ప్రపంచ క్రికెట్ లీగ్ ఛాంపియన్‌షిప్',
        'ICC Champions Trophy': 'ఐసిసి ఛాంపియన్స్ ట్రోఫీ',
        'The Wisden Trophy': 'ది విస్డెన్ ట్రోఫీ',
        'Asia Cup': 'ఆసియా కప్'
    }
    if not description in trophy_translations.keys():
        return getTransliteratedDescription(description)
    return trophy_translations[description]


def get_trophy_names_list(given_trophy_list):
    if not is_valid_string(given_trophy_list):
        return ''
    trophy_list = list(given_trophy_list)
    for i in range(len(trophy_list)):
        trophy_list[i] = get_trophy_name(trophy_list[i])
    return ', '.join(trophy_list)


def get_trophy_info(row):
    global all_attributes
    if not is_valid_string(row['Major_Trophies']):
        return [], [], {}
    all_trophies = ast.literal_eval(row['Major_Trophies'])
    if len(all_trophies) == 0:
        return [], [], {}
    trophy_names = [name for name in all_trophies.keys()
                    if len(all_trophies[name]) > 0]
    trophy_stat_names = []
    if len(trophy_names) == 0:
        return [], [], {}
    for ke in all_trophies[trophy_names[0]].keys():
        if can_consider_trophy_stat(ke, all_trophies):
            trophy_stat_names.append(ke)
    trophy_details = {}
    for key1 in all_trophies.keys():
        if key1 in trophy_names:
            trophy_details[key1] = {}
        else:
            continue
        for key2 in all_trophies[key1].keys():
            if key2 in trophy_stat_names:
                trophy_details[key1][key2] = all_trophies[key1][key2]
    # for i in range(len(trophy_names)):
    #     trophy_names[i] = getTransliteratedDescription(trophy_names[i])
    trophy_stat_names = [t_stat for t_stat in trophy_stat_names if not t_stat in [
        'tt', 'pr', 'hn', 'bbad']]
    return trophy_names, trophy_stat_names, trophy_details


def get_role(role):
    if not is_valid_string(role):
        return ''
    role_map = {
        "Bowler": "బౌలర్",
        "Allrounder": "ఆల్ రౌండర్",
        "Batter": "బ్యాట్స్‌మన్‌",
        "Opening batter": "ఓపెనింగ్ బ్యాట్స్‌మన్‌",
        "Wicketkeeper batter": "వికెట్ కీపర్ బ్యాట్స్‌మన్‌",
        "Top order batter": "టాప్ ఆర్డర్ బ్యాట్స్‌మన్‌",
        "Middle order batter": "మిడిల్ ఆర్డర్ బ్యాట్స్‌మన్",
        "Wicketkeeper": "వికెట్ కీపర్",
        "Bowling allrounder": "బౌలింగ్ ఆల్ రౌండర్",
        "Batting allrounder": "బ్యాటింగ్ ఆల్ రౌండర్"
    }
    if not role in role_map.keys():
        return role
    return role_map[role]


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


def get_debut_string(deb):
    # print(deb)
    if not is_valid_string(deb):
        return ''
    deb = deb.replace("vs", "versus")
    deb = deb.replace("Vs", "versus")
    deb = deb.replace("vS", "versus")
    deb = deb.replace("VS", "versus")
    occ = deb.find(" at ")
    if occ == -1:
        return getTransliteratedDescription(deb)
    deb = deb[:occ] + ', ' + deb[occ:]
    occ = deb.find(" at ")
    occ2 = deb.find("-")
    if occ2 == -1:
        occ2 = len(deb)
    curr_sub = deb[occ:occ2]
    # print(curr_sub)
    tokens = curr_sub.split(' ')
    tokens.append('lo ')
    deb = deb.replace(curr_sub, ' '.join(tokens[2:]))
    partition = deb.find('lo ')
    partition += 3
    return getTransliteratedDescription(deb[:partition]) + getTranslatedDescription(deb[partition:])


def get_teams_string(teams_list):
    if not is_valid_string(teams_list):
        return ''
    actual_list = ast.literal_eval(teams_list)
    capitals = {
        'Super 3s': 'సూపర్ ౩స్', 'SC': 'ఎస్.సీ.', 'Glamorgan 2nd': 'గ్లమోర్గన్ 2న్ద్', 
        'HBS': 'హెచ్.బీ.ఎస్.', 'BCCSL': 'బీ.సీ.సీ.ఎస్.ఎల్.', 'Leicestershire 2nd': 'లీసెస్టర్షైర్ 2న్ద్', 
        'CH': 'సీ.హెచ్.', 'ECB': 'ఇ.సీ.బీ.', 'C': 'సీ.', 'Warwickshire 2nd': 'వార్విక్షైర్ 2న్ద్', 
        'UWI': 'యూ.డబల్యూ.ఐ.', 'PINT': 'పి.ఐ.ఎన్.టి.', 'Surrey 2nd': 'సర్రే 2న్ద్', 
        'NZCPA': 'ఎన్.జీ.సీ.పి.ఏ.', 'Lancashire 2nd': 'లాంక్షైర్ 2న్ద్', 
        'Essex 2nd': 'ఎస్సెక్స్ 2న్ద్', 'BCB': 'బీ.సీ.బీ.', '1': '1', 
        'Somerset 2nd': 'సోమర్సెట్ 2న్ద్', 'DVS': 'డి.వీ.ఎస్.', 'XI': 'XI', 
        'Kent 2nd': 'కెంట్ 2న్ద్', "Men's 1": "మెన్'స్ 1", 'KNCB': 'కె.ఎన్.సీ.బీ.', 
        'CA': 'సీ.ఏ.', 'MCA': 'ఎం.సీ.ఏ.', 'VII': 'VII', 'Patriots 1': 'పేట్రియాట్స్ 1', '19': '19', 
        'AJ': 'ఏ.జె.', 'BCA': 'బీ.సీ.ఏ.', 'HCC': 'హెచ్.సీ.సీ.', 'PCA': 'పి.సీ.ఏ.', 'TN': 'టి.ఎన్.', 
        'P': 'పి.', 'UCB-BCB': 'యూ.సీ.బీ.-బీ.సీ.బీ.', 'RR': 'ఆర్.ఆర్.', 'Sussex 2nd': 'సస్సెక్స్ 2న్ద్', 
        'MAF': 'ఎం.ఏ.ఎఫ్.', 'ICBT': 'ఐ.సీ.బీ.టి.', 'DS': 'డి.ఎస్.', 'World-XI': 'వరల్డ్-XI', 'ICL': 'ఐ.సీ.ఎల్.', 
        'Worcestershire 2nd': 'వోర్సెస్టర్షైర్ 2న్ద్', 'XII': 'XII', 'DH': 'డి.హెచ్.', 'VRA': 'వీ.ఆర్.ఏ.', 
        'ICC': 'ఐసీసీ', 'Under-17': 'అండర్ -17', 'VOC': 'వీ.ఓ.సీ.', 'NCA': 'ఎన్.సీ.ఏ.', 
        'MCCU': 'ఎం.సీ.సీ.యూ.', 'IV': 'IV', 'MV': 'ఎం.వీ.', 'Durham 2nd': 'డర్హామ్ 2న్ద్', 'B': 'బీ', 
        'RCA': 'ఆర్.సీ.ఏ.', 'KSCA': 'కె.ఎస్.సీ.ఏ.', 'Northern 2nd': 'నార్తర్న్ 2న్ద్', 'WICB': 'డబల్యూ.ఐ.సీ.బీ.', 
        'FATA': 'ఎఫ్.ఏ.టి.ఏ.', 'DY': 'డి.వై.', 'TNCA': 'టి.ఎన్.సీ.ఏ.', 'NCU': 'ఎన్.సీ.యూ.', 'S': 'ఎస్.', 
        'CPL': 'సీ.పి.ఎల్.', 'YMCA': 'వై.ఎం.సీ.ఏ.', 'Yorkshire 2nd': 'యార్క్షైర్ 2న్ద్', 'T20': 'టి20', 'PJ': 'పి.జె.', 
        'Patriots 2': 'పేట్రియాట్స్ 2', 'UCCE': 'యూ.సీ.సీ.ఇ.', 'Middlesex 2nd': 'మిడిల్‌సెక్స్ 2న్ద్', 'Under-23': 'అండర్-23', 
        'D.A.V': 'డి.ఏ.వీ.', 'HDG': 'హెచ్.డి.జీ.', 'CC': 'సీ.సీ.', 'MAS': 'ఎం.ఏ.ఎస్.', 'ACB': 'ఏ.సీ.బీ.', 'UAE': 'యూ.ఏ.ఇ.', 
        'Under 19': 'అండర్ 19', '2': '2', 'MC': 'ఎం.సీ.', 'AJK': 'ఏ.జె.కె.', 'CI': 'సీ.ఐ.', 'TUKS': 'టి.యూ.కె.ఎస్.', 
        'Pakhtunkhwa 2nd': 'పఖ్తున్ఖ్వా 2న్ద్', 'Sindh 2nd': 'సింధ్ 2న్ద్', 'DOHS': 'డి.ఓ.హెచ్.ఎస్.', 'TUTI': 'టి.యూ.టి.ఐ.', 
        'Gloucestershire 2nd': 'గ్లౌసెస్టర్షైర్ 2న్ద్', 'Hampshire 2nd': 'హాంప్‌షైర్ 2న్ద్', 'D': 'డి.', 'Derbyshire 2nd': 'డెర్బీషైర్ 2న్ద్', 
        'MCCU 2nd': 'ఎం.సీ.సీ.యూ. 2న్ద్', 'A': 'ఏ.', 'VB': 'వీ.బీ.', 'Nottinghamshire 2nd': 'నాటింగ్హామ్షైర్ 2న్ద్', 
        'Northamptonshire 2nd': 'నార్తాంప్టన్షైర్ 2న్ద్', 'KZKC': 'కె.జీ.కె.సీ.', 'DJ': 'డి.జె.', 
        'Under-11s': 'అండర్ -11స్', 'Under-22s': 'అండర్ -22స్', 'Under-17s': 'అండర్ -17స్', 'Under': 'అండర్', 
        'Under-15s': 'అండర్ -15స్', 'Under-25s': 'అండర్ -25స్', 'Under-20s': 'అండర్ -20స్', 'Under-21s': 'అండర్ -21స్', 
        'Under-13s': 'అండర్ -13స్', 'Under-14s': 'అండర్ -14స్', 'Under-18s': 'అండర్ -18స్', 'Under-24s': 'అండర్ -24స్', 
        'Under-19s': 'అండర్ -19స్', 'Under-16s': 'అండర్ -16స్', 'Under-23s': 'అండర్ -23స్' 
    }
    translated_output = ""
    twos = [ke for ke in capitals.keys() if len(ke.split(" ")) == 2]
    ones = [ke for ke in capitals.keys() if len(ke.split(" ")) == 1]
    try:
        for j in range(len(actual_list)):
            # print("Actual team name", actual_list[j])
            tokenized = actual_list[j].split(" ")
            for i in range(len(tokenized)-1):
                cur = tokenized[i] + " " + tokenized[i+1]
                if cur in twos:
                    t = capitals[cur].split(" ")
                    tokenized[i] = t[0]
                    tokenized[i+1] = t[1]
            for i in range(len(tokenized)):
                if tokenized[i] in ones:
                    tokenized[i] = capitals[tokenized[i]]
            actual_list[j] = ' '.join(tokenized)
            # print("Updated team name", actual_list[j])
        translated_output = getTransliteratedDescription(
            ', '.join(actual_list))      
        return translated_output
    except Exception as e:
        print("Level 2", e)
        try:
            translated_output = getTranslatedDescription(actual_list)
            if ']]' in translated_output:
                translated_output = translated_output.replace(']]', ']')
            actual_list = list(ast.literal_eval(translated_output))
            return ', '.join(actual_list)
        except Exception as f:
            print("Level 3", f)
            try:
                translated_output = getTranslatedDescription(
                    ', '.join(actual_list))
                return translated_output
            except Exception as g:
                print("Final level", g)
                return ', '.join(actual_list)


def get_db_val(row, attribute_name):
    if "debut" in attribute_name:
        attribute_name = attribute_name.replace('_Telugu', '')
        return get_debut_string(row[attribute_name])
    if attribute_name == "Player_Name_Telugu":
        return getTransliteratedDescription(row['Player_Name']).strip()
    if attribute_name == "Playing Role_Telugu":
        return get_role(row["Playing Role"])
    if attribute_name == "Nationality_Telugu":
        return get_nationality(row["Nationality"])
    if "trophy_names" in attribute_name:
        trophy_names, trophy_stat_names, trophy_details = get_trophy_info(row)
        if not "Telugu" in attribute_name:
            return ', '.join(trophy_names)
        return get_trophy_names_list(trophy_names)
    return get_teams_string(row['Teams'])


with open('final_cricket_players_DF.pkl', 'rb') as f:
    cricket_players_DF = pickle.load(f)
    all_attributes = cricket_players_DF.columns.tolist()
    cricket_players_DF.fillna(value="nan", inplace=True)
    ids = cricket_players_DF.Cricinfo_id.tolist()
    final_data = []
    for i, cricketer_id in enumerate(ids):
        required_player = cricket_players_DF.loc[cricket_players_DF['Cricinfo_id'] == cricketer_id]
        if i % 100 == 0:
            print(f'{i} players done')
        for j, row in required_player.iterrows():
            # print(row)
            curr_player_list = []
            for att in cols:
                if att in all_attributes:
                    curr_player_list.append(row[att])
                else:
                    curr_player_list.append(get_db_val(row, att))
            final_data.append(curr_player_list)
    a = pd.DataFrame(final_data, columns=cols)
    a = a.drop_duplicates()
    a = a.drop_duplicates('Cricinfo_id')
    a.drop(a.columns[a.columns.str.contains(
        'unnamed', case=False)], axis=1, inplace=True)
    a.to_csv('professional_life_trans.csv', index=False)
