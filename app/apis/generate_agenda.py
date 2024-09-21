from typing import Any, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.config import INDEX_NAME, MEETING_DATA_NAMESPACE
from app.services.agenda_service import gen_agenda

router = APIRouter()


class DiscussionData(BaseModel):
    name: str
    department: str
    discussion_points: Any


class AgendaRequest(BaseModel):
    discussion_data: List[DiscussionData]


@router.post("/generate_agenda")
def gen_agenda_details(request: AgendaRequest):
    try:
        print("hello")
        agenda = gen_agenda(
            discussion_data=request.discussion_data,
            index_name=INDEX_NAME,
            namespace=MEETING_DATA_NAMESPACE,
        )
        return {"agenda": agenda}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
