import pandas as pd
import sweetviz as sv
import json
import ast
import pickle

a = pd.read_csv("cricket_players.csv", low_memory=False)
all_attributes = a.columns.tolist()

# lists - 
def list_attrs(attributes):
    global a
    for attribute in attributes:
        for i, row in a.iterrows():
            if pd.isnull(a.at[i, attribute]):
                continue
            if str(a.at[i, attribute]) == "":
                continue
            if isinstance(a.at[i, attribute], list) and len(a.at[i, attribute]) >= 1:
                continue
            a.at[i, attribute] = ast.literal_eval(a.at[i, attribute])
           
# dicts - 
def dict_attrs(attributes):
    global a
    for attribute in attributes:
        for i, row in a.iterrows():
            if pd.isnull(a.at[i, attribute]):
                continue
            if str(a.at[i, attribute]) == "":
                continue
            if isinstance(a.at[i, attribute], dict) and len(a.at[i, attribute]) >= 1:
                continue
            a.at[i, attribute] = ast.literal_eval(a.at[i, attribute])
              
# int - 
def to_int_attrs(attributes):
    global a
    for attribute in attributes:
        for i, row in a.iterrows():
            if pd.isnull(a.at[i, attribute]):
                a.at[i, attribute] = -1   
                continue
            if str(a.at[i, attribute]) == "":
                a.at[i, attribute] = -1
                continue
            a.at[i, attribute] = int(float(a.at[i, attribute]))

# float -         
def to_float_attrs(attributes):
    global a
    for attribute in attributes:
        for i, row in a.iterrows():
            if pd.isnull(a.at[i, attribute]):
                a.at[i, attribute] = -1.0
                continue
            if str(a.at[i, attribute]) == "":
                a.at[i, attribute] = -1.0
                continue
            a.at[i, attribute] = float(a.at[i, attribute])

sl = all_attributes[:5] + all_attributes[9:10] + all_attributes[19:20] + all_attributes[29:31] + all_attributes[41:43] + all_attributes[79:81] + all_attributes[118:120] + all_attributes[156:158] + all_attributes[213:215] + all_attributes[102:103] + all_attributes[135:136] + all_attributes[167:168] + all_attributes[186:187] + all_attributes[198:199] + all_attributes[228:229] + all_attributes[60:61] + all_attributes[53:56] + all_attributes[91:94] + all_attributes[125:132] + all_attributes[178:179] + all_attributes[221:224] + all_attributes[145:151]
sl = sl + ["Gender", "Cricinfo_id", "AWARDS"]
dl = all_attributes[90:91]
ll = all_attributes[50:53] + all_attributes[88:89] + all_attributes[144:145] + all_attributes[193:194] + all_attributes[220:221]
ll = [att for att in ll if att != "AWARDS"]

batting_attributes = [attr for attr in all_attributes if attr.startswith("Batting_") and not (attr.endswith("HS") or attr.endswith("Ave"))]
bowling_attributes = [attr for attr in all_attributes if attr.startswith("Bowling_") and not (
    attr.endswith("BBI") or attr.endswith("BBM") or attr.endswith("Ave") or attr.endswith("Econ") or attr.endswith("SR")
)]
stat_attributes = [attr for attr in all_attributes 
    if (attr.startswith("HOME_") or attr.startswith("AWAY_") or attr.startswith("NEUTRAL_")) and not (
    attr.endswith("Span") or attr.endswith("HS") or attr.endswith("Avg") or attr.endswith("SR")
)]
il = batting_attributes + bowling_attributes + stat_attributes + ["Jersey_Number"]

fl = [att for att in all_attributes if (not att in dl) and (not att in ll) and (not att in il) and (not att in sl)]

a = pd.read_csv("cricket_players.csv", low_memory=False)

dict_attrs(dl)
list_attrs(ll)
to_int_attrs(il)
to_float_attrs(fl)

a[il] = a[il].astype(int)
a[fl] = a[fl].astype(float)

indices_to_drop = []

for i, row in a.iterrows():
    ctr = 0
    for attribute in all_attributes:
        if pd.isnull(a.at[i, attribute]):
            continue
        if str(a.at[i, attribute]) == "":
            continue
        if attribute in fl and int(a.at[i, attribute]) < 0:
            continue
        if attribute in il and int(a.at[i, attribute]) < 0:
            continue
        ctr += 1
    if ctr < 58:
        indices_to_drop.append(i)

print(len(indices_to_drop))
print(a.shape)   
for i in indices_to_drop:
    a.drop(i, inplace = True)
print(a.shape)
a.drop(a.columns[a.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
a.to_csv('cricket_players.csv', index=False)
report = sv.analyze(a, pairwise_analysis='off')
report.show_html()

a = pd.read_csv("cricket_players.csv", low_memory=False)
with open('cricket_players_DF.pkl', 'wb') as f:
    pickle.dump(a, f)