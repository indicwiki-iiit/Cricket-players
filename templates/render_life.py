# Displays relevant professional life details for a given player based on his/her information

import pickle
import random
import ast
import pandas as pd
from functools import cmp_to_key
from jinja2 import Environment, FileSystemLoader

all_attributes = []
month_names = {
    'February': 'ఫిబ్రవరి', 'December': 'డిసెంబర్', 'May': 'మే', 'October': 'అక్టోబర్',
    'January': 'జనవరి', 'November': 'నవంబర్', 'April': 'ఏప్రిల్', 'March': 'మార్చి',
    'September': 'సెప్టెంబర్', 'June': 'జూన్', 'August': 'ఆగస్టు', 'July': 'జూలై'
}

# Hardcoding for displaying stats in table based on their priority index
bat_stat_order = {
    "Mat": 1,
    "Inns": 2,
    "NO": 5,
    "Runs": 3,
    "HS": 4,
    "Ave": 6,
    "100s": 9,
    "50s": 10,
    "Ct": 13,
    "St": 14,
    "BF": 8,
    "SR": 7,
    "4s": 11,
    "6s": 12
}

bowl_stat_order = {
    "Mat": 1,
    "Inns": 2,
    "Balls": 3,
    "Runs": 4,
    "Wkts": 5,
    "BBI": 6,
    "BBM": 7,
    "Ave": 8,
    "Econ": 9,
    "SR": 10,
    "4w": 11,
    "5w": 12,
    "10w": 13
}

# Hardcoding few common stat names for display
translated_names = {
    'rn': "పరుగులు",
    'bta': "సగటు బ్యాటింగ్ స్కోరు",
    'st': "స్టంపింగ్స్",
    'dk': 'డక్లు',
    'ft': 'అర్ధ శతకాలు',
    'fw': "ఐదు వికెట్ మ్యాచ్‌లు",
    'mt': "మ్యాచ్‌లు",
    'btsr': "స్ట్రైక్ రేట్",
    'bbi': "ఉత్తమ బౌలింగ్ ఇన్నింగ్స్",
    'hs': "అత్యధిక స్కోరు",
    'wk': "వికెట్లు",
    'ct': "క్యాచ్‌లు",
    'bwa': "సగటు బౌలింగ్ స్కోరు",
    'sp': "వ్యవధి",
    "Mat": "మ్యాచ్‌లు",
    "Inns": "ఇన్నింగ్స్",
    "in": "ఇన్నింగ్స్",
    "NO": "నాట్-అవుట్స్",
    "no": "నాట్-అవుట్స్",
    "Runs": "పరుగులు",
    "HS": "అత్యధిక స్కోరు",
    "Ave": "సగటు బ్యాటింగ్ స్కోరు",
    "Avg": "సగటు బ్యాటింగ్ స్కోరు",
    "100s": "శతకాలు",
    "50s": "అర్ధ శతకాలు",
    "Ct": "క్యాచ్‌లు",
    "St": "స్టంపింగ్స్",
    "BF": "ఎదురుకున్న బంతులు",
    "bf": "ఎదురుకున్న బంతులు",
    "SR": "స్ట్రైక్ రేట్",
    "0s": "జీరోలు",
    "4s": "ఫోర్లు",
    'fo': "ఫోర్లు",
    'si': "సిక్సలు",
    "6s": "సిక్సలు",
    "Balls": "బంతులు",
    "Wkts": "వికెట్లు",
    "BBI": "ఉత్తమ బౌలింగ్ ఇన్నింగ్స్",
    "BBM": "ఉత్తమ బౌలింగ్ మ్యాచ్",
    "Econ": "ఎకానమీ",
    "4w": "నాలుగు వికెట్ మ్యాచ్‌లు",
    "5w": "ఐదు వికెట్ మ్యాచ్‌లు",
    "10w": "పది వికెట్ మ్యాచ్‌లు",
    "Span": "వ్యవధి",
    "Test": "టెస్ట్",
    "ODI": "వన్డే ఇంటర్నేషనల్‌",
    "T20": "టీ20",
    "T20I": "అంతర్జాతీయ టీ20",
    "FC": "ఫస్ట్ క్లాస్",
    "List A": "లిస్ట్ ఏ"
}

