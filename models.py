from pydantic import BaseModel

class WebsiteRequest(BaseModel):
    website: str

class SearchRequest(BaseModel):
    query: str