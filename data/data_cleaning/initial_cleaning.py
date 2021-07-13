# Performs an initial level data cleaning based on defects observed in sweetviz report

import pandas as pd
import sweetviz as sv

# Rectifying Best Bowling Innings, Best Bowling Matches figures which were misinterpreted (21/3 was considered as 21st March) 
def clean_BBI_and_BBM(a):
    date_issue_atts = ['Bowling_FC_BBI', 'Bowling_List A_BBI', 'Bowling_Test_BBI', 'Bowling_T20_BBI', 'Bowling_ODI_BBI', 'Bowling_T20I_BBI', 
                    'Bowling_FC_BBM', 'Bowling_List A_BBM', 'Bowling_Test_BBM', 'Bowling_T20_BBM', 'Bowling_ODI_BBM', 'Bowling_T20I_BBM']
    month_to_num = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }
    for attribute in date_issue_atts:
        for i, row in a.iterrows():
            if pd.isnull(a.at[i, attribute]):
                continue
            elif row[attribute] == '-':
                continue
            elif '/' in row[attribute]:
                continue
            split_val = row[attribute].split('-')
            for j in range(len(split_val)):
                ind_val = split_val[j]
                try:
                    split_val[j] = str(int(ind_val))
                except:
                    split_val[j] = str(month_to_num[ind_val])
            a.at[i, attribute] = '/'.join(split_val)


# Converting numerical values to integers (wherever necessary) for further processing during rendering 
def remove_floats_from_required_attributes(a, attributes):
    for attribute in attributes:
        for i, row in a.iterrows():
            if pd.isnull(a.at[i, attribute]):
                continue
            elif row[attribute] == '-':
                continue
            try:
                a.at[i, attribute] = str(int(float(row[attribute])))
            except:
                a.at[i, attribute] = '-'

# cleaning up corner cases in batting style, playing role attributes where unwanted values were found
def edge_case_of_batting_style_and_role(a, attributes):
    for attribute in attributes:
        for i, row in a.iterrows():
            if attribute == "Batting Style" and row[attribute] == "Right hand bat, Right hand bat":
                a.at[i, attribute] = "Right hand bat"
            elif attribute == "Playing Role" and row[attribute] == "Batter, Batter":
                a.at[i, attribute] = "Batter"

# cleaning up empty entries in awards attribute
def clean_up_awards(a):
    for i, row in a.iterrows():
        try:
            if (len(row["AWARDS"]) is 0) or (len(row["AWARDS"]) == 1 and (len(row["AWARDS"][0]) == 0 or row["AWARDS"][0] == ':')):
                a.at[i, "AWARDS"] = pd.NA
        except:
            a.at[i, "AWARDS"] = pd.NA
            
# cleaning up empty entries in records attribute
def clean_up_records(a):
    attributes = ["Records", "Test Records", "ODI Records", "T20I Records"]
    for attribute in attributes:
        for i, row in a.iterrows():
            try:
                if len(row[attribute]) is 0:
                    a.at[i, attribute] = pd.NA
            except:
                a.at[i, attribute] = pd.NA

# cleaning up empty entries in major trophies attribute                
def clean_up_major_trophies(a):
    for i, row in a.iterrows():
        try:
            if len(row["Major trophies"]) == 0:
                a.at[i, "Major trophies"] = pd.NA
        except:
            a.at[i, "Major trophies"] = pd.NA          

a = pd.read_csv("final_cricket_players.csv", low_memory=False)
all_attributes = a.columns.tolist()
batting_attributes = [attr for attr in all_attributes if attr.startswith("Batting_") and not (attr.endswith("HS") or attr.endswith("Ave"))]
bowling_attributes = [attr for attr in all_attributes if attr.startswith("Bowling_") and not (
    attr.endswith("BBI") or attr.endswith("BBM") or attr.endswith("Ave") or attr.endswith("Econ") or attr.endswith("SR")
)]
stat_attributes = [attr for attr in all_attributes 
    if (attr.startswith("HOME_") or attr.startswith("AWAY_") or attr.startswith("NEUTRAL_")) and not (
    attr.endswith("Span") or attr.endswith("HS") or attr.endswith("Avg") or attr.endswith("SR")
)]

clean_BBI_and_BBM(a)
remove_floats_from_required_attributes(a, batting_attributes + bowling_attributes + stat_attributes + ["Jersey_Number"])
edge_case_of_batting_style_and_role(a, ["Batting Style", "Playing Role"])
clean_up_awards(a)
clean_up_records(a)
clean_up_major_trophies(a)

# Storing dataset after necessary initial phase cleaning
a.drop(a.columns[a.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
a.to_csv('final_cricket_players.csv', index=False)
report = sv.analyze(a, pairwise_analysis='off')
report.show_html()