# Checks if given argument is indeed a valid string in the dataset
def is_valid_string(attribute_value):
    if not isinstance(attribute_value, str) and not isinstance(attribute_value, float) and not isinstance(attribute_value, type(None)):
        return True
    return not (attribute_value == None or pd.isnull(attribute_value) or str(attribute_value) == "" or str(attribute_value) == "nan")

# Returns translated trophy name
def get_trophy_name(description):
    if not is_valid_string(description) or description == None or pd.isnull(description):
        return ''
    trophy_translations = {
        "Basil D'Oliveira": "బాసిల్ డి'ఒలివెరా",
        'World Cup': '[[ప్రపంచ కప్]]',
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
        'Asia Cup': 'ఆసియా కప్',
        "ICC Women's Champ": 'ఐసిసి విమెన్స్ ఛాంపియన్షిప్',
        "ICC Women's World Cu": 'ఐసిసి విమెన్స్ ప్రపంచ కప్',
        'Rose Bowl': 'రోజ్ బౌల్'
    }
    return trophy_translations[description]

# Returns translated nationality of a player
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

# Takes a list of trophies as an argument and returns a string with its translation
def get_trophy_names_list(given_trophy_list):
    if not is_valid_string(given_trophy_list):
        return ''
    trophy_list = list(given_trophy_list)
    for i in range(len(trophy_list)):
        trophy_list[i] = get_trophy_name(trophy_list[i])
    return ', '.join(trophy_list)

# Returns a url corresponding to details related to given player's debut matches
def get_matches_ref(all_ref, player_name):
    if not is_valid_string(all_ref):
        return ''
    required_ref = [r for r in all_ref if "matches" in r]
    if len(required_ref) == 0:
        return ''
    return "<ref>[" + required_ref[0] + " " + player_name.strip() + " మ్యాచ్‌లు]</ref>"

# Returns a url corresponding to details related to given player's stats in batting, bowling, fielding
def get_stats_ref(all_ref, player_name):
    if not is_valid_string(all_ref):
        return ''
    required_ref = [r for r in all_ref if "stats" in r]
    if len(required_ref) == 0:
        return ''
    return "<ref>[" + required_ref[0] + " " + player_name.strip() + " గణాంకాలు]</ref>"

# Processes given stat and returns appropriate response by altering it if necessary
def stat_value(attribute_name, attribute_value):
    if not is_valid_string(attribute_value) or attribute_value == None or pd.isnull(attribute_value):
        return "-"
    if "hs" in attribute_name.lower() or "bbi" in attribute_name.lower() or "BBM" in attribute_name or "span" in attribute_name.lower() or attribute_name == 'sp':
        return attribute_value
    if int(float(attribute_value)) < 0:
        return "-"
    return attribute_value

# Comparator for displaying stats based on priority index
def bat_comparator(a, b):
    global bat_stat_order
    if bat_stat_order[a] > bat_stat_order[b]:
        return 1
    return -1

# Method for displaying stats based on priority index
def get_bat_atts_sorted(bat_stats_list):
    return sorted(bat_stats_list, key=cmp_to_key(bat_comparator))

# Comparator for displaying stats based on priority index
def bowl_comparator(a, b):
    global bowl_stat_order
    if bowl_stat_order[a] > bowl_stat_order[b]:
        return 1
    return -1

# Method for displaying stats based on priority index
def get_bowl_atts_sorted(bowl_stats_list):
    return sorted(bowl_stats_list, key=cmp_to_key(bowl_comparator))

# dummy function
def print_names(li):
    return (li)

# Returns translated role of a given player
def get_role(role):
    if not is_valid_string(role) or role == None or pd.isnull(role):
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

# randomly shuffles a given list
def shuffle_list(given_list):
    result = list(given_list)
    random.shuffle(result)
    return result

