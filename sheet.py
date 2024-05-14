'''
-------------------------------------------------------------------
* sheet.py
* 구글 스프레드 시트 정보 가져와서 DB에 저장
* 
* API Limit : 5(read/s), 1(write/s)
-------------------------------------------------------------------
'''
# Module Import
import random
import os
from enum import Enum
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(os.getenv('JSON_FILE'), scope)
client = gspread.authorize(creds)
URL = os.getenv('SHEET_URL')
gc = client.open_by_url(URL)

Skill_list = []


def init_Enum():
    global Skill_list
    worksheet = gc.get_worksheet(0)
    temp = worksheet.get('C43:D60')
    temp += worksheet.get('P43:Q60')
    temp += worksheet.get('AD43:AE60')
    Skill_list = ['근력','건강','크기','민첩','지능','정신력','교육','행운']
    for item in temp :
        if item[0] == 'FALSE' :
            continue
        elif item[0] == 'TRUE' :
            Skill_list.append(item[1])
    enum_dict = {name: value for name, value in zip(Skill_list, Skill_list)}
    return Enum("Skill", enum_dict)

def sheet(name):
    global Skill_list
    # Init
    worksheet = gc.worksheet(name)
    temp = worksheet.get('C43:K60')
    temp += worksheet.get('P43:X60')
    temp += worksheet.get('AD43:AS60')
    
    dict = {}
    dict[Skill_list[0]] = int(worksheet.acell('Z9').value)     
    dict[Skill_list[1]] = int(worksheet.acell('Z13').value)    
    dict[Skill_list[2]] = int(worksheet.acell('Z17').value)   
    dict[Skill_list[3]] = int(worksheet.acell('AI9').value)
    dict[Skill_list[4]] = int(worksheet.acell('AI13').value)
    dict[Skill_list[5]] = int(worksheet.acell('AI17').value)
    dict[Skill_list[6]] = int(worksheet.acell('AR9').value)
    dict[Skill_list[7]] = int(worksheet.acell('AR13').value)
    dict[Skill_list[8]] = int(worksheet.acell('C32').value)
   
    for item in temp :
        if item[0] == 'FALSE' :
            continue
        elif item[0] == 'TRUE' :
            dict[item[1]] = int(item[-1])
    return dict

    
def sanc(name, suc_val , fail_val):
    worksheet = gc.worksheet(name)
    San = int(worksheet.acell('AM25').value)
    
    dice_val = random.randrange(1,100)
    
    # 성공
    if dice_val <= San : 
        if (suc_val > 0) :
            San -= suc_val
            worksheet.update('AM25',San)    
        return '성공', dice_val
    else :
        if (fail_val > 0) :
            San -= fail_val
            worksheet.update('AM25',San)    
        return '실패', dice_val