import pickle
import pandas
from genXML import tewiki, writePage
from render_info import main1
from render_personal_life_and_statistics import main2, main4
from render_life import main3
from render_records import main5
from render_categories import main6

with open('../data_collection/data/final_cricket_players_translated_dataset_with_images.pkl', 'rb') as f:    
    cricket_players_DF = pickle.load(f)
    # ids = cricket_players_DF.Cricinfo_id.tolist()
    # ids for 20 cricketers chosen
    ids = [52910, 10696, 47478, 52672, 665053, 5692, 44024, 51487, 318845, 53116, 5390, 277906, 267192, 54545, 55150, 769517, 53448, 215501, 275487, 54273]
    # ids = [28081]
    # change below file_name to cricket_players.txt to store rendered output in txt file like previously done
    file_name = 'cricket_players_(20).xml'
    with open(file_name, 'w') as fobj:
        # for xml file, uncomment below line
        fobj.write(tewiki + '\n')
        for i, _id in enumerate(ids):
            if i % 100 == 0:
                print(f'{i} players done')
            s = '\n\n'
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
            
            # uncomment below code (if commented) for storing in a txt file, where each article is separated by 160 hyphens and has player id on top for each article
            # fobj.write('-'*160)
            # fobj.write(s)
            # fobj.write(str(_id))
            # fobj.write(s)
            # fobj.write(template_string)
            # fobj.write(s)
            # fobj.write('-'*160)
            # fobj.write(s) 
            
            # uncomment below code (if commented) for generating xml file
            row = cricket_players_DF.loc[cricket_players_DF['Cricinfo_id']==_id]
            writePage(row.Player_Name.values[0], template_string, fobj)
        fobj.write('</mediawiki>')
        
