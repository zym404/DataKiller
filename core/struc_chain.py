import time
import json
import pandas as pd
import logging
import os
from core.model_config import LLM,LLM_B
from core.output_format_conversion import Json2DataFrame_InquryLetter
from vector_store.Milvus import get_all_file_name, get_all_sub_path
from spiliter.pdf_splitter import PdfEngine
from core.output_format_conversion import Json2Dict
from prompt.annual_report import ANNUAL_REPORT_PROMPT
from spiliter.excel_spliter import excel_splitter

os.environ["LANGCHAIN_TRACING_V2"] = "true"  
os.environ["LANGCHAIN_PROJECT"] = "DateKiller_1.0"  
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"  
os.environ["LANGCHAIN_API_KEY"] = "ls__4e4954be6c504e5f8bd17bf19e0a8396"  # 更新为您的API密钥
# os.environ["OPENAI_PROXY"] = "http://127.0.0.1:7890"


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# def StructualInqueryLetter(
#         cls, 
#         query: str, 
#         file_type = '问询函',
#         waiting_time = 20,
#         ) -> pd.DataFrame:
#         '''
#         LLM调用有TMP和RPM限制，一分钟内token和request不能超过某一个数量
#         结构化任务容易触发这个限制，故出现改情形时，可以适当加大waiting_time参数
#         '''
#         doc_list = return_raw_file(file_type)[:5] # 生成要格式化的文件任务队列
#         filename_list = get_all_file_name(file_type) # 生成文件名的任务队列

#         llm = LLM
#         struc_chain = load_chain(llm=llm,chain_type='stuff', verbose=cls.enable_debug)

#         output = ''
#         df = pd.DataFrame()
#         for i in range(len(doc_list)):
#             doc = doc_list[i]
#             _query = query.format(inquiry_letter=filename_list[i])
#             logging.debug(f"Executing StructualInqueryLetter with query: {_query} and filename: {filename_list[i]}")

#             chain = struc_chain({"input_documents": doc, "question": _query},
#                         return_only_outputs=cls.enable_debug)
#             txt = chain["output_text"]
#             output += txt
#             try:
#                 df_tmp = Json2DataFrame_InquryLetter(txt)
#                 df = pd.concat([df,df_tmp],ignore_index=True)
#             except:
#                 print(f'{filename_list[i]}未成功')
#             time.sleep(waiting_time)
#         print("使用向量数据库+千帆线上模型")
#         print(output)
#         return df, output

file_paths = get_all_sub_path(r"D:\DataKiller\DataKiller 1.0\docs\年报问询函" , ".pdf")
filename_list = get_all_file_name("年报问询函")


# def gen_query_batch(file_paths,sleep=0.2):
#     # 千帆的embedding为QPS限制为5，所以需要sleep 0.2s
#     for file_path in file_paths:
#         # TODO 阈值类tag和非阈值类tag的k
#         # time.sleep(sleep)        
#         yield {'inquiry_letter_name':"年报问询函", 'context':PdfEngine.return_raw_file(file_path)}


chain = ANNUAL_REPORT_PROMPT | LLM
a = PdfEngine.return_raw_file(file_paths[0])


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
    # time.sleep(60)   

# file_paths.index(file_path)

df = pd.DataFrame()
for i in range(13,int(len(file_paths)/5)+1):
    query_batch = [{'inquiry_letter_name':"年报问询函", 'context':PdfEngine.return_raw_file(file_path)} for file_path in file_paths[i:i+5]]

    output = chain.batch(query_batch)
    print(output)
    output = [Json2Dict(record.content) for record in output]
    filtered_dict = [{key: value for key, value in record.items() if key != "列表"} for record in output]
    for j in range(len(output)):
        for x in output[j]['列表']:
            x.update(filtered_dict[j])
        df = df._append(output[j]['列表'],ignore_index=True)
    print(f"***********************\n\n*******第{str(i)}批完成******\n\n***********************")
    if i % 10 == 0:
        time.sleep(180)
        
    time.sleep(60)   
    

df.to_excel('final2.xlsx')
   




