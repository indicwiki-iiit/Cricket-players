# Cricket-players

Cricket-players is one of the domains, which is a part of the IndicWiki Project.

## Description

The aim of this domain is to create a large number of articles (about 10,000) about notable cricket players across the world. This domain has potential because of the interest and passion for cricket and cricketers in our country, and Telugu-speaking states are no exception.
Hence, we are generating these data-rich articles in telugu for about 10,000 notable players, and uploading them to wikipedia, so that people who can read only in their native language (here, telugu) can benefit from this information.

## Installation

Create virtual environment in the project folder using the following commands.

```bash
$ pip install virtualenv
$ virtualenv -p python3.7 venv
```
After the successful creation of virtual environment (venv), clone the repository or download the zip folder of the project and extract it into the project folder.

Activate the virtual environment and headover to install the dependencies by following command.
```bash
$ pip install -r requirements.txt
```
requirements.txt comes along with the Project Directory. 

## Guide to generate XML dump, articles for different cricketers

- Clone the repository into the local system.
- For generating articles, one needs the folders: data, templates; and files: render.py, genXML.py. Ensure that these files and folders are available.
- In the file 'render.py', update the `ids` list such that it contains all the cricinfo IDs of the required players.

### Generating XML dump

- Follow the comments of 'render.py' and uncomment necessary lines to generate XML dump.
- Execute 'render.py' with the command: `python3.7 render.py`. This will generate the XML dump for given player ids list, and store them in the xml file 'cricket\_players.xml'.

### Generating individual articles and storing in a text file

- Follow the comments of 'render.py' and uncomment necessary lines to generate articles for different ids, in a txt file. Update the file name variable to 'cricket\_players.txt'.
- Execute 'render.py' with the command: `python3.7 render.py`. This will generate the required articles for given player ids list, and store them in a txt file 'cricket\_players.txt'. Each player's article has the corresponding player's cricinfo id at the beginning, and each such articles are distinguished by dotted lines (at the beginning and end of article) in the txt file.


## Github Structure

### data

> Github folder Link: https://github.com/indicwiki-iiit/Cricket-players/tree/main/data
- This folder contains the penultimate and final versions of our datasets, along with implementation for data cleaning and sweetviz report for analyzing the dataset.
    - _final\_cricket\_players\_translated\_dataset\_with\_images.csv_ -> This is the csv format of the final version of the dataset obtained after merging, cleaning and translation/transliteration.
    - _final\_cricket\_players\_translated\_dataset\_with\_images.pkl_ -> This is the pickle file of the final version of the dataset obtained after merging, cleaning and translation/transliteration.
    - _final\_cricket\_players\_translated\_dataset\_with\_images.xlsx_ -> This is the xlsx format of the final version of the dataset obtained after merging, cleaning and translation/transliteration.
    - _SWEETVIZ\_REPORT.html_ -> This is a brief report of the dataset, generated using sweetviz library, for better analysis of data.

#### data\_cleaning

> Github folder Link: https://github.com/indicwiki-iiit/Cricket-players/tree/main/data/data_cleaning
- This folder contains the complete implementation for data cleaning.
    - _initial\_cleaning.py_ -> This file contains implementation which performs an initial level data cleaning based on defects observed in sweetviz report.
    - _symbol\_replacement.py_ -> This file contains implementation which performs a secondary level data cleaning based on defects observed on dataset obtained after initial cleaning.
    - _final\_cleaning.py_ -> This file contains implementation which performs a final level data cleaning based on defects observed on dataset obtained after secondary level cleaning.

### templates

> Github folder Link: https://github.com/indicwiki-iiit/Cricket-players/tree/main/templates
- This folder contains the implementations of templates required for rendering articles.
    - _categories.j2_ -> This file contains the jinja2 template corresponding to categories of a cricket player in the article.
    - _info.j2_ -> This file contains the jinja2 template corresponding to infobox and overview of a cricket player in the article.
    - _life.j2_ -> This file contains the jinja2 template corresponding to professional life section of a cricket player in the article.
    - _personal\_life.j2_ -> This file contains the jinja2 template corresponding to personal life section of a cricket player in the article.
    - _player\_statistical\_analysis.j2_ -> This file contains the jinja2 template corresponding to statistical analysis sub-section of a cricket player in the article.
    - _records.j2_ -> This file contains the jinja2 template corresponding to records, awards and references of a cricket player in the article.
    - _render\_categories.py_ -> This file contains implementation which displays relevant categories for a given player based on his/her information.
    - _render\_info.py_ -> This file contains implementation which displays infobox and overview for a given player based on his/her information.
    - _render\_life.py_ -> This file contains implementation which displays relevant professional life details for a given player based on his/her information.
    - _render\_personal\_life\_and\_statistics.py_ -> This file contains implementation which displays personal life and statistical analysis for a given player based on his/her information.
    - _render\_records.py_ -> This file contains implementation which displays relevant records, awards and references for a given player based on his/her information.

