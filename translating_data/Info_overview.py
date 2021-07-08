'''this info_overview.py file gets the telugu translations of
attributes in InfoBox and overview section of cricket players domain'''

# Importing all necessary libraries
import pandas as pd
import pickle
import translators as ts
from deeptranslit import DeepTranslit
from deep_translator import GoogleTranslator
from google_trans_new import google_translator
from google.transliteration import transliterate_word, transliterate_text
import ast

req_str = "Cricinfo_id, Full Name, Full_Name_Telugu, Teams, teams_ov_telugu, Birth_Place, Birth_Place_telugu, Died, Died_telugu, Age, Age_telugu, Height, height_telugu, Batting Style, Batting_Style_telugu, Bowling Style, Bowling_Style_telugu, T20I Matches_debut, T20I_info_Matches_debut_Telugu, ODI Matches_debut, ODI_info_Matches_debut_Telugu, Test Matches_debut, Test_info_Matches_debut_Telugu, Test Matches_last_appearance, Test_info_Matches_last_appearance_telugu, ODI Matches_last_appearance, ODI_info_Matches_last_appearance_telugu, T20I Matches_last_appearance, T20I_info_Matches_last_appearance, AWARDS, awards_telugu"
cols = req_str.split(', ')
print(cols)
translator = google_translator()
trans = DeepTranslit('telugu').transliterate
all_attributes = []


# This function checks whether the given input is a valid one(Not nan)
def is_valid_string(attribute_value):
    if not isinstance(attribute_value, str):
        return True
    return not (attribute_value == None or pd.isnull(attribute_value) or str(attribute_value) == "" or str(attribute_value) == "nan")


# This function Transliterates the given input by using deep translit and other transliteration libraries.
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
            return transliterate_text(test_text, lang_code='te')
        except:
            pass
    return description

# This function translates the given input by using Google trans new and other translation libraries.
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

# Gets interlinks for Birthplace of the player
def interLinks_for_place(birth_place,countries):
    if not is_valid_string(birth_place):
        return ''
    date = []
    place = []
    birth_place = ast.literal_eval(birth_place)
    for i in birth_place:
        date.append(i.strip())
    for i in date:
        if i in countries:
            date.remove(i)
    for i in date:
        place.append(getTranslatedDescription(i))
    if len(place) == 0:
        return "nan"
    elif len(place) == 1:
        # date = getTranslatedDescription(date)
        # date = ast.literal_eval(date)
        return "[["+place[0]+"]]"
    else:
        # date = getTranslatedDescription(date)
        # date = ast.literal_eval(date)
        li = ']],[['.join(place)
        return "[["+li+"]]"

# Gives Transliterated death place and death date of the player(including age)
def translate_death(row):
    if not is_valid_string(row):
        return ''
    if ', (' in row:
        deadth = row.split(", (")
        if 'aged' in deadth[1]:
            deadth[1] = deadth[1].replace('aged','(వయస్సు :')
            if (deadth[1].find('y') != -1 and deadth[1].find('d') != -1):
                deadth[1] = deadth[1].replace('y'," సంవత్సరాల")
                deadth[1] = deadth[1].replace('d'," రోజులు")
            elif (deadth[1].find('y') != -1):
                deadth[1] = deadth[1].replace('y'," సంవత్సరాలు")
            deadth[0] = getTransliteratedDescription(deadth[0]).strip()
        return ''.join(deadth)
    elif ' (' in row:
        deadth = row.split(" (")
        if 'aged' in deadth[1]:
            deadth[1] = deadth[1].replace('aged','(వయస్సు :')
            if (deadth[1].find('y') != -1 and deadth[1].find('d') != -1):
                deadth[1] = deadth[1].replace('y'," సంవత్సరాల")
                deadth[1] = deadth[1].replace('d'," రోజులు")
            elif (deadth[1].find('y') != -1):
                deadth[1] = deadth[1].replace('y'," సంవత్సరాలు")
            deadth[0] = getTransliteratedDescription(deadth[0]).strip()
        return ''.join(deadth)
    elif '(aged null)' in row:
        deadth = row.replace("(aged null)","")
        return getTransliteratedDescription(deadth)
    else:
        return getTransliteratedDescription(row)

# Results Translated age of the player
def Age_translation(age):
    if not is_valid_string(age):
        return ''
    if (age.find('y') != -1 and age.find('d') != -1):
        age = age.replace('y'," సంవత్సరాల")
        age = age.replace('d'," రోజులు")
    elif (age.find('y') != -1):
        age = age.replace('y'," సంవత్సరాలు")
    return age

'''This functions results Home teams of the player(max 6) by considering the nationality of the player
If the home teams are less than 6 it results the other teams(max 6 only)'''
def teams6(tea,Nationality):
    Iteam = []
    NonIteam = []
    li = []
    for i in tea:
        if Nationality in i:
            Iteam.append(i)
        else:
            NonIteam.append(i)
    if len(Iteam) < 7:
        li = Iteam + NonIteam
    else:
        li = Iteam[:6]
    if len(li) < 7:
        return li
    else:
        return li[:6]

