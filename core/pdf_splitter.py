from PyPDF2 import PdfReader
from typing import (List, Tuple)
from langchain.docstore.document import Document
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class PdfEngine:
    def __init__(self, pdf):
        self.pdf = pdf

    # 获取pdf文件内容
    def batch_split(files: List):
        """
        批量遍历指定的文件并进行 markdown 分割，用于进一步embedding
        :param files: 批量文件路径
        :return: 切割后的文件列表[Document]
        """
        all_split_docs: List[Document] = []
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        for file in files:
            pdfText = ""
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages:
                pdfText += page.extract_text()
            splits = text_splitter.split_text(pdfText)
            all_split_docs.extend(splits)
        return text_splitter.create_documents(all_split_docs)

