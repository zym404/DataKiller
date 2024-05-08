from langchain_core.pydantic_v1 import BaseModel, Field


class _StructualInquiryLetter(BaseModel):
    监管问题: str = Field(description='概括需要公司说明的监管问题')
    监管问题背景: str = Field(description='需要公司说明的监管问题的背景')
    需要问询公司的具体方面: str = Field(description='每个监管问题需要问询公司的具体方面，是一个list')
    
    
class StructualInquiryLetter(BaseModel):
    列表: list[_StructualInquiryLetter] = Field(description='所有监管问题的列表')
    问询函主题: str = Field(description='问询函的主旨摘要，格式：“关于XXXX公司XX问题的问询函”')
    问询机构: str = Field(description='证券交易所名称，只能为"上海证券交易所"或"深圳证券交易所"')
    函件类别: str = Field(description='函件的类别')
    公司名称: str = Field(description='公司的名称，为工商信息登记的全称')
    证券代码: str = Field(description='上市公司的证券代码')
    公告日期: str = Field(description='证券交易所发布函件的日期，请把日期转换为阿拉伯数字')
    几日内回复: str = Field(description='证券交易所要求几日内进行回复，上海证券交易所特有')
    截止到哪天之前回复: str = Field(description='证券交易所要求截至到哪天之前进行回复，深圳证券交易所特有')


# class _StructualInquiryLetter(BaseModel):
#     监管问题内容: str = Field(description='监管问题的具体内容')
#     监管问题概括: str = Field(description='概括一下监管问题的内容')
#     补充披露: str = Field(description='需要公司补充、披露、说明的事项，是一个list')
#     问询科目: str = Field(description='问询函的涉及的会计科目')
    
# class StructualInquiryLetter(BaseModel):
#     列表: list[_StructualInquiryLetter] = Field(description='所有监管问题的列表')
#     问询机构: str = Field(description='证券交易所名称')
#     函件类别: str = Field(description='函件的类别')
#     # 函件编号: str = Field(description='函件的编号')
#     公司名称: str = Field(description='公司的名称，为工商信息登记的全称,请注意全称的格式为“XXX股份有限公司”')
#     公告日期: str = Field(description='证券交易所发布函件的日期，格式为“YYYY年MM月DD日”')
#     # 几日内回复: str = Field(description='证券交易所要求几日内进行回复，上海证券交易所特有')
#     回复截止日期: str = Field(description='公司做出回复的截止日期，格式为“YYYY年MM月DD日”')


class TaggingInquiryLetter(BaseModel):
    监管问题: str = Field(description='概括需要公司说明的监管问题')
    监管问题背景: str = Field(description='需要公司说明的监管问题的背景')
    需要问询公司的具体方面: str = Field(description='每个监管问题需要问询公司的具体方面，是一个list')
    严重性程度: str = Field(description='监管问题严重程度')
    # 监管问题类别: str = Field(description='监管问题的类别')
    # 问询科目: str = Field(description='问询函的涉及的会计科目')
    判断过程: str = Field(description='判断监管问题严重程度的过程')
    问询函主题: str = Field(description='问询函的主旨摘要，格式：“关于XXXX公司XX问题的问询函”')
    问询机构: str = Field(description='证券交易所名称，只能为"上海证券交易所"或"深圳证券交易所"')
    函件类别: str = Field(description='函件的类别')
    公司名称: str = Field(description='公司的名称，为工商信息登记的全称')
    证券代码: str = Field(description='上市公司的证券代码')
    公告日期: str = Field(description='证券交易所发布函件的日期，请把日期转换为阿拉伯数字')
    几日内回复: str = Field(description='证券交易所要求几日内进行回复，上海证券交易所特有')
    截止到哪天之前回复: str = Field(description='证券交易所要求截至到哪天之前进行回复，深圳证券交易所特有')