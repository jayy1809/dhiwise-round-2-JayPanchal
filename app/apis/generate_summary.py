from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.config import INDEX_NAME, TRANSCRIPT_DATA_NAMESPACE
from app.services.summary_service import gen_summary

router = APIRouter()


class SummaryRequest(BaseModel):
    agenda: Any


@router.post("/generate_summary")
def gen_summary_details(request: SummaryRequest):
    try:
        summary = gen_summary(
            agenda=request.agenda,
            index_name=INDEX_NAME,
            namespace=TRANSCRIPT_DATA_NAMESPACE,
        )
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
