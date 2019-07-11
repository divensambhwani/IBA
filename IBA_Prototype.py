# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 12:47:09 2019
IBA_Prototype
@author: Sunil Padikar
"""

########################Set Working Directory################
import os
#os.chdir(r"C:\Users\Sunil Padikar\Desktop\IBA_Challenge\Prototype")
#########Filter Variables Start#######################
search_country = "Indonesia"
search_skills  = "Adaptability,Agile development,Community Development,Problem Solving"
search_bck_skills =  "Health Science,Social Work"
#########Filter Variables End#########################
#########Read Data Start####################################
import common_functions
import pandas as pd
import re
skills_pref = common_functions.readData('jsons/skill_pref.json')
back_pref = common_functions.readData('jsons/back_pref.json')
neighbours = common_functions.readData('jsons/neighbours_clean.json')
country_ass = pd.read_excel('jsons/country_ass.xlsx')
#all_opportunities = pd.read_csv('jsons/opportunity_iba_challenge.csv')recommendation_data
all_opportunities = pd.read_csv('jsons/recommendation_data.csv')
unique_open_opp = all_opportunities.drop_duplicates(subset='opportunity_id')[all_opportunities['status'] == 'open']
#########Read Data End####################################
#########Apply Filter on Opportunity Start####################################
fil_skills_pref = common_functions.get_skill_associate(search_skills,skills_pref)
fil_back_pref_skills = common_functions.get_skill_associate(search_bck_skills,back_pref)
################Country App By Opening###########
ind = country_ass[country_ass['country'] == search_country].index[0]
app_by_opening = country_ass.iloc[ind,1]
upper = 0
lower = 0
if app_by_opening > 24:
    upper = app_by_opening + (app_by_opening * 0.1) 
    lower = app_by_opening - (app_by_opening * 0.1)
elif app_by_opening < 24 and app_by_opening >= 14:
    upper = app_by_opening + (app_by_opening * 0.05) 
    lower = app_by_opening - (app_by_opening * 0.05)
elif app_by_opening < 1 and app_by_opening >= 0.5:
    upper = app_by_opening + (app_by_opening * 0.8) 
    lower = app_by_opening - (app_by_opening * 0.8)
elif app_by_opening < 0.5 and app_by_opening >= 0.2:
    upper = app_by_opening + (app_by_opening * 0.5) 
    lower = app_by_opening - (app_by_opening * 0.5)
elif app_by_opening < 0.2:
    upper = app_by_opening + (app_by_opening * 2) 
    lower = app_by_opening - (app_by_opening * 2)
else:
    upper = app_by_opening + (app_by_opening * 0.1) 
    lower = app_by_opening - (app_by_opening * 0.1)

country_ass_final = country_ass[country_ass['app_by_opening'] <= upper]
country_ass_final  = country_ass_final[country_ass_final['app_by_opening'] >= lower]
"""
end_val = len(country_ass)
cont_ass_list  = []
start_val = 0

if ind+3 <= end_val:
    end_val = ind+3
if start_val <= ind-3:
    start_val = ind-3
    cont_ass_list = country_ass.iloc[start_val:end_val,]['country'].tolist()

fil_neighbours = neighbours[search_country] + cont_ass_list 
fil_neighbours = list(set(fil_neighbours))
"""
################Country App By Opening###########
bg_ptrn = common_functions.get_regx_pattern(fil_back_pref_skills)
sp_ptrn = common_functions.get_regx_pattern(fil_skills_pref)

fil_by_bg = unique_open_opp[unique_open_opp['opp_background_pref'].str.contains(bg_ptrn, na = False)]    
fil_by_sp = unique_open_opp[unique_open_opp['opp_skill_pref'].str.contains(sp_ptrn, na = False)]

fil_stg_sp_bg = [fil_by_bg,fil_by_sp]
fil_stg_sp_bg = pd.concat(fil_stg_sp_bg).drop_duplicates(subset='opportunity_id')

#Country filter is commmented to for now
#cntry = "("+re.sub(r"([^A-Za-z0-9\|\s])", r"\\\1", "|".join(fil_neighbours))+")"
#fil_stg_sp_bg = fil_stg_sp_bg[fil_stg_sp_bg['name_entity'].str.contains(cntry, na = False)]
#########Apply Filter on Opportunity End####################################

ctry = {"main":search_country,"neighbours":"|".join(neighbours[search_country]), "associates":country_ass_final['country'].tolist()}
#########Rank Opportunity Start####################################
fil_stg_sp_bg['app_by_opening_weight'] = fil_stg_sp_bg.apply(lambda row: common_functions.assig_weight(row,common_functions.convert_to_list(fil_skills_pref),common_functions.convert_to_list(fil_back_pref_skills),ctry), axis = 1)
#########Rank Opportunity End####################################
fil_stg_sp_bg['app_by_opening_wei'] = fil_stg_sp_bg.apply(lambda row: common_functions.assig_wei(row,common_functions.convert_to_list(fil_skills_pref),common_functions.convert_to_list(fil_back_pref_skills),ctry), axis = 1)
fil_stf_sp_bg = fil_stg_sp_bg.iloc[:,[1,2,5,9,12,13]]
