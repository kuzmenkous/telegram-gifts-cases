from pydantic import BaseModel


class ServerErrorSchema(BaseModel):
    status_code: int
    detail: str