# Takes a list of team names as input, results the transliterated output of the input
def get_teams_string(teams_list,Nationality):
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
# Takes a list of Awards of the player as input, results the transliterated output of the input
def get_awards(teams_list):
    if not is_valid_string(teams_list):
        return ''
    actual_list = ast.literal_eval(teams_list)
    capitals = {
        'OBE':'ఓ.బీ.ఇ.','july':"జూలై", 'Year':'ఇయర్','year':'ఇయర్','on':'ఆన్','Dec':'డిసెంబర్', 'the':'ది','The':"ది", 'MBE':'ఎం.బీ.ఇ.', 'SASSSA':'ఎస్.ఏ.ఎస్.ఎస్.ఎస్.ఏ.', 
	'SHIELD':'ఎస్.హెచ్.ఐ.ఇ.ఎల్.డి.', 'ECB':'ఇ.సీ.బీ.', 'SACOS':'ఎస్.ఏ.సీ.ఓ.ఎస్.', 'N.C.C':'ఎన్.సీ.సీ.', 
	'MdeS':'ఎం.డి.ఇ.ఎస్.', 'NtlB':'ఎన్.టి.ఎల్.బీ.', '(ICC':'(ఐ.సీ.సీ.', 'ICC':'ఐ.సీ.సీ.', 'HS':'హెచ్.ఎస్.', 
	'(ET':'(ఇ.టి.', 'SA':'ఎస్.ఏ.', 'BHS':'బీ.హెచ్.ఎస్.', 'UNISA':'యూ.ఎన్.ఐ.ఎస్.ఏ.', 'HH':'హెచ్.హెచ్.', 
	'UOFS':'యూ.ఓ.ఎఫ్.ఎస్.', 'u-19s':'అండర్ -19స్', 'LG':'ఎల్.జీ.', 'WP':'డబల్యూ.పి.', 'MR':'ఎం.ఆర్.', 
	'R':'ఆర్.', 'AM':'ఏ.ఎం.', 'UAE':'యూ.ఏ.ఇ.', 'FC':'ఎఫ్.సీ.', 'CWS':'సీ.డబల్యూ.ఎస్.', 'B':'బీ.', 
	'RAU':'ఆర్.ఏ.యూ.', 'CBC':'సీ.బీ.సీ.', '(HS':'(హెచ్.ఎస్.', 'XI':'XI', 'SACD':'ఎస్.ఏ.సీ.డి.', 'EG':'ఇ.జీ.', 
	'(EP/WP/Bdr/Ess/WAus/SA':'(ఇ.పి./డబల్యూ.పి./బీ.డి.ఆర్./ఇ.ఎస్.ఎస్./డబల్యూ.ఏ.యూ.ఎస్./ఎస్.ఏ.', 
	'WPB':'డబల్యూ.పి.బీ.', 'UWC':'యూ.డబల్యూ.సీ.', 'Tvl':'టి.వీ.ఎల్.', 'UPE':'యూ.పి.ఇ.', 'ET':'ఇ.టి.', 
	'CBE':'సీ.బీ.ఇ.', '(GW':'(జీ.డబల్యూ.', 'SHEFFIELD':'ఎస్.హెచ్.ఇ.ఎఫ్.ఎఫ్.ఐ.ఇ.ఎల్.డి.', 'SACS':'ఎస్.ఏ.సీ.ఎస్.', 
	'(FA':'(ఎఫ్.ఏ.', 'SASA':'ఎస్.ఏ.ఎస్.ఏ.', 'FA':'ఎఫ్.ఏ.', ' v ':' వర్సెస్ ', 'Under-19s':'అండర్ -19స్', 
	'Under':'అండర్', 'EL':'ఇ.ఎల్.', 'BBC':'బీ.బీ.సీ.', 'FR':'', 'GO':'ఎఫ్.ఆర్.', 'MTN':'ఎం.టి.ఎన్.', 'PCA':'పి.సీ.ఏ.', 
	'S.F.':'ఎస్.ఎఫ్.', 'PE':'పి.ఇ.', 'SAARC':'ఎస్.ఏ.ఏ.ఆర్.సీ.', 'GW':'జీ.డబల్యూ.', 'OFS':'ఓ.ఎఫ్.ఎస్.', 'ODI':'ఓ.డి.ఐ.', 
	'Surrey':'సర్రే', 'Under-17s':'అండర్ -17స్', 'Derbyshire':'డెర్బీషైర్', 'A':'ఏ.', 'KS':'కె.ఎస్.', 'S':'ఎస్.', 
	'Lancashire':'లాంక్షైర్', 'Leicestershire':'లీసెస్టర్షైర్', 'NT':'ఎన్.టి.', 'SRdeS':'ఎస్.ఆర్.డి.ఇ.ఎస్.', 
	'T20I':'టి20ఐ', 'GRADE':'జీ.ఆర్.ఏ.డి.ఇ.', 'NBC':'ఎన్.బీ.సీ.', 'I':'ఐ.', 'EP':'ఇ.పి.', 'CC':'సీ.సీ.', 'DR':'డి.ఆర్.', 'St':'సెయింట్' 
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
            ',, '.join(actual_list))      
        return translated_output
    except Exception as e:
        print("Level 2", e)
        try:
            translated_output = getTranslatedDescription(actual_list)
            if ']]' in translated_output:
                translated_output = translated_output.replace(']]', ']')
            actual_list = list(ast.literal_eval(translated_output))
            return ',, '.join(actual_list)
        except Exception as f:
            print("Level 3", f)
            try:
                translated_output = getTranslatedDescription(
                    ',, '.join(actual_list))
                return translated_output
            except Exception as g:
                print("Final level", g)
                return ',, '.join(actual_list)

