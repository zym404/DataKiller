import json
import pandas as pd
from typing import Any, Dict, List, Optional
from copy import deepcopy
import pickle
import requests
from langchain_text_splitters import RecursiveJsonSplitter
'''
# note: RecursiveJsonSplitter的方法使用到递归，会对可变对象做出更改，所以需要使用序列化/反序列化
# 实现读取excel文件并按行进行分割
# 1. 读取excel文件
# 2. 转换为json格式
# 3. 使用RecursiveJsonSplitter进行文本分割
# 4. 输出分割后的文本
'''
def excel_splitter(filepath: str,
                   with_index: Optional[bool]=False,
                   max_chunk_size: Optional[str]=500,
                   ) -> List[Dict]:
    # filepath = r'./docs/IDOU测试样例/03_异常事件触发情况_20231024.xlsx'
    # max_chunk_size=1000
    df = pd.read_excel(filepath)
    if with_index:
        df.reset_index(inplace=True)
    txt = df.to_json(orient='records',force_ascii=False)
    json_data = json.loads(txt)
    json_data = [str(data) for data in json_data]
    return json_data




