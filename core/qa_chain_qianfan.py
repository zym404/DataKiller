import langchain
import logging
import json
import os
from core.core_chain import load_chain
from core.vector_db_qianfan import get_vector_store, VectorCollectionName,return_raw_file,get_all_file_name
from langchain_community.llms.chatglm3 import ChatGLM3
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.schema.messages import AIMessage
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain.agents import initialize_agent, AgentType
from langchain_community.embeddings import QianfanEmbeddingsEndpoint
from langchain_community.llms.baidu_qianfan_endpoint import QianfanLLMEndpoint
from langchain_community.chat_models.baidu_qianfan_endpoint import QianfanChatEndpoint
from langchain_community.chat_models import QianfanChatEndpoint
from PyPDF2 import PdfReader

# 设置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 设置 API 密钥

os.environ["QIANFAN_AK"] = "gKMOfVu47gp3BMMUJb8EPpfG"
os.environ["QIANFAN_SK"] = "1G5RdeXf9RdIjj6bzeF4A1udqT8jTEPl"

vector_db = get_vector_store(collection_name=VectorCollectionName)


QianfanLLM = QianfanLLMEndpoint(
    model="ERNIE-Speed-128k",
    temperature=0.1
    )

class DocChatter(object):
    enable_debug = True

    @classmethod
    def enable_debug_mode(cls, is_enable: bool) -> None:
        cls.enable_debug = is_enable
        langchain.debug = is_enable
        logging.info(f"Debug mode set to {'enabled' if is_enable else 'disabled'}.")

    @classmethod
    def StructualQuery(cls, query: str, filename=None,):
        logging.debug(f"Executing StructualQuery with query: {query} and filename: {filename}")
        doc_list = return_raw_file()
        filename_list = get_all_file_name()
        llm = QianfanLLM
        nchain = load_chain(llm=llm, verbose=cls.enable_debug)
        for i in range(len(doc_list)):
            doc = doc_list[i]
            real = nchain({"input_documents": doc, "question": query.format(inquiry_letter=filename_list[i]) + " 用中文回答，并且输出内容来源。"},
                        return_only_outputs=cls.enable_debug)
            txt = real["output_text"]
            # output = json.loads(txt[txt.index('{'):-3].replace('\n',''))
        print("使用向量数据库+千帆线上模型")
        print(real["output_text"])
        return real["output_text"]
    
    @classmethod
    def GptRagQuery(cls, top_n: int, query: str):
        logging.debug(f"Executing GptRagQuery with query: {query} and top_n: {top_n}")
        # 查询相似度向量库
        # docs = vector_db.similarity_search(query=query, k=4)
        docs = return_raw_file()[0]
        print(len(docs))
        if len(docs) == 0:
            return print("没有找到相关的文档")
        logging.debug(f"Retrieved top {top_n} documents for query.")
        print('foun oucumnt' + query)
        llm = QianfanLLM
        nchain = load_chain(llm=llm, verbose=cls.enable_debug)
        # nchain = qa_chain(llm=llm, return_map_steps=cls.enable_debug, verbose=cls.enable_debug)
        real = nchain({"input_documents": docs, "question": query + " 用中文回答"},
                      return_only_outputs=cls.enable_debug)
        print("使用向量数据库+千帆线上模型")
        print(real["output_text"])
        return real["output_text"]

    @classmethod
    def VectorQuery(cls, top_n: int, query: str):
        logging.debug(f"Executing VectorQuery with query: {query} and top_n: {top_n}")

        # 查询相似度向量库
        docs = vector_db.similarity_search(query=query, k=1)
        print(len(docs))
        if len(docs) == 0:
            return "没有找到相关的文档"
        print("使用向量数据库直接查找")
        logging.debug(f"Retrieved top {top_n} documents for query.")
        return docs[0]


# DocChatter.VectorQuery(top_n=6,query='贵人鸟是什么')
    # @classmethod
    # def LocalQuery(cls, top_n: int, query: str):
    #     logging.debug(f"Executing LocalQuery with query: {query} and top_n: {top_n}")
    #     # 调用本地模型进行查询，并且rag检索
    #     docs = vector_db.similarity_search(query=query, k=2)
    #     print(len(docs))
    #     if len(docs) == 0:
    #         return print("没有找到相关的文档")
    #     logging.debug(f"Retrieved top {top_n} documents for query.")
    #     print('foun oucumnt' + query)
    #     endpoint_url = "http://9.135.219.182:20000/v1/chat/completions"
    #     messages = [
    #         AIMessage(content="欢迎问我任何问题"),
    #     ]
    #     llm = ChatGLM3(
    #         endpoint_url=endpoint_url,
    #         max_tokens=80000,
    #         prefix_messages=messages,
    #         top_p=0.0
    #     )
    #     nchain = load_qa_chain(llm=llm, return_map_steps=cls.enable_debug, verbose=cls.enable_debug)
    #     real = nchain({"input_documents": docs, "question": query + " 用中文回答，并且输出内容来源。"},
    #                   return_only_outputs=cls.enable_debug)
    #     print("使用向量数据库+GLM3本地模型")
    #     print(real["output_text"])
    #     return real["output_text"]

    # @classmethod
    # def LocalQueryMysql(cls, top_n: int, query: str):
    #     logging.debug(f"Executing LocalQuery with query: {query} and top_n: {top_n}")
    #     # 调用本地模型进行查询，并且rag检索
    #     print('query:' + query)
    #     endpoint_url = "http://9.135.219.182:20000/v1/chat/completions"
    #     # messages = [
    #     #     AIMessage(content="欢迎问我任何问题"),
    #     # ]
    #     llm = ChatGLM3(
    #         endpoint_url=endpoint_url,
    #         max_tokens=8000,
    #         #prefix_messages=messages,
    #         top_p=0.0
    #     )

    #     llm = llm(temperature=0.0)

    #     username = "root"
    #     password = "111111"
    #     host = '9.134.251.252'
    #     port= '13306'
    #     database = 'gva'
    #     db=SQLDatabase.from_uri(f"mysql+pymysql://{username}:{password}@{host}:{int(port)}/{database}")
    #     agent_executor = create_sql_agent(llm, db=db, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

    #     #db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

    #     toolkit = SQLDatabaseToolkit(db=db,llm=llm)
    #     context = toolkit.get_context()
    #     tools = toolkit.get_tools()
    #     messages = [
    #         HumanMessagePromptTemplate.from_template("{input}"),
    #         AIMessage(content="你现在是一名数据分析师,结合得到的数据给出合适的建议。"),
    #     ]

    #     prompt = ChatPromptTemplate.from_messages(messages)
    #     agent_executor = create_sql_agent(
    #         llm=llm,
    #        # db=db, 只需要db或则toolkit一种
    #         toolkit=toolkit,
    #         agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    #         verbose=True,
    #         handle_parsing_errors=True,
    #     )



    #     output = agent_executor.invoke(query)
    #     print('------------------')
    #     print(type(output))
    #     print(output)





    #     return output
