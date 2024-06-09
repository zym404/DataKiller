from langchain_core.pydantic_v1 import BaseModel, Field

    
class TaggingInquiryLetter(BaseModel):
    # 标签: str = Field(description='业务标签')
    标签结果: str = Field(description='业务标签的判断结果')
    判断依据: str = Field(description='业务标签的判断依据')
    原文引用: str = Field(description='业务标签判断依据的原文引用')
