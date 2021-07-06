import pickle
from jinja2 import Environment, FileSystemLoader
from google.transliteration import transliterate_text
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
import json
import pandas as pd

from genXML import tewiki, writePage

import ast

def getData(row):
	# Translation and Transliteration
	player_name = row.Player_Name_Telugu.values[0]
	all_records = row.records_telugu.values[0]
	test_records = row.test_records_telugu.values[0]
	odi_records = row.odi_records_telugu.values[0]
	t20i_records = row.t20i_records_telugu.values[0]
	gender = row.Gender.values[0]
	references = ast.literal_eval(row.References.values[0])
	awards = str(row.awards_telugu.values[0])


	if(all_records !='[]'):
		try:
			all_records = ast.literal_eval(all_records)
		except:
			all_records = ast.literal_eval(row.records.values[0])

	
	if(test_records != '[]'):
		try:
			test_records = ast.literal_eval(test_records)
		except:
			test_records = ast.literal_eval(row.test_records.values[0])

	
	if(odi_records != '[]'):
		try:
			odi_records = ast.literal_eval(odi_records)
		except:
			odi_records = ast.literal_eval(row.odi_records.values[0])

	
	if(t20i_records != '[]'):
		try:
			t20i_records = ast.literal_eval(t20i_records)
		except:
			t20i_records = ast.literal_eval(row.t20i_records.values[0])

	if(awards != 'nan'):
		try:
			awards = awards.split(',, ')
		except:
			awards = ast.literal_eval(row.AWARDS.values[0])


	# Data dictionary 
	data = {
		
		'player_name':player_name,
		'all_records': all_records, 
		'test_records': test_records, 
		'odi_records': odi_records,
		't20i_records': t20i_records,
		'gender': gender,
		'awards': awards,
		'references': references
	  }

	return data



def getData2(row):
	data = {
		
		'player_name':row.Player_Name_Telugu.values[0],
		'all_records': ast.literal_eval(row.records.values[0]), 
		'test_records': ast.literal_eval(row.test_records.values[0]), 
		'odi_records': ast.literal_eval(row.odi_records.values[0]),
		't20i_records': ast.literal_eval(row.t20i_records.values[0]),
		'gender': row.Gender.values[0],
		'references': ast.literal_eval(row.References.values[0])
	  }

	return data



def get_matches_ref(matches_ref, player_name):
	required_ref = [r for r in matches_ref if "records" in r]
	if len(required_ref) == 0:
		return ''
	return "<ref>[" + required_ref[0] + " " + player_name + " రికార్డులు]</ref>"


cricketDF = pd.DataFrame()
with open('../data_collection/data/final_cricket_players_translated_dataset_with_images.pkl', 'rb') as f:
    cricketDF = pickle.load(f)
    cricketDF.fillna(value="nan", inplace=True)

def main5(_id):
	file_loader = FileSystemLoader('./')
	env = Environment(loader=file_loader)
	template = env.get_template('records.j2')

	func_dict = {
		"get_matches_ref": get_matches_ref
	}
	template.globals.update(func_dict)
	
	cricketDF.rename(columns={'Records' : 'records'}, inplace=True)
	cricketDF.rename(columns={'Test Records' : 'test_records'}, inplace=True)
	cricketDF.rename(columns={'ODI Records' : 'odi_records'}, inplace=True)
	cricketDF.rename(columns={'T20I Records' : 't20i_records'}, inplace=True)
	row = cricketDF.loc[cricketDF['Cricinfo_id'] == _id]
	return template.render(getData(row))




