from pydantic import BaseModel


class DocsCreate(BaseModel):
    name: str
    content: str
    referrals: str
