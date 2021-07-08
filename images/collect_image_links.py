# Extracting image links for players with a valid english wikipedia article

import csv
import pandas as pd
from bs4 import BeautifulSoup as bf
import requests

# Extract image link from infobox given a player's english wikipedia article's url
def get_image_link(page_url):
    if page_url == None or page_url == "nan":
        return ""
    request = requests.get(page_url)
    soup = bf(request.text,"html.parser")
    if soup == None:
        return ""
    a = soup.find("td", class_="infobox-image")
    if a == None:
        return ""
    b = a.find("a")
    if b == None:
        return ""
    if b.has_attr("href"):
        return b["href"]
    return ""

a = pd.read_csv('All_players_images.csv', low_memory=False)
image_links = []
ids = a.cricinfoIdLabel.tolist()

# Obtain image link for each player based on cricinfo_id
for i, cricketer_id in enumerate(ids):
    required_player = a.loc[a['cricinfoIdLabel'] == cricketer_id]
    if i % 100 == 0:
        print(f'{i} players done')
    for j, row in required_player.iterrows():
        try:
            image_links.append(get_image_link(row['Wikipedia_page_links']))
        except Exception as e:
            print(e)
            image_links.append("")

a['Wikipedia_image_link'] = image_links
a = a.drop_duplicates()
a = a.drop_duplicates('cricinfoIdLabel')
a.drop(a.columns[a.columns.str.contains(
    'unnamed', case=False)], axis=1, inplace=True)
a.to_csv('cricket_player_images.csv', index=False)
