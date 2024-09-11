from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime


class UrlCreateSchema(BaseModel):
    url: HttpUrl = Field(..., example="http://example.com")


class UrlCreateResponseSchema(UrlCreateSchema):
    id: int = Field(...)
    short_code: str = Field(...)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)

    class Config:
        orm_mode = True


class UrlStatsResponseSchema(UrlCreateResponseSchema):
    access_count: int = Field(...)