# Results the translated Height of the player
def translate_height(height):
    if not is_valid_string(height):
        return ''
    if (height.find('ft') != -1 and height.find('in') != -1):
        height = height.replace('ft',"")
        height = height.replace('in',"")
        height = height.split(' ')
    elif(height.find('ft') != -1):
        height = height.replace('ft',"")
        height = list(height)
        
    
    return height

# Function takes a debut or last appearance match of the player as input string, Results date, year, opponent team of the match

def spliting(row):
    if not is_valid_string(row):
        return ''
    li =[]
    final = []
    date = row.split(",")
    li.append(date[-1])
    year = date[0].split("at")
    li.append(year[-1])
    against = year[0].split("vs")
    li.append(against[-1])
    for i in li:
        final.append(getTranslatedDescription(i.strip()))
    return final

# Calls the above funtions as per the attribute.
def get_db_val(row, attribute_name):
    countries = ['Japan', 'Namibia', 'Argentina', 'Singapore', 'Austria', 'U.A.E.', 'Belgium', 'Scotland', 'Italy', 'Zimbabwe', 'South Africa', 'Germany', 'E&C Africa', 'Malaysia', 
    'Sri Lanka', 'Oman', 'Australia', 'Bangladesh', 'Uganda', 'Chile', 'West Indies', 'India', 'Hong Kong', 'Denmark', 'P.N.G.', 'Nepal', 'Pakistan', 'Fiji', 'Cayman Is', 
    'England', 'Kenya', 'U.S.A.', 'Bermuda', 'Kuwait', 'Netherlands', 'New Zealand', 'Malta', 'Canada', 'Afghanistan', 'Ireland', 'Gibraltar']
    if attribute_name == "Full_Name_Telugu":
        return getTransliteratedDescription(row['Full Name'])
    if attribute_name == "Birth_Place_telugu":
        return interLinks_for_place(row["Birth_Place"],countries)
    if attribute_name == "Died_telugu":
        return translate_death(row["Died"])
    if attribute_name == "height_telugu":
        return translate_height(row['Height'])
    if attribute_name == "Age_telugu":
        return Age_translation(row["Age"])
    if attribute_name == "Batting_Style_telugu":
        return getTransliteratedDescription(row["Batting Style"])
    if attribute_name == "Bowling_Style_telugu":
        return getTransliteratedDescription(row['Bowling Style'])
    if attribute_name == "awards_telugu":
        return get_awards(row["AWARDS"])
    if attribute_name == "teams_ov_telugu":
        return get_teams_string(row["Teams"],row["Nationality"])
    if attribute_name == "T20I_info_Matches_debut_Telugu":
        return spliting(row['T20I Matches_debut'])
    if attribute_name == "ODI_info_Matches_debut_Telugu":
        return spliting(row["ODI Matches_debut"])
    if attribute_name == "Test_info_Matches_debut_Telugu":
        return spliting(row["Test Matches_debut"])
    if attribute_name == "Test_info_Matches_last_appearance_telugu":
        return spliting(row['Test Matches_last_appearance'])
    if attribute_name == "ODI_info_Matches_last_appearance_telugu":
        return spliting(row["ODI Matches_last_appearance"])
    if attribute_name == "T20I_info_Matches_last_appearance":
        return spliting(row["T20I Matches_last_appearance"])
    

with open('final_cricket_players_DF.pkl', 'rb') as f:
    cricket_players_DF = pickle.load(f)
    all_attributes = cricket_players_DF.columns.tolist()
    cricket_players_DF.fillna(value="nan", inplace=True)
    ids = cricket_players_DF.Cricinfo_id.tolist()
    ids = ids[:500]
    final_data = []
    for i, cricketer_id in enumerate(ids):
        required_player = cricket_players_DF.loc[cricket_players_DF['Cricinfo_id'] == cricketer_id]
        if i % 10 == 0:
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
    # a = a.drop_duplicates()
    # a = a.drop_duplicates('Cricinfo_id')
    a.drop(a.columns[a.columns.str.contains(
        'unnamed', case=False)], axis=1, inplace=True)
    a.to_csv('info1-500.csv', index=False)