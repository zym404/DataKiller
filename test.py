import os
from core.qa_chain_qianfan import DocChatter

# query ='''
# 1. 请说明什么是企业的隐性关联方交易。
# 2. 请基于贵人鸟问询函内容，并说明贵人鸟公司是否疑似存在隐性关联方交易。
# 3. 请详细的说明贵人鸟疑似关联方的细节，注意结合问询函的内容。

# 回答以上问题并返回你的CoT
# '''

query ='''
将贵人鸟问询函内容整理成Python字典的格式输出。
字典的关键字只有以下这几个:公司名称、证券代码、公告日期、监管问题、公司答复、涉及财报科目，涉及金额。
注意，关键字的数据类型是str，对应的值的数据类型是list，且list中的元素的数据类型为str
每一个监管问题，单独一行。
请不要输出与Python字典无关的回答
一个监管问题对应一条记录，如果已存在多个监管问题，请返回多条记录
比如A公司存在两个监管问题，最后输出
```{
  "公司名称": ["公司A","公司A"],
  "证券代码": ["公司A代码","公司A代码"],
  "公告日期": ["公司A公告日期","公司A公告日期"],
  "监管问题": ["公司A监管问题1","公司A监管问题2"],
  "公司答复": ["公司A答复1","公司A答复2"],
  
  "涉及财报科目": [
    "扣除非经常性损益后的净利润",
    "司法重整留债债务本息"
  ],
  "涉及金额": [
    "5亿元",
    "2.1亿元"
  ]
}
```

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

txt = DocChatter.GptRagQuery(top_n=5,query=query)   

print(txt)
txt[txt.index("python")+6:-3].replace('\n','')