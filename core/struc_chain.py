import time
import json
import pandas as pd
import logging
import os
from core.model_config import LLM_STRUC
from core.output_format_conversion import Json2DataFrame_InquryLetter
from vector_store.Milvus import get_all_file_name, get_all_sub_path
from spiliter.pdf_splitter import PdfEngine
from core.output_format_conversion import Json2Dict
from prompt.annual_report import ANNUAL_REPORT_PROMPT
from spiliter.excel_spliter import excel_splitter
from core.checking import checking
# from core.checking import checking


os.environ["LANGCHAIN_TRACING_V2"] = "true"  
os.environ["LANGCHAIN_PROJECT"] = "DateKiller_1.0"  
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"  
os.environ["LANGCHAIN_API_KEY"] = "ls__4e4954be6c504e5f8bd17bf19e0a8396"  # 更新为您的API密钥
# os.environ["OPENAI_PROXY"] = "http://127.0.0.1:7890"

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')




# def gen_query_batch(file_paths,sleep=0.2):
#     # 千帆的embedding为QPS限制为5，所以需要sleep 0.2s
#     for file_path in file_paths:
#         # TODO 阈值类tag和非阈值类tag的k
#         # time.sleep(sleep)        
#         yield {'inquiry_letter_name':"年报问询函", 'context':PdfEngine.return_raw_file(file_path)}




# df = pd.DataFrame()

# for file_path in file_paths[11:]:
#     query =  {'inquiry_letter_name':"年报问询函", 'context':PdfEngine.return_raw_file(file_path)}

#     _output = chain.invoke(query)  

#     output = _output
#     # print(output)
#     output = Json2Dict(output.content)
#     filtered_dict = {key: value for key, value in output.items() if key != "列表"}
#     for x in output['列表']:
#         x.update(filtered_dict)
#     df = df._append(output['列表'],ignore_index=True)
#     print(f"***********************\n\n*******{file_path}完成******\n\n***********************")
#     time.sleep(60)   

# file_paths.index(file_path)
# filename_list = tmp
# file_paths = p

def struc_chain(source_dir,
                filename_list,
                save_file=True,
                output_filename='final',
                start_batch=0,
                end_batch=0,
                n = 5, # 每批数量
                ):
    if end_batch == 0:
        end_batch = int(len(filename_list)/n)
    df = pd.DataFrame()
    file_paths = [source_dir+'\\'+filename+'.pdf' for filename in filename_list]
    for i in range(start_batch,end_batch+1):
        query_batch = [{'inquiry_letter_name':filename, 'context':PdfEngine.return_raw_file(file_path)} for file_path in file_paths[i:i+n] for filename in filename_list[i:i+n]]

        output = chain.batch(query_batch)
        print(output)
        output = [Json2Dict(record.content) for record in output]
        filtered_dict = [{key: value for key, value in record.items() if key != "列表"} for record in output]
        for j in range(len(output)):
            for x in output[j]['列表']:
                x.update(filtered_dict[j])
            output[j]['列表']['文件名称'] = filename_list[i:i+5][j]
            df = df.append(output[j]['列表'],ignore_index=True)
        print(f"***********************\n\n*******第{str(i)}批完成******\n\n***********************")
        if i % 10 == 0:
            time.sleep(180)
            
        time.sleep(60)   
    if save_file:
        df.to_excel(output_filename+'.xlsx')
    return df

'''
# 使用时把年报放入“年报问询函”文件夹下
# 可以用start_batch、end_batch和n调节跑批的参数
'''
source_dir = r"D:\DataKiller\DataKiller 1.0\docs\年报问询函"
filename_list = get_all_file_name("年报问询函")

chain = ANNUAL_REPORT_PROMPT | LLM_STRUC


file_paths = [source_dir+'\\'+filename+'.pdf' for filename in filename_list]
df = struc_chain(source_dir,filename_list,output_filename='final_1')

df_with_problem = checking(df) # 检验
filename_list_with_problem = df_with_problem['文件名称'] # 有问题的名单，会再跑一遍

df_new = struc_chain(source_dir,filename_list_with_problem,
                    output_filename='final_checking',
                    start_batch=0,
                    end_batch=1,
                    )


