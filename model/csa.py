from pydantic import BaseModel

from typing import List


class QueryRequest(BaseModel):
    query: str


class QueryDetails(BaseModel):
    vector_size: int
    results_found: int
    collection_name: str


class QueryResponse(BaseModel):
    status: str
    text_response: str
    sources: List[str]
    query_details: QueryDetails
