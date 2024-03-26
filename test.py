import os
os.chdir('DataKiller')
from core.qa_chain_qianfan import DocChatter
import json
import re
# query ='''
# 1. 请说明什么是企业的隐性关联方交易。
# 2. 请基于贵人鸟问询函内容，并说明贵人鸟公司是否疑似存在隐性关联方交易。
# 3. 请详细的说明贵人鸟疑似关联方的细节，注意结合问询函的内容。

# 回答以上问题并返回你的CoT
# '''
# 每一个存在监管问题，字典的关键字字段都需要有记录！！！，如果找不到，相应关键字字段记录为"/"

# query ='''
# 将贵人鸟问询函内容整理成json的格式输出。
# json的关键字只有以下这几个:公司名称、证券代码、公告日期、监管问题详情、公司答复、涉及财报科目，涉及金额。
# 注意，关键字的数据类型是str，对应的值的数据类型是list，且list中的元素的数据类型为str

# 请不要输出与json无关的回答
# 比如A公司存在两个监管问题，最后输出
# ```{
#   "公司名称": ["公司A","公司A"],
#   "证券代码": ["公司A代码","公司A代码"],
#   "公告日期": ["公司A公告日期","公司A公告日期"],
#   "监管问题详情": ["公司A监管问题详情1","公司A监管问题详情2"],
#   "公司答复": ["公司A答复1","公司A答复2"],
  
#   "涉及财报科目": [
#     "科目1",
#     "科目2"
#   ],
#   "涉及金额": [
#     "金额1",
#     "金额2"
#   ]
# }
# ```

# '''

query = '''
以下文本是{inquiry_letter}，请将内容按照监管问题的要点整理成json的格式输出
json的关键字只有以下这几个:监管问题、公司答复、涉及财报科目、涉及金额、公司名称、证券代码、公告日期。
注意：文本是由pdf解析器解析而来，故字符与字符之间存在不必要的空格，请不要输出这些空格
请不要输出和json格式无关的文本
'''

# query ='''
# 将贵人鸟问询函内容整理成Python字典的格式输出。
# 字典的关键字只有以下这几个:公司名称、证券代码、公告日期、监管问题、公司答复、涉及财报科目，涉及金额。

# 请不要输出与Python字典无关的回答

# ```{
#   "公司名称": ["公司A","公司A"],
#   "证券代码": ["公司A代码","公司A代码"],
#   "公告日期": ["公司A公告日期","公司A公告日期"],
#   "监管问题": ["公司A监管问题1","公司A监管问题2"],
#   "公司答复": ["公司A答复1","公司A答复2"],
  
  # "涉及财报科目": [
  #   "科目1",
  #   "科目2"
  # ],
  # "涉及金额": [
  #   "金额1",
  #   "金额2"
  # ]
# }
# ```

# '''

# txt = DocChatter.GptRagQuery(top_n=5,query=query)   
txt = DocChatter.StructualQuery(query=query)
# import qianfan
# qianfan.ChatCompletion().models()
output = json.loads(txt[txt.index('{'):-3].replace('\n',''))
import pandas as pd
df = pd.DataFrame(columns=['公司名称', '证券代码', '公告日期', '监管问题', '公司答复', '涉及财报科目', '涉及金额'])

txt

df._append(output,ignore_index=True)
txt.replace('\n','')
matches = re.findall(r'\[(.*?)\]',txt , re.DOTALL)
json.loads(matches[0][1:-2])
print(matches[0][1:-2])
print(matches)
matches[0]


