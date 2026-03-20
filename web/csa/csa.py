from fastapi import APIRouter, HTTPException
import service.csa.csa as service
from model.csa import QueryRequest, QueryResponse

# from typing import Any

# from error import Missing

router = APIRouter(prefix="/csa")


@router.post("/query", status_code=201, response_model=QueryResponse)
async def process_query(request: QueryRequest):
    try:
        return await service.process_query(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