# Returns a sentence based on available batting stats
def batting_description_func(first_word, gender_pronoun_2, num1, num2):
    if num1 <= 0 and num2 <= 0:
        return ''
    if num1 > 0 and num2 > 0:
        return (first_word + ' ' + gender_pronoun_2 + ' సగటు స్కోరు ' + str(num1) + ', స్ట్రైక్ రేట్ ' + str(num2) + '. ')
    elif num1 > 0:
        return (first_word + ' ' + gender_pronoun_2 + ' సగటు స్కోరు ' + str(num1) + '. ')
    return (first_word + ' ' + gender_pronoun_2 + ' స్ట్రైక్ రేట్ ' + str(num2) + '. ')

# Returns a sentence based on available bowling stats
def bowling_description_func(first_word, gender_pronoun_2, num1, num2):
    if num1 <= 0 and num2 <= 0:
        return ''
    if num1 > 0 and num2 > 0:
        return (first_word + ' ' + gender_pronoun_2 + ' సగటు బౌలింగ్ స్కోరు ' + str(num1) + ', ఎకానమీ రేట్ ' + str(num2) + '. ')
    elif num1 > 0:
        return (first_word + ' ' + gender_pronoun_2 + ' సగటు బౌలింగ్ స్కోరు ' + str(num1) + '. ')
    return (first_word + ' ' + gender_pronoun_2 + ' ఎకానమీ రేట్ ' + str(num2) + '. ')

# Introductory sentence for a player's batting/bowling career information
def opening_sentence(first_word, player_name, num1, num2, has_played):
    if num1 <= 0 and num2 <= 0:
        return ''
    match_word = 'మ్యాచ్‌లు'
    if num1 == 1:
        match_word = 'మ్యాచ్‌'
    innings_word = 'ఇన్నింగ్స్‌లలో'
    if num2 == 1:
        innings_word = 'ఇన్నింగ్స్‌లో'
    if num1 > 0 and num2 > 0:
        return (first_word + ' ' + player_name + ' ' + str(num1) + ' ' + match_word + ', ' + str(num2) + ' ' + innings_word + ' ' + has_played + '. ')
    elif num1 > 0:
        return (first_word + ' ' + player_name + ' ' + str(num1) + ' ' + match_word + ' ' + has_played + '. ')
    return (first_word + ' ' + player_name + ' ' + str(num2) + ' ' + innings_word + ' ' + has_played + '. ')

# Returns a sentence based on available batting stats
def batting_sent1(gender_pronoun_1, sum_batting_100s, sum_batting_50s, has_done):
    if sum_batting_100s <= 0 and sum_batting_50s <= 0:
        return ''
    hundred_word = 'శతకాలు'
    if sum_batting_100s == 1:
        hundred_word = 'శతకం'
    fifty_word = 'అర్ధ శతకాలు'
    if sum_batting_50s == 1:
        fifty_word = 'అర్ధ శతకం'
    if sum_batting_100s > 0 and sum_batting_50s > 0:
        return ('అన్ని ఫార్మాట్లు కలిపి ' + gender_pronoun_1 + ' ' + str(sum_batting_100s) + ' ' + hundred_word + ', ' + str(sum_batting_50s) + ' ' + fifty_word + ' ' + has_done + '. ')
    elif sum_batting_100s > 0:
        return ('అన్ని ఫార్మాట్లు కలిపి ' + gender_pronoun_1 + ' ' + str(sum_batting_100s) + ' ' + hundred_word + ' ' + has_done + '. ')
    return ('అన్ని ఫార్మాట్లు కలిపి ' + gender_pronoun_1 + ' ' + str(sum_batting_50s) + ' ' + fifty_word + ' ' + has_done + '. ')

