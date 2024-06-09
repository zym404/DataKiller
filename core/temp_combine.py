import pandas as pd
import os
from functools import reduce
def _get_all_xlsx_files(source_dir='./docs/2022年报问询函'):
    xlsx_files = []
    file_names = []
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.xlsx'):
                xlsx_files.append(os.path.join(root,file))
                file_names.append(file.replace('.xlsx',''))
    return xlsx_files,file_names

file_list,_ = _get_all_xlsx_files()
file_list = [pd.read_excel(file_path) for file_path in file_list]

df = pd.concat(file_list,ignore_index=True,axis=0)
df = df.drop("Unnamed: 0",axis=1)
df.to_excel("./docs/2022年报问询函.xlsx")