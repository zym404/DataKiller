from langchain_core.pydantic_v1 import BaseModel, Field

# class _StructualInquiryLetter(BaseModel):
#     监管问题: str = Field(description='证券交易所问询函中披露的上市公司存在的关注事项和监管问题，需要上市公司做出回复说明')
#     公司答复: str = Field(description='上市公司就监管问题做出的回复，简明扼要')
#     涉及主体: str = Field(description='')
#     涉及财报科目: str = Field(description='监管问题涉及的财报科目，该科目为上市公司会计准则中规定的会计科目')
#     涉及金额: str = Field(description='监管问题中涉及的金额')
#     公司名称: str = Field(description='公司的名称，为工商信息登记的全称')
#     证券代码: str = Field(description='上市公司的证券代码')
#     公告日期: str = Field(description='问询函的发布日期')
    

# class StructualInquiryLetter(BaseModel):
#     列表: list[_StructualInquiryLetter] = Field(description='所有监管问题的列表')

class _StructualInquiryLetter(BaseModel):
    
    监管问题: str = Field(description='概括需要公司说明的监管问题')
    监管问题背景: str = Field(description='需要公司说明的监管问题的背景')
    需要问询公司的具体方面: str = Field(description='每个监管问题需要问询公司的具体方面，是一个list')
    问询事项: str = Field(description='大的问询事项，如资产重组、关联交易等')
    问询机构: str = Field(description='证券交易所名称，只能为"上海证券交易所"或"深圳证券交易所"')
    函件类别: str = Field(description='函件的类别')
    公司名称: str = Field(description='公司的名称，为工商信息登记的全称')
    证券代码: str = Field(description='上市公司的证券代码')
    公告日期: str = Field(description='证券交易所发布函件的日期，请把日期转换为阿拉伯数字')
    


class StructualInquiryLetter(BaseModel):
    列表: list[_StructualInquiryLetter] = Field(description='所有监管问题的列表')