# Returns a sentence based on available bowling stats
def bowling_sent1(gender_pronoun_1, sum_bowling_balls, has_done, sum_wickets, has_taken):
    if sum_bowling_balls <= 0 and sum_wickets <= 0:
        return ''
    balls_word = 'బంతులు'
    overs_word = 'ఓవర్లు'
    wickets_word = 'వికెట్లు'
    if sum_bowling_balls == 1:
        balls_word = 'బంతి'
    if sum_wickets == 1:
        wickets_word = 'వికెట్'
    if sum_bowling_balls//6 == 1:
        overs_word = 'ఓవర్'
    if sum_bowling_balls > 0 and sum_wickets > 0:
        return ('తన కెరీర్ లో, ' + gender_pronoun_1 + ' మొత్తం ' + str(sum_bowling_balls) + ' ' + balls_word + ' (' + str(sum_bowling_balls//6) + ' ' + overs_word + ') బౌలింగ్ చేసి, ' + str(sum_wickets) + ' ' + wickets_word + ' ' + has_taken + '. ')
    elif sum_bowling_balls > 0:
        return ('తన కెరీర్ లో, ' + gender_pronoun_1 + ' మొత్తం ' + str(sum_bowling_balls) + ' ' + balls_word + ' (' + str(sum_bowling_balls//6) + ' ' + overs_word + ') బౌలింగ్ ' + has_done + '. ')
    return ('తన కెరీర్ లో ' + str(sum_wickets) + ' ' + wickets_word + ' ' + has_taken + '. ')

# Returns a sentence based on available bowling stats
def bowling_sent2(gender_pronoun_2, gender_pronoun_1, bowling_10w_test, bowling_10w_FC, has_taken):
    if bowling_10w_test <= 0 and bowling_10w_FC <= 0:
        return ''
    test_word = 'టెస్ట్ మ్యాచ్‌లలో'
    if bowling_10w_test == 1:
        test_word = 'టెస్ట్ మ్యాచ్ లో'
    fc_word = 'ఫస్ట్ క్లాస్ మ్యాచ్‌లలో'
    if bowling_10w_FC == 1:
        fc_word = 'ఫస్ట్ క్లాస్ మ్యాచ్‌ లో'
    if bowling_10w_test > 0 and bowling_10w_FC > 0:
        return (gender_pronoun_2 + ' కెరీర్లో, ' + gender_pronoun_1 + ' ' + str(bowling_10w_test) + ' ' + test_word + ', ' + str(bowling_10w_FC) + ' ' + fc_word + ' 10 వికెట్లు ' + has_taken + '. ')
    elif bowling_10w_test > 0:
        return (gender_pronoun_2 + ' కెరీర్లో, ' + gender_pronoun_1 + ' ' + str(bowling_10w_test) + ' ' + test_word + ' 10 వికెట్లు ' + has_taken + '. ')
    return (gender_pronoun_2 + ' కెరీర్లో, ' + gender_pronoun_1 + ' ' + str(bowling_10w_FC) + ' ' + fc_word + ' 10 వికెట్లు ' + has_taken + '. ')

# Returns translated output of given stat
def get_translation(word, prefix_string):
    global translated_names
    if not is_valid_string(word) or word == None or pd.isnull(word):
        return ''
    if not word in translated_names.keys():
        return word
    if word == "SR":
        if prefix_string == 'Batting_':
            return translated_names[word]
        return "బౌలింగ్ స్ట్రైక్ రేట్"
    if word == "Ave":
        if prefix_string == 'Batting_':
            return translated_names[word]
        return "సగటు బౌలింగ్ స్కోరు"
    return translated_names[word]

# Checks if given attribute is in given list
def null_check(given_list, given_att):
    for element in given_list:
        if '_' + element + '_' in given_att:
            return True
    return False

# Decides if the row corresponding to a particular cricket format should be considered or not
def can_be_considered_1(attributes, prop_name, row, curr_att):
    req_attrs = [a for a in attributes if '_' + prop_name + '_' in a]
    req_list = [a for a in req_attrs if (isinstance(row[a], str) and is_valid_string(row[a])) or (
        (not isinstance(row[a], str)) and stat_value(a, row[a]) != "-" and stat_value(a, row[a]) > 0)]
    valids_count = len(req_list)
    return valids_count != 0

# Decides if the row corresponding to a particular cricket stat should be considered or not
def can_be_considered_2(attributes, prop_name, row, curr_att, other_list):
    req_attrs = [
        a for a in attributes if prop_name in a and null_check(other_list, a)]
    req_list = [a for a in req_attrs if (isinstance(row[a], str) and is_valid_string(row[a])) or (
        (not isinstance(row[a], str)) and stat_value(a, row[a]) != "-" and stat_value(a, row[a]) > 0)]
    valids_count = len(req_list)
    return valids_count != 0

# Get all relevant batting information about the player
def get_batting_info(row):
    global all_attributes
    bat_attributes = [att for att in all_attributes if "Batting_" in att and (
        not "_Ct" in att) and (not "_St" in att) and att != 'Batting_Style_telugu']
    batting_format_names = []
    batting_stat_names = []
    batting_details = {}
    # print(row['Batting_T20_Mat'])

    for att in bat_attributes:
        curr_att = att.split('_')
        # print(curr_att)
        if can_be_considered_1(bat_attributes, curr_att[1], row, curr_att):
            batting_format_names.append(curr_att[1])
    for att in bat_attributes:
        curr_att = att.split('_')
        # print(curr_att)
        if can_be_considered_2(bat_attributes, curr_att[2], row, curr_att, batting_format_names):
            batting_stat_names.append(curr_att[2])

    batting_format_names = list(set(batting_format_names))
    batting_stat_names = get_bat_atts_sorted(list(set(batting_stat_names)))

    for format_name in batting_format_names:
        for stat_name in batting_stat_names:
            attribute_name = "Batting_" + format_name + "_" + stat_name
            batting_details[attribute_name] = row[attribute_name]
    return batting_format_names, batting_stat_names, batting_details

# Get all relevant bowling information about the player
def get_bowling_info(row):
    global all_attributes
    bowl_attributes = [
        att for att in all_attributes if "Bowling_" in att and att != 'Bowling_Style_telugu']
    # print(bowl_attributes)
    bowling_format_names = []
    bowling_stat_names = []
    bowling_details = {}

    for att in bowl_attributes:
        curr_att = att.split('_')
        if can_be_considered_1(bowl_attributes, curr_att[1], row, curr_att):
            bowling_format_names.append(curr_att[1])
    for att in bowl_attributes:
        curr_att = att.split('_')
        if can_be_considered_2(bowl_attributes, curr_att[2], row, curr_att, bowling_format_names):
            bowling_stat_names.append(curr_att[2])

    bowling_format_names = list(set(bowling_format_names))
    bowling_stat_names = get_bowl_atts_sorted(list(set(bowling_stat_names)))

    for format_name in bowling_format_names:
        for stat_name in bowling_stat_names:
            if stat_name == "10w" and not format_name in ["Test", "FC"]:
                continue
            attribute_name = "Bowling_" + format_name + "_" + stat_name
            bowling_details[attribute_name] = row[attribute_name]
    return bowling_format_names, bowling_stat_names, bowling_details

# Get all relevant fielding information about the player
def get_fielding_info(row):
    global all_attributes
    field_attributes = [att for att in all_attributes if "Batting_" in att and (
        "_Ct" in att or "_St" in att or "Mat" in att or "Inns" in att) and att != 'Batting_Style_telugu']
    fielding_format_names = []
    fielding_stat_names = []
    fielding_details = {}

    for att in field_attributes:
        curr_att = att.split('_')
        if can_be_considered_1(field_attributes, curr_att[1], row, curr_att):
            fielding_format_names.append(curr_att[1])
    for att in field_attributes:
        curr_att = att.split('_')
        if can_be_considered_2(field_attributes, curr_att[2], row, curr_att, fielding_format_names):
            fielding_stat_names.append(curr_att[2])

    fielding_format_names = list(set(fielding_format_names))
    fielding_stat_names = get_bat_atts_sorted(list(set(fielding_stat_names)))

    for format_name in fielding_format_names:
        for stat_name in fielding_stat_names:
            attribute_name = "Batting_" + format_name + "_" + stat_name
            fielding_details[attribute_name] = row[attribute_name]
    return fielding_format_names, fielding_stat_names, fielding_details

# Decides if the row corresponding to a particular cricket stat of a major trophy should be considered or not
def can_consider_trophy_stat(stat_name, all_trophies):
    valid_entries = [all_trophies[ke][stat_name] for ke in all_trophies.keys() if stat_name in all_trophies[ke].keys() and is_valid_string(
        all_trophies[ke][stat_name]) and not (all_trophies[ke][stat_name] == None or pd.isnull(all_trophies[ke][stat_name]))]
    valid_entries = [entry for entry in valid_entries if (isinstance(
        entry, str) and entry != '-') or ((isinstance(entry, int) or isinstance(entry, float)) and entry > 0)]
    # print(valid_entries)
    return len(valid_entries) != 0

# Get all information related to major trophies the player played in
def get_trophy_info(row):
    global all_attributes
    if not is_valid_string(row['Major_Trophies']) or row['Major_Trophies'] == None or pd.isnull(row['Major_Trophies']):
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

# Perform some calculations on player attributes and return some statistics for analysis and display
def get_description_sums(row):
    global all_attributes

    bat_match_attrs = [
        att for att in all_attributes if "Batting_" in att and "Mat" in att]
    sum_batting_matches = sum([row[att]
                              for att in bat_match_attrs if row[att] > 0])

    bat_inns_attrs = [
        att for att in all_attributes if "Batting_" in att and "Inns" in att]
    sum_batting_innings = sum([row[att]
                              for att in bat_inns_attrs if row[att] > 0])

    bat_runs_attrs = [
        att for att in all_attributes if "Batting_" in att and "Runs" in att]
    sum_batting_runs = sum([row[att]
                           for att in bat_runs_attrs if row[att] > 0])

    bat_100s_attrs = [
        att for att in all_attributes if "Batting_" in att and "100s" in att]
    sum_batting_100s = sum([row[att]
                           for att in bat_100s_attrs if row[att] > 0])

    bat_50s_attrs = [
        att for att in all_attributes if "Batting_" in att and "50s" in att]
    sum_batting_50s = sum([row[att] for att in bat_50s_attrs if row[att] > 0])

    field_catch_attrs = [
        att for att in all_attributes if "Batting_" in att and "Ct" in att]
    sum_catches = sum([row[att] for att in field_catch_attrs if row[att] > 0])

    field_stump_attrs = [
        att for att in all_attributes if "Batting_" in att and "St" in att and att != 'Batting_Style_telugu']
    sum_stumpings = sum([row[att]
                        for att in field_stump_attrs if row[att] > 0])

    sum_dismissals = sum_catches + sum_stumpings

    bowl_mat_attrs = [
        att for att in all_attributes if "Bowling_" in att and "Mat" in att]
    sum_bowling_matches = sum([row[att]
                              for att in bowl_mat_attrs if row[att] > 0])

    bowl_inns_attrs = [
        att for att in all_attributes if "Bowling_" in att and "Inns" in att]
    sum_bowling_innings = sum([row[att]
                              for att in bowl_inns_attrs if row[att] > 0])

    bowl_balls_attrs = [
        att for att in all_attributes if "Bowling_" in att and "Balls" in att]
    sum_bowling_balls = sum([row[att]
                            for att in bowl_balls_attrs if row[att] > 0])

    bowl_wkt_attrs = [
        att for att in all_attributes if "Bowling_" in att and "Wkts" in att]
    sum_wickets = sum([row[att] for att in bowl_wkt_attrs if row[att] > 0])

    return sum_batting_matches, sum_batting_innings, sum_batting_runs, sum_batting_100s, sum_batting_50s, sum_dismissals, sum_catches, sum_stumpings, sum_bowling_matches, sum_bowling_innings, sum_bowling_balls, sum_wickets

# Get career start year of player
def get_start_year(span):
    if not is_valid_string(span) or span == None or pd.isnull(span):
        return -1
    try:
        break_up = span.split('-')
        return int(break_up[0])
    except:
        return -1

# Verify if the player has stopped playing cricket
def did_retire(span):
    if not is_valid_string(span) or span == None or pd.isnull(span):
        return False
    try:
        break_up = span.split('-')
        return int(break_up[1]) < 2021
    except:
        return False

# Converts an abbreviation filled with upper-case letters to corresponding readable telugu translation
def change_abbr(h):
    alpha = {
        "A": "ఏ",
        "B": "బీ",
        "C": "సీ",
        "D": "డీ",
        "E": "ఈ",
        "F": "ఎఫ్",
        "G": "జీ",
        "H": "హెచ్",
        "I": "ఐ",
        "J": "జే",
        "K": "కే",
        "L": "ఎల్",
        "M": "ఎం",
        "N": "ఎన్",
        "O": "ఓ",
        "P": "పీ",
        "Q": "క్యూ",
        "R": "ఆర్",
        "S": "ఎస్",
        "T": "టీ",
        "U": "యూ",
        "V": "వీ",
        "W": "డబల్యూ",
        "X": "ఎక్స్",
        "Y": "వై",
        "Z": "జెడ్"
    }
    return ''.join([alpha[i] + '.' for i in h])[:-1]

# Hardcoding few short-hand notations (abbreviations)
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

# Extracts required information from player's row for obtaining template string
def getData(row):
    batting_format_names, batting_stat_names, batting_details = get_batting_info(
        row)
    bowling_format_names, bowling_stat_names, bowling_details = get_bowling_info(
        row)
    fielding_format_names, fielding_stat_names, fielding_details = get_fielding_info(
        row)
    trophy_names, trophy_stat_names, trophy_details = get_trophy_info(row)
    sum_batting_matches, sum_batting_innings, sum_batting_runs, sum_batting_100s, sum_batting_50s, sum_dismissals, sum_catches, sum_stumpings, sum_bowling_matches, sum_bowling_innings, sum_bowling_balls, sum_wickets = get_description_sums(
        row)
    data = {
        # {%- macro early_career(player_name, career_start_year, first_class_debut, listA_debut, T20_debut, T20I_debut, ODI_debut, test_debut) -%}
        'player_name': row['Player_Name_Telugu'].strip(),
        'gender': row['Gender'],
        'career_start_year': get_start_year(row['career_span']),
        'first_class_debut': row['FC Matches_debut_Telugu'],
        'listA_debut': row['List A Matches_debut_Telugu'],
        'T20_debut': row['T20 Matches_debut_Telugu'],
        'T20I_debut': row['T20I Matches_debut_Telugu'],
        'ODI_debut': row['ODI Matches_debut_Telugu'],
        'test_debut': row['Test Matches_debut_Telugu'],

        # {%- macro career_intro(player_name, player_role, nationality, teams, jersey_number, has_retired) -%}
        'player_role': row['Playing Role_Telugu'],
        'nationality': row['Nationality_Telugu'],
        'teams': row['Teams_Telugu'],
        'jersey_number': row['Jersey_Number'],
        'has_retired': did_retire(row['career_span']),

        # {%- macro batting_description(player_name, sum_batting_matches, sum_batting_innings, sum_batting_runs, sum_batting_100s,
        #                sum_batting_50s, test_batting_average, test_batting_strike_rate, ODI_batting_average,
        #                ODI_batting_strike_rate, T20I_batting_average, T20I_batting_strike_rate) -%}

        'sum_batting_matches': sum_batting_matches,
        'sum_batting_innings': sum_batting_innings,
        'sum_batting_runs': sum_batting_runs,
        'sum_batting_100s': sum_batting_100s,
        'sum_batting_50s': sum_batting_50s,
        'test_batting_average': row['Batting_Test_Ave'],
        'test_batting_strike_rate': row['Batting_Test_SR'],
        'ODI_batting_average': row['Batting_ODI_Ave'],
        'ODI_batting_strike_rate': row['Batting_ODI_SR'],
        'T20I_batting_average': row['Batting_T20I_Ave'],
        'T20I_batting_strike_rate': row['Batting_T20I_SR'],

        # {%- macro fielding_description(sum_dismissals, sum_catches, sum_stumpings, is_wicketkeeper) -%}
        'sum_dismissals': sum_dismissals,
        'sum_catches': sum_catches,
        'sum_stumpings': sum_stumpings,

        # {%- macro bowling_description(player_name, sum_bowling_matches, sum_bowling_innings, sum_bowling_balls, sum_wickets, test_bowling_average,
        #                         test_bowling_economy, ODI_bowling_average, ODI_bowling_economy, T20I_bowling_average, T20I_bowling_economy,
        #                         bowling_10w_test, bowling_10w_FC) -%}

        'sum_bowling_matches': sum_bowling_matches,
        'sum_bowling_innings': sum_bowling_innings,
        'sum_bowling_balls': sum_bowling_balls,
        'sum_wickets': sum_wickets,
        'test_bowling_average': row['Bowling_Test_Ave'],
        'test_bowling_economy': row['Bowling_Test_Econ'],
        'ODI_bowling_average': row['Bowling_ODI_Ave'],
        'ODI_bowling_economy': row['Bowling_ODI_Econ'],
        'T20I_bowling_average': row['Bowling_T20I_Ave'],
        'T20I_bowling_economy': row['Bowling_T20I_Econ'],
        'bowling_10w_test': row['Bowling_Test_10w'],
        'bowling_10w_FC': row['Bowling_FC_10w'],

        # {%- macro trophy_description(player_name, major_trophy_and_championship_names) -%}
        'major_trophy_and_championship_names': row['trophy_names_Telugu'],

        # Batting table
        'batting_format_names': batting_format_names,
        'batting_stat_names': batting_stat_names,
        'batting_details': batting_details,

        # Bowling table
        'bowling_format_names': bowling_format_names,
        'bowling_stat_names': bowling_stat_names,
        'bowling_details': bowling_details,

        # Fielding table
        'fielding_format_names': fielding_format_names,
        'fielding_stat_names': fielding_stat_names,
        'fielding_details': fielding_details,

        # Trophy table
        'trophy_names': trophy_names,
        'trophy_stat_names': trophy_stat_names,
        'trophy_details': trophy_details,

        # References
        'all_ref': ast.literal_eval(row['References'])
    }
    # print(bowling_format_names)
    # print(bowling_stat_names)
    # print(bowling_details)
    return data

cricket_players_DF = pd.DataFrame()
with open('./data/final_cricket_players_translated_dataset_with_images.pkl', 'rb') as f:
    cricket_players_DF = pickle.load(f)
    cricket_players_DF.fillna(value="nan", inplace=True)
    all_attributes = cricket_players_DF.columns.tolist()

# Takes a player id as argument and returns corresponding template string associated with professional life of that player  
def main3(_id):
    global all_attributes
    file_loader = FileSystemLoader('./')
    env = Environment(loader=file_loader)
    template = env.get_template('./templates/life.j2')

    func_dict = {
        "stat_value": stat_value,
        "is_valid_string": is_valid_string,
        "shuffle_list": shuffle_list,
        "batting_description_func": batting_description_func,
        "bowling_description_func": bowling_description_func,
        "opening_sentence": opening_sentence,
        "batting_sent1": batting_sent1,
        "bowling_sent1": bowling_sent1,
        "bowling_sent2": bowling_sent2,
        "print_names": print_names,
        "get_translation": get_translation,
        "get_matches_ref": get_matches_ref,
        "get_stats_ref": get_stats_ref,
        "get_role": get_role,
        "get_trophy_name": get_trophy_name,
        "get_trophy_names_list": get_trophy_names_list
    }
    template.globals.update(func_dict)
    required_player = cricket_players_DF.loc[cricket_players_DF['Cricinfo_id'] == _id]
    for j, row in required_player.iterrows():
        return template.render(getData(row))