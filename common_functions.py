# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 16:44:09 2019

@author: Sunil Padikar
"""
import json
import re
def readData(_file_name):

    with open(_file_name) as f:
        skill_pref = json.load(f)
        return skill_pref

def get_skill_associate(search_skills,skills_pref):
    filter_skills = dict()
    for skill in search_skills.split(sep = ','):
        if skill in skills_pref:
            filter_skills[skill] = skills_pref[skill]
    return filter_skills

def get_regx_pattern(fil_back_pref_skills):
    ptrn = ""
    for k,v in fil_back_pref_skills.items():
        ptrn += "|"+k+"|"+"|".join(v["association"].split(","))
    ptrn = "(" + ptrn[1:]+ ")"
    ptrn = re.sub(r"([^A-Za-z0-9\|\(\)\s])", r"\\\1", ptrn)
    return ptrn

def convert_to_list(dictionary):
    new_list = list()
    for k,v in dictionary.items():
        new_list.append(k)        
        new_list = new_list + list(v['association'].split(','))
    return new_list

def value_exist(dictionary,key,value):
    if key not in dictionary:
        dictionary[key] = value
    elif(dictionary[key] > value):
        dictionary[key] = value
    return dictionary

def calc_skills_weight(row,col_name,skills):
    unit_weight = 40
    new_dict = dict()
    if str(row[col_name]) != 'nan':
        opp_skill_set = set(row[col_name].split(','))
        skills_set = list(skills)
        unit_weight /= len(skills_set)
        unit_weight *= 4
        skills_intersect = set(skills_set).intersection(opp_skill_set)
        
        i = 0
        while i<len(skills):
            if skills[i] in skills_intersect:
                if i % 4 == 0:
                    new_dict = value_exist( new_dict,skills[i],unit_weight)
                    i+=4
                elif i % 4 == 1:
                    new_dict = value_exist( new_dict,skills[i],unit_weight*.8)
                    i+=3
                elif i % 4 == 2:
                    new_dict = value_exist( new_dict,skills[i],unit_weight*.75)   
                    i+=2
                elif i % 4 == 3:
                    new_dict = value_exist( new_dict,skills[i],unit_weight*.7)
                    i+=1
            else:
                i+=1
        
    return sum(new_dict.values())
    
def assig_weight(row,skills_pref,back_pref,country):
    weight = 1
    if row['app_by_opening'] < 1 :
      weight = 1
    elif row['app_by_opening'] < 2 :
      weight = 0.85
    elif row['app_by_opening'] > 2 :
      weight = 0.7
      
    skills_weights = calc_skills_weight(row,'opp_skill_pref',skills_pref)
    back_weights = calc_skills_weight(row,'opp_background_pref',back_pref)
    
    country_weights = 20

    
    if country['main'] == row['name_entity'] :
        country_weights *= 1
    elif row['name_entity'] in country['neighbours']:
        country_weights *= 0.75
    elif row['name_entity'] in country['associates']:
        country_weights *= 0.6
    else:
        country_weights *= 0.3
    
    #return (skills_weights + back_weights + country_weights)*weight
    return "Skill:"+str(skills_weights) +"BG:"+ str(back_weights) + "Country:" + str(country_weights) +"App/op"+ str(weight) +"Overall:"+ str((skills_weights + back_weights + country_weights)*weight)

def assig_wei(row,skills_pref,back_pref,country):
    weight = 1
    if row['app_by_opening'] < 1 :
      weight = 1
    elif row['app_by_opening'] < 2 :
      weight = 0.85
    elif row['app_by_opening'] > 2 :
      weight = 0.7
      
    skills_weights = calc_skills_weight(row,'opp_skill_pref',skills_pref)
    back_weights = calc_skills_weight(row,'opp_background_pref',back_pref)
    
    country_weights = 20

    
    if country['main'] == row['name_entity'] :
        country_weights *= 1
    elif row['name_entity'] in country['neighbours']:
        country_weights *= 0.75
    elif row['name_entity'] in country['associates']:
        country_weights *= 0.6
    else:
        country_weights *= 0.3
    
    return (skills_weights + back_weights + country_weights)*weight