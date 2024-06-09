import json
import pandas as pd
import re

# def Json2DataFrame_InquryLetter(txt:str) -> pd.DataFrame:
#     matches = re.findall(r'```json(.*?)```',txt , re.DOTALL)[0].replace('\n','')
#     json_script = json.loads(matches)
#     df = pd.DataFrame(json_script['列表'])
#     try:
#         lst = ['问询函主题','问询机构','函件类别','公司名称','证券代码','公告日期','几日内回复','截止到哪天之前回复']
#         for x in lst:
#             df[x] = json_script[x]
#         return df
#     except:
#         return df
    
def Json2DataFrame_InquryLetter(txt:str) -> pd.DataFrame:
    matches = re.findall(r'```json(.*?)```',txt , re.DOTALL)[0].replace('\n','')
    json_script = json.loads(matches)
    df = pd.DataFrame(json_script['列表'])
    try:
        lst = ['问询机构','函件类别','公司名称','公告日期','公告编号','回复截止日期']
        for x in lst:
            df[x] = json_script[x]
        return df
    except:
        return df

def Json2Dict(txt:str) -> dict:
    if re.findall(r'```json(.*?)```',txt , re.DOTALL):
        matches = re.findall(r'```json(.*?)```',txt , re.DOTALL)[0].replace('\n','')
        json_script = json.loads(matches)
    elif txt[0]=='{' and txt[-1]=='}':
        json_script = json.loads(txt)
    return json_script