### images

> Github folder Link: https://github.com/indicwiki-iiit/Cricket-players/tree/main/images
- This folder contains the implementation for scraping images from wikidata and english wikipedia articles, and the dataset obtained on doing so.
    - _collect\_image\_links.py_ -> This file contains implementation for extracting image links of players with a valid english wikipedia article.
    - _get\_images.py_ -> This file contains implementation for extracting english wikipedia article url for different players having a valid wikidata id.
    - _cricket\_player\_images.csv_ -> This file contains the dataset which contains information related to wikipedia article url, wikipedia article infobox image link, wikidata id etc. for each player (key information which was exploited for extracting images).

### records

> Github folder Link: https://github.com/indicwiki-iiit/Cricket-players/tree/main/records
- This folder contains the implementation for translation of all records attributes (for which online libraries didn't work).
    - _records\_processing.py_ -> This file contains the script for identifying the count and type of unique sentence structures in records attribute of dataset.
    - _fix\_records.py_ -> This file contains the script for translating records attribute of dataset.
    - _Part-1\_records\_translation.xlsx_ -> This file contains the first split of dataset comprising of unique sentence structures for records, and their corresponding translation (done manually).
    - _Part-2\_records\_translation.xlsx_ -> This file contains the second split of dataset comprising of unique sentence structures for records, and their corresponding translation (done manually).
    - _Part-3\_records\_translation.xlsx_ -> This file contains the third split of dataset comprising of unique sentence structures for records, and their corresponding translation (done manually).

### scraping

> Github folder Link: https://github.com/indicwiki-iiit/Cricket-players/tree/main/scraping
- This folder contains the implementation of data scraping for obtaining dataset.
    - _scrape.ipynb_ -> This file contains the script for scraping notable players' data from cricinfo official site.
    - _Stats\_JSON\_Data Scraper.ipynb_ -> This file contains script for scraping additional stat details from cricinfo official site, in json format (for notable players).

### translating\_data

> Github folder Link: https://github.com/indicwiki-iiit/Cricket-players/tree/main/translating_data
- This folder contains the implementation for obtaining and storing a translated (and transliterated) dataset, to save overhead of translation libraries while generating articles via XML file. It also contains the intermediate datasets obtained in the process.
    - _awards.csv_ -> This file contains dataset corresponding to translated values for awards attribute.
    - _cricket\_players\_records.xlsx_ -> This file contains dataset corresponding to translated values for records attributes (with excel translation - which didn't produce desirable output).
    - _handle\_debuts.py_ -> This file contains implementation which rectifies mistakes in existing debut strings translation, and handles abbreviations in those sentences.
    - _info\_overview.py_ -> This file contains implementation for obtaining telugu contents for all attributes associated with infobox and overview of a player's article.
    - _modified\_info\_overview.csv_ -> This file contains dataset corresponding to translated values for attributes of infobox and overview.
    - _Personal\_life\_stats\_translated.csv_ -> This file contains dataset corresponding to translated values for attributes of personal life section and statistical analysis sub-section.
    - _professional\_life\_trans.csv_ -> This file contains dataset corresponding to translated values for attributes of professional life section.
    - _professional\_life.py_ -> This file contains implementation for obtaining telugu contents for all attributes associated with professional life of a player.

### Report

You can find the detailed report [here](https://github.com/indicwiki-iiit/Cricket-players/blob/main/Cricket_Players_Domain-Interns_report.pdf)

### Sample Article

You can find the sample article [here](https://github.com/indicwiki-iiit/Cricket-players/blob/main/Cricket%20Players%20-%20Sample%20Article.pdf)

### cricket\_players.xml

> Github file Link: https://github.com/indicwiki-iiit/Cricket-players/tree/main/cricket_players.xml
- This file contains the XML dump which consists of articles of all the 10k players, whose data has been collected.

### duplicates\_to\_consider.json

> Github file Link: https://github.com/indicwiki-iiit/Cricket-players/tree/main/duplicates_to_consider.json
- This file contains a dictionary regarding which players are to be considered when duplicate names are encountered.

### genXML.py

> Github file Link: https://github.com/indicwiki-iiit/Cricket-players/tree/main/genXML.py
- This file contains the code for generating an XML file which has the data for rendering an article.

### render.py

> Github file Link: https://github.com/indicwiki-iiit/Cricket-players/tree/main/render.py
- This is the code used for rendering the cricket player articles using jinja2 templates from templates folder.

### requirements.txt:

> Github file Link: https://github.com/indicwiki-iiit/Cricket-players/tree/main/requirements.txt
- This contains all the packages and libraries that are necessary for building this project.




