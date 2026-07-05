from pydantic import BaseModel

class RunRequest(BaseModel):
    message: str
    

class EventRequest(BaseModel):
    event: str