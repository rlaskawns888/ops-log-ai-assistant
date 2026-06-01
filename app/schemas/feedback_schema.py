from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

class FeedbackType(str, Enum):
    HELPFUL="HELPFUL"
    NOT_HELPFUL="NOT_HELPFUL"
    INACCURATE="INACCURATE"
    DANGROUS="DANGROUS"

class FeedbackCreateRequest(BaseModel):
    result_id: int = Field(..., alias="resultId")
    feedback_type: FeedbackType = Field(..., alias="feedbackType")
    comment: Optional[str] = None

    class Config:
        poplulate_by_name = True

class FeedbackCreateResponse(BaseModel):
    feedback_id: int = Field(..., alais="feedbackId")
    result_id: int = Field(..., alias="resultId")
    feedback_type: FeedbackType = Field(..., alias="feedbackType")
    comment: Optional[str] = None
    created_ad: datetime = Field(..., alias="createdAt")

    #Pydantic v2에서 “데이터를 어떻게 채우고, 객체를 어떻게 응답 모델로 바꿀지” 정하는 설정
    class Config:
        populate_by_name = True #alias와 실제 필드명 둘 다 허용
        from_attributes = True #SQLAlchemy 객체 같은 일반 객체의 속성을 읽어서 Pydantic 모델로 변환 가능
  
# Pydantic v1
# class Config:
#     allow_population_by_field_name = True
#     orm_mode = True