from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from services.finance_agent import multiagent

router = APIRouter(
    prefix="/agent",
    tags=["finance agent"]
)

class AgentQuery(BaseModel):
    query: str

@router.post("/stream")
async def compare(data: AgentQuery):
    async def generate_comparison_response():
        response_stream = await multiagent.arun(data.query, stream=True)
        async for chunk in response_stream:
            if chunk.content:
                yield chunk.content

    return StreamingResponse(
        generate_comparison_response(), 
        media_type="text/plain"
    )