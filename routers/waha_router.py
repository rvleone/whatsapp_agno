from fastapi import APIRouter
from workers import tasks


router = APIRouter(prefix="/waha", tags=["WAHA"])

@router.post("/webhook")
async def recieve_whatsapp_message(data: dict) -> dict[str, str]:
    print(data.get("event"))

    event_dispatcher(data)
    return {'status': 'sucess'}

def event_dispatcher(data: dict) -> None:
    event_type = data.get("event")
    if event_type == "message":
        print("FROM:", data['payload']['from'])
        print("MESSAGE:", data['payload']['body'])
        chat_id = data['payload']['from']
        message = data['payload']['body']
        tasks.task_answer.delay(chat_id=chat_id, prompt=message)
    elif event_type == "session.status":
        print("STATUS EVENT:", data['payload']['status'])
    else:
        print(f"Evento: {event_type}")