from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime


class UrlCreateSchema(BaseModel):
    url: HttpUrl = Field(..., example="http://example.com")


class UrlResponseSchema(UrlCreateSchema):
    id: int = Field(...)
    short_code: str = Field(...)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)

    class Config:
        orm_mode = True


class UrlStatsResponseSchema(UrlResponseSchema):
    access_count: int = Field(...)
