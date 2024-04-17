import os
from core.model_config import EMB
from langchain_community.vectorstores import Milvus
from core.pdf_splitter import PdfEngine
from typing import List
from langchain.docstore.document import Document

# 配置Milvus向量数据库
DocumentPath = "./docs/" # 本地知识库地址
VectorDbHost = "localhost" # 向量数据库的host，如果本地部署为localhost
VectorDbPort = "19530" # Milvus的端口，默认为19530
VectorCollectionName = "Inquiry_letter_1"



def get_all_sub_path(source_dir: str = "./docs/", filter_file: str = ""):
    """
    :param source_dir:起始目录
    :param filter_file:取某个后缀的文件，如果没指定则全部都返回
    :return:
    get_all_sub_path 深度遍历目录和子目录并返回文件列表
    """
    path_list = []
    for fpath, dirs, fs in os.walk(source_dir):
        for f in fs:
            p = os.path.join(fpath, f)
            if filter_file != "":
                if p.endswith(filter_file):
                    path_list.append(p)
            else:
                path_list.append(p)

    return path_list

def get_all_file_name(doc_type='问询函',source_dir: str = "./docs/"):
    pdf_files = []
    source_dir += doc_type
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.pdf'):
                pdf_files.append(file.replace('.pdf',''))
    return pdf_files


def create_embeddings(documents: List[Document], collection_name: str = VectorCollectionName):
    embeddings = EMB

    vector_db = Milvus.from_documents(
        documents,
        embeddings,
        connection_args={"host": VectorDbHost, "port": VectorDbPort},
        collection_name=collection_name,
        drop_old=True,
    )
    return vector_db

# 未使用
def incr_embeddings(documents: List[Document]):
    db = get_vector_store()
    index = db.add_documents(documents)
    return index

# 传入向量数据集的名字，返回对应的数据集
# 以"ragpdf"为例，返回应该是向量数据库服务器上对应的"ragpdf"向量库
def get_vector_store(collection_name: str = VectorCollectionName):
    embedding = EMB  # Connect to a milvus instance on localhost
    milvus_store = Milvus(
        embedding_function=embedding,
        collection_name=collection_name,
        connection_args={"host": VectorDbHost, "port": VectorDbPort},
    )
    return milvus_store


def create_vector_store(file_type: str, collection_name: str = VectorCollectionName,):

    pdfFiles = get_all_sub_path(DocumentPath + file_type + '//', ".pdf")
    print(f"------->>>>>> pdf files {len(pdfFiles)} documents")
    documents = PdfEngine.batch_split(pdfFiles)
    print(f"------->>>>>> pdf generate {len(documents)} documents")

    return create_embeddings(documents, collection_name)


def return_raw_file(file_type):
    # pdf
    pdfFiles = get_all_sub_path(DocumentPath + file_type + '//', ".pdf")
    print(f"------->>>>>> pdf files {len(pdfFiles)} documents")
    documents = PdfEngine.return_raw_file(pdfFiles)
    print(f"------->>>>>> pdf generate {len(documents)} documents")

    return documents



