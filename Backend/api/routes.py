from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from Backend.schemas.models import DatasetInput, ChatInput

router = APIRouter()


@router.post('/datasets')
def upload(records: DatasetInput, request: Request):
    return request.app.state.datasets.replace(records)


@router.get('/datasets/current')
def current(request: Request):
    return request.app.state.datasets.snapshot()


@router.post('/chat')
def chat(body: ChatInput, request: Request):
    if body.stream:
        return StreamingResponse(request.app.state.chat.streaming(body.question), media_type='text/event-stream', headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})
    return request.app.state.chat.complete(body.question)
