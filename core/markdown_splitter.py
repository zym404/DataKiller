from typing import (List, Tuple)
from langchain.document_loaders import TextLoader
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain.docstore.document import Document


class MarkdownHeaderSplitter(object):
    @classmethod
    def batch_split(cls, files: List):
        """
        批量遍历指定的文件并进行 markdown 分割，用于进一步embedding
        :param files: 批量文件路径
        :return: 切割后的文件列表[Document]
        """
        all_split_docs: List[Document] = []
        headers_to_split_on = [
            ("#", "Header_1"),
            ("##", "Header_2"),
            ("###", "Header_3"),
        ]
        for file in files:
            loader = TextLoader(file)
            document = loader.load()
            split_docs = cls.split_single_v2(
                document=document[0],
                headers_to_split_on=headers_to_split_on
            )
            all_split_docs.extend(split_docs)
        return all_split_docs

    @classmethod
    def split_single_v2(cls, headers_to_split_on: List[Tuple[str, str]], document: Document):
        """
        将一篇 markdown 格式文章进行分割处理
        :param document: 一篇完整的 markdown 文章
        :param headers_to_split_on: 分割的层级
        :return: [Document]列表
        """
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        docs = markdown_splitter.split_text(document.page_content)
        # 规范化处理document的 metadata，因为会作为milvus的表字段存入
        for doc in docs:
            meta_data = document.metadata.copy()
            cls.add_header_info_to_content(
                document=doc,
                meta_data=meta_data,
                headers_to_split_on=headers_to_split_on)
        return docs

    @classmethod
    def add_header_info_to_content(cls, document: Document, meta_data: dict,
                                   headers_to_split_on: List[Tuple[str, str]]):
        content = document.page_content
        for header in headers_to_split_on:
            header_key = header[1]
            header_val = document.metadata.get(header_key, "")
            meta_data[header_key] = header_val  # 设置到 metadata 中
            content = f"{header_val}\t{content}"  # 拼接到内容中
        document.page_content = content
        document.metadata = meta_data
        return document