from pydantic import BaseModel


class GDPRDeletionEvent(BaseModel):
    user_id: str
    request_time: str
    request_id: str
# Event definitions (optional)
