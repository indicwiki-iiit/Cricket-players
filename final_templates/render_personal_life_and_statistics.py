from jinja2 import Environment, FileSystemLoader
import pandas as pd
import numpy as np
import ast 
import pickle

def translate(var):
    res = list()
    for i in range(len(var)):
        if(var[i] != "nan"):
            if(i == 1):
                re = list_str(var[i],3)
                re = re[0:-1]
                #re = transliterate_text(list_str(var[i],2),lang_code="te")
                
            elif(i == 4):
                relation =str()
                rel = conv(var[i])
                for i in range(len(rel)):
                    try:
                        relation = relation + str(rel[i][0]) + str(rel[i][1])
                    except:
                        relation = relation + str(rel[i][0])
                re = translator.translate(relation,lang_tgt="te",lang_src="en")
            else:
                re = translator.translate(var[i],lang_tgt="te",lang_src="en")
            
            res.append(re)
        else:
            res.append(var[i])
    return res
#Return the data with the converted data type based upon the syntax tree evalution of the source variable. 
def conv(t):
    literal = ast.literal_eval(t)
    return literal
#Add interwiki link sytax to specific data. 
def interwiki(li):
    li = ast.literal_eval(li)
    ret = ""
    for i in range(len(li)):
        ret = ret + "[[" + transliterate_text(li[i],lang_code="te") + "]],"  
    return ret
#Add interwiki link sytax to string which contain date as a part of it. 
def inter_wiki_date(li):
    li = ast.literal_eval(li)
    ret = ""
    for i in range(len(li)):
        ret = ret + "[[" + li[i] + "]],"
    return ret[0:-1]

#Handle list to string converstion for rendering the data. 
def list_str(val,check_year):
    if(check_year == 2):
        p = inter_wiki_date(val)
    elif(check_year == 3):
        p = interwiki(val)
    elif(check_year == 5):
        pr = val
        return pr
    else:
        
        pr = ast.literal_eval(val)
        p = (", ").join(pr)
        p = p.replace(", (","(")
        p = p.replace("( ","(")
    return p
#To handle the missing values and recognizing them
def nan_check(x):
    if(x == -1 or x == "nan" or x == "-1"):
        return "-"
    else:
        return x
#Based upon certain conditions a row within the statistics table need to be dropped ,i.e if all the row values are "nan" , etc. 
def drop_row(dataset,e):
    row_drop = list()
    for i in range(15):
        d = dataset[e*i:e*i+e]
        p = set(d)
        if(len(p) == 1 and "-" in p):
            row_drop.append(i)
        elif(len(p) == 1 and 0 in p):
            row_drop.append(i)
    return row_drop
#Based upon the table data the heading of the table also need to be managed.Few headings might need to be excluded i.e if whole column is "nan".
def head_filter(l_1 , l_2):
    fin_l =list()
    for j in range(len(l_2)):
        if(j not in l_1):
            fin_l.append(l_2[j])
    return fin_l
#To handle abbrevations, a dict map for each english alphabet and string search for values which contain english alphabet and replace them with correponding telugu dict value.
def change_abbr(h):
    alpha= {
    "A":"ఏ",      
    "B":"బీ",
    "C":"సీ",  
    "D":"డి",
    "E":"ఈ",
    "F":"ఎఫ్",
    "G":"జీ",
    "H":"హెచ్",
    "I":"ఐ",
    "J":"జె",       
    "K":"కె",
    "L":"ఎల్",
    "M":"ఎం",
    "N":"ఎన్",
    "O":"ఓ",
    "P":"పి",
    "Q":"క్యూ",
    "R":"ఆర్",   
    "S":"ఎస్",
    "T":"టి",
    "U":"యూ",
    "V":"వీ",
    "W":"డబల్యూ",
    "X":"ఎక్స",
    "Y":"వై",
    "Z":"జీ"
    }
    n = ""
    for i in range(len(h)):
        if(ord(h[i]) >= 65 and ord(h[i]) <= 90):
            n = n + alpha[h[i].upper()] +"."
        else:
            n = n+ h[i]
    return n
#To convert relations attribute and render them.
def relation_print(li):
    ret = ast.literal_eval(li)
    s= ""
    for i in range(len(ret)):
        s = s + ret[i][0] + ret[i][1] + " "
    if(s[-1] == " "):
        s = s[0:-1] + "."
    else:
        s = s+ "."
    return s
#Main function to handle the table values and filter based upon specific conditions.
#Droping columns if all values are "nan" , other edge case handling
def table_check(data):
    one = 0
    two = 0
    three = 0
    threshold = int(len(data)/3)
    for j in range(len(data)):
        data[j] = nan_check(data[j])
        if(j%3 == 0 and data[j] == "-"):
            one += 1
        if(j%3 == 1 and data[j] == "-"):
            two += 1
        if(j%3 == 2 and data[j] == "-"):
            three += 1
    li = [one,two,three]
    drop = list()
    data_1 = data
    for v in range(3):
        if(li[v] == threshold):
            drop.append(v+1)
            del data_1[v::3]
    return [data_1,drop]

def check(tag_name,v,b,c):
    if(v == -1 and b == -1 and c == -1 ):
        em = "-"
        return em
    else:
        v = nan_check(v)
        b = nan_check(b)
        c = nan_check(c)
        val = "| " +str(tag_name)+ " || " + str(v) + " || " + str(b) + " || " + str(c) + " |"
        return val
#Render data for few attributes based upon the stats value with singular and plural suffix.
def sing_plu(v):
    if(v > 1):
        return "లు "
    else:
        return " "
#To include listed python functions as helper functions for the j2 renderer.
func_dict = {
    "check": check,
    "list_str":list_str,
    "nan_check" :nan_check,
    "table_check":table_check,
    "conv":conv,
    "head_filter":head_filter,
    "drop_row":drop_row,
    "translate":translate,
    "change_abbr":change_abbr,
    "sing_plu":sing_plu,
    "relation_print":relation_print
}


a = pd.DataFrame()
with open('./data_collection/data/final_cricket_players_translated_dataset_with_images.pkl', 'rb') as f:
    a = pickle.load(f)

def render(_id, template):
    head = list(a.columns)
    val = a.loc[a["Cricinfo_id"] == _id]
    val = val.replace(np.nan ,"nan")
    val = val.fillna("nan")
    val = dict(val.squeeze())
    env = Environment(loader=FileSystemLoader("./"))
    jinja_template = env.get_template(template)
    jinja_template.globals.update(func_dict)
    template_string = jinja_template.render(val)
    return template_string

def main2(_id):
    return render(_id, template="./final_templates/personal_life.j2")

def main4(_id):
    return render(_id, template="./final_templates/player_statistical_analysis.j2")
