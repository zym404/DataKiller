import os
import pandas as pd
from typing import Dict

from langchain_core.vectorstores import VectorStore
from vector_store.Milvus import init_vector_store_from_texts,get_vector_store
from spiliter.excel_spliter import excel_splitter
from spiliter.csv_spiliter import csv_splitter

def _get_all_xlsx_files(source_dir='./docs/标签规则/例子'):
    xlsx_files = []
    file_names = []
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.xlsx'):
                xlsx_files.append(os.path.join(root,file))
                file_names.append(file.replace('.xlsx',''))
    return xlsx_files,file_names

def init_tagging_examples_vector_store() -> Dict[str,VectorStore]:

    xlsx_files, file_names = _get_all_xlsx_files()
    xlsx_files = [excel_splitter(xlsx_file,max_chunk_size=500) for xlsx_file in xlsx_files]

    index = ['Tagging_rules'+str(i) for i in range(len(file_names))]

    vector_dbs = [init_vector_store_from_texts(texts,collection_name=collection_name) for texts,collection_name in zip(xlsx_files,index)]

    vector_dbs = dict(zip(file_names,vector_dbs))
    return vector_dbs


def get_tagging_rules_vector_store() -> Dict[str,VectorStore]:
    _, file_names = _get_all_xlsx_files()
    index = ['Tagging_rules'+str(i) for i in range(len(file_names))]
    vector_dbs = [get_vector_store(collection_name) for collection_name in index]
    vector_dbs = dict(zip(file_names,vector_dbs))
    return vector_dbs
