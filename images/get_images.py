import pandas as pd
import sweetviz as sv
import json
import ast
import pickle
import wikipedia
        
a = pd.read_csv('All_players_images.csv', low_memory=False)

def get_wikipedia_url_from_wikidata_id(wikidata_id, lang='en', debug=False):
    import requests
    from requests import utils

    url = (
        'https://www.wikidata.org/w/api.php'
        '?action=wbgetentities'
        '&props=sitelinks/urls'
        f'&ids={wikidata_id}'
        '&format=json')
    json_response = requests.get(url).json()
    if debug: print(wikidata_id, url, json_response) 

    entities = json_response.get('entities')    
    if entities:
        entity = entities.get(wikidata_id)
        if entity:
            sitelinks = entity.get('sitelinks')
            if sitelinks:
                if lang:
                    # filter only the specified language
                    sitelink = sitelinks.get(f'{lang}wiki')
                    if sitelink:
                        wiki_url = sitelink.get('url')
                        if wiki_url:
                            return requests.utils.unquote(wiki_url)
                else:
                    # return all of the urls
                    wiki_urls = {}
                    for key, sitelink in sitelinks.items():
                        wiki_url = sitelink.get('url')
                        if wiki_url:
                            wiki_urls[key] = requests.utils.unquote(wiki_url)
                    return wiki_urls
    return None

ids = a.cricinfoIdLabel.tolist()
wiki_links = []

for i, cricketer_id in enumerate(ids):
    required_player = a.loc[a['cricinfoIdLabel'] == cricketer_id]
    if i % 100 == 0:
        print(f'{i} players done')
    for j, row in required_player.iterrows():
        try:
            # wiki_links.append(wikipedia.page(row['personLabel']).url)
            wiki_links.append(get_wikipedia_url_from_wikidata_id(row['person'].split('/')[-1]))
        except Exception as e:
            print(e)

a['Wikipedia_page_links'] = wiki_links
a = a.drop_duplicates()
a = a.drop_duplicates('cricinfoIdLabel')
a.drop(a.columns[a.columns.str.contains(
    'unnamed', case=False)], axis=1, inplace=True)
a.to_csv('All_players_images.csv', index=False)
