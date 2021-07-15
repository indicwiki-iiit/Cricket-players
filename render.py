# Generates XML dump for required articles (based on cricket player ids provided as parameters)
import pickle
import json
import pandas
from genXML import tewiki, writePage
import sys
sys.path.append('./templates')
from render_info import main1
from render_personal_life_and_statistics import main2, main4
from render_life import main3
from render_records import main5
from render_categories import main6

# Handling edge cases of duplicate titles in XML dump
duplicates_to_consider = {}
with open('duplicates_to_consider.json', 'r') as f:
    duplicates_to_consider = json.load(f)

with open('./data/final_cricket_players_translated_dataset_with_images.pkl', 'rb') as f:    
    cricket_players_DF = pickle.load(f)
    # Complete list of cricinfo-ids of required cricket player articles (update here based on necessity)
    all_ids = cricket_players_DF.Cricinfo_id.tolist()
    # Split of above list of all ids for obeying constraints of xml file size (update here based on necessity)
    split_ids = [all_ids[:5000], all_ids[5000:]]
    # Xml file names for each corresponding split mentioned above - should have same number of elements as split_ids array (update here based on necessity)
    file_names = [f'cricket_players(part-{i}).xml' for i in range(1, 3)]
    current_page_id = 900000
    for k in range(len(file_names)):
        file_name = file_names[k]
        ids = split_ids[k]
        with open(file_name, 'w') as fobj:
            fobj.write(tewiki + '\n')
            for i, _id in enumerate(ids):
                if i % 100 == 0:
                    print(f'Part-{k+1}: {i} players done')
                s = '\n\n'
                row = cricket_players_DF.loc[cricket_players_DF['Cricinfo_id']==_id]
                player_full_name = row['Full Name'].values[0]
                if player_full_name in duplicates_to_consider.keys() and int(_id) != int(duplicates_to_consider[player_full_name]):
                    continue
                player_infobox_and_overview = main1(_id)
                player_infobox_and_overview = player_infobox_and_overview.rstrip().lstrip()
                player_personal_life = main2(_id)
                player_personal_life = player_personal_life.rstrip().lstrip()
                player_professional_life = main3(_id)
                player_professional_life = player_professional_life.rstrip().lstrip()
                player_statistics = main4(_id)
                player_statistics = player_statistics.rstrip().lstrip()
                player_records_awards_references = main5(_id)
                player_records_awards_references = player_records_awards_references.rstrip().lstrip()
                player_categories = main6(_id)
                player_categories = player_categories.rstrip().lstrip()
                template_string = player_infobox_and_overview + s + player_personal_life + s + player_professional_life + s + player_statistics + s + player_records_awards_references + s + player_categories + s        
                writePage(current_page_id, row.Full_Name_Telugu.values[0], template_string, fobj)
                current_page_id += 1
            fobj.write('</mediawiki>')
        
