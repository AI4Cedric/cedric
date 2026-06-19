from pydantic import BaseModel

class ChatRequest(BaseModel):
    provider: str
    prompt: str


class DlpResult(BaseModel):
    risk_score: int
    action: str
    reasons: list[str]


class ChatResponse(BaseModel):
    provider: str
    response: str
    dlp: DlpResult