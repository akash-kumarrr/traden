from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from services.finance_agent import multiagent

from models.user import User
from core.security import get_current_user

router = APIRouter(
    prefix="/agent",
    tags=["finance agent"]
)

class AgentQuery(BaseModel):
    query: str

@router.post("/stream")
async def compare(data: AgentQuery, current_user : User = Depends(get_current_user )):
    async def generate_comparison_response():
        response_stream = await multiagent.arun(data.query, stream=True)
        async for chunk in response_stream:
            if chunk.content:
                yield chunk.content

    return StreamingResponse(
        generate_comparison_response(), 
        media_type="text/plain"
    )