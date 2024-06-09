import os
import time
import json
import pandas as pd
import logging
import re

from core.model_config import LLM
from vector_store.tagging_examples_initialize import (
    init_tagging_examples_vector_store, 
    get_tagging_rules_vector_store,
    _get_all_xlsx_files
)
from core.output_format_conversion import Json2Dict
from prompt.tagging import TAGGING_PROMPT
from spiliter.excel_spliter import excel_splitter

# vector_dbs = get_tagging_rules_vector_store()

# 第一次使用或者更新案例库使用该代码
# 目前暂未实现将例子放入向量库中，暂时无法使用
# vector_dbs = init_tagging_examples_vector_store()

rules_queue,tags_queue = _get_all_xlsx_files('./docs/标签规则/规则定义')
rules_queue = [excel_splitter(rule_file) for rule_file in rules_queue]
rules_queue = dict(zip(tags_queue,rules_queue))

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

questions_queue = excel_splitter(r"./docs/2023年报问询函 - 副本.xlsx")

def gen_query_batch(tags_queue,
                    question, 
                    rules_queue, 
                    vector_dbs, 
                    k=3,sleep=0.2):
    # 千帆的embedding为QPS限制为5，所以需要sleep 0.2s
    for tag in tags_queue:
        # TODO 阈值类tag和非阈值类tag的k
        time.sleep(sleep)  

        yield {
            'tag':tag, 
            'question':question, 
            'rules':rules_queue[tag],
            'examples':""
        }   # 暂时不加入例子
            #    'examples':vector_dbs[tag].similarity_search(query=question, k=1)}


chain = TAGGING_PROMPT | LLM
vector_dbs = ""

def cast_output_to_dict(_output,record,query_batch,error_count=0)-> dict:
    try:
        output = [Json2Dict(_output[i]) for i in range(len(_output))]
    except json.JSONDecodeError as e:
        error_count += 1
        _output = [re.sub(r'\n  “', r'\n "', _output[i]) for i in range(len(_output))] 
        _output = [re.sub(r'”:', '":', _output[i]) for i in range(len(_output))] 
        _output = [re.sub(r': “', ': "', _output[i]) for i in range(len(_output))] 
        _output = [re.sub(r'”,', '",', _output[i]) for i in range(len(_output))] 
        _output = [re.sub(r'”\n', '"\n', _output[i]) for i in range(len(_output))] 
        output = [Json2Dict(_output[i]) for i in range(len(_output))] 

    # record = query_batch[0]['question']
    # record = eval(questions_queue[i])
    for j in range(len(output)):
        # tag = tags_queue[j]
        tag = query_batch[j]['tag']
        if tag != "关键字":
            record[f'{tag}'] = output[j]['标签结果']
            record[f'{tag}判断依据'] = output[j]['判断依据']
            record[f'{tag}原文引用'] = output[j]['原文引用']
        elif tag == "关键字":
            if type(output[j]) == type(list()):
                for k in range(len(output[j])):
                    record[f'{tag}_{j+1}'] = output[j][k]['标签结果']
                    record[f'{tag}判断依据_{j+1}'] = output[j][k]['判断依据']
                    record[f'{tag}原文引用_{j+1}'] = output[j][k]['原文引用']
            elif type(output[j]) == type(dict()):
                record[f'{tag}_1'] = output[j]['标签结果']
                record[f'{tag}判断依据_1'] = output[j]['判断依据']
                record[f'{tag}原文引用_1'] = output[j]['原文引用']
    return record,error_count

df = pd.DataFrame()
error_count = 0

# for i in range(0,len(questions_queue)):
for i in range(68,150):
    query_batch = {query['tag']: query for query in gen_query_batch(tags_queue, questions_queue[i], rules_queue,vector_dbs)}
    
    query_1 = [query_batch['关键字']]
    output_1 = chain.invoke(query_1[0])
    print(output_1)
    output_1 = [output_1.content]
    record_1 = eval(questions_queue[i])
    record_1,_ = cast_output_to_dict(output_1,record_1,query_1,error_count)

    query_2 = [query_batch[tag] for tag in query_batch if tag != '关键字']
    output_2 = chain.batch(query_2)
    print(output_2)
    output_2 = [output.content for output in output_2]
    record_2,_ = cast_output_to_dict(output_2,record_1,query_2,error_count)
    
    df = df._append(record_2,ignore_index=True)

    print(f"***********\n\nBATCH {i} DONE\n\n*******************")
    # time.sleep(30)

# print(error_count)
df.to_excel('tagging_new.xlsx')

# Json2Dict(output_1[0])
