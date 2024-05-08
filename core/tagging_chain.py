import os
import time
import json
import pandas as pd
import logging
from typing import Dict

from core.model_config import LLM
from vector_store.tagging_examples_initialize import (
    init_tagging_examples_vector_store, 
    get_tagging_rules_vector_store,
    _get_all_xlsx_files
)
from core.output_format_conversion import Json2Dict
from prompt.tagging import TAGGING_PROMPT
from spiliter.excel_spliter import excel_splitter
from spiliter.pdf_splitter import PdfEngine
from vector_store.Milvus import init_vector_store_from_texts,get_vector_store
from spiliter.excel_spliter import excel_splitter


# vector_dbs = get_tagging_rules_vector_store()

# 第一次使用或者更新案例库使用该代码
# 目前暂未实现将例子放入向量库中，暂时无法使用
# vector_dbs = init_tagging_examples_vector_store()

rules_queue,tags_queue = _get_all_xlsx_files('./docs/标签规则/规则定义')
rules_queue = [excel_splitter(rule_file) for rule_file in rules_queue]
rules_queue = dict(zip(tags_queue,rules_queue))

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

questions_queue = excel_splitter(r"D:\DataKiller\final.xlsx")[:5]

def gen_query_batch(tags_queue,
                    questions_queue, 
                    rules_queue, 
                    vector_dbs, 
                    k=3,sleep=0.2):
    # 千帆的embedding为QPS限制为5，所以需要sleep 0.2s
    for question in questions_queue:
        for tag in tags_queue:
            # TODO 阈值类tag和非阈值类tag的k
            time.sleep(sleep)  

            yield {'tag':tag, 
                   'question':question, 
                   'rules':rules_queue[tag],
                   'examples':""}
                #    'examples':vector_dbs[tag].similarity_search(query=question, k=1)}


chain = TAGGING_PROMPT | LLM
vector_dbs = ""

df = pd.DataFrame()

for i in range(len(questions_queue)):
    query_batch = [query for query in gen_query_batch(tags_queue, [questions_queue[i]], rules_queue,vector_dbs)]

    _output = chain.batch(query_batch)
    print(_output)
    output = [Json2Dict(_output[i]) for i in range(len(_output))]
    # Json2Dict(_output[1].content)

    record = eval(questions_queue[i])
    for i in range(len(output)):
        tag = tags_queue[i]
        if tag != "关键字":
            record[f'{tag}'] = output[i]['标签结果']
            record[f'{tag}判断依据'] = output[i]['判断依据']
            record[f'{tag}原文引用'] = output[i]['原文引用']
        elif tag == "关键字":
            if type(output[i]) == type(list()):
                for j in range(len(output[i])):
                    record[f'{tag}_{j+1}'] = output[i][j]['标签结果']
                    record[f'{tag}判断依据_{j+1}'] = output[i][j]['判断依据']
                    record[f'{tag}原文引用_{j+1}'] = output[i][j]['原文引用']
            elif type(output[i]) == type(dict()):
                record[f'{tag}_1'] = output[i]['标签结果']
                record[f'{tag}判断依据_1'] = output[i]['判断依据']
                record[f'{tag}原文引用_1'] = output[i]['原文引用']
        # record[f'{tag}'] = output[i]['标签']
        # record[f'{tag}判断依据'] = output[i]['判断依据']
        # record[f'{tag}原文引用'] = output[i]['原文引用']
    df = df._append(record,ignore_index=True)

    print("***********BATCH DONE*******************")
    time.sleep(30)

df.to_excel('tagging.xlsx')




