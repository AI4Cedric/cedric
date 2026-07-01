from dotenv import load_dotenv
from dlp import scan_prompt
from dlp.decision import (
    apply_dlp_policy
)
from dlp.restorer import restore_text

import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import (
ChatRequest,
ChatResponse
)

from providers import (
generate_response
)

app = FastAPI(
title="Cedric AI Gateway"
)

app.add_middleware(
CORSMiddleware,
allow_credentials=True,
allow_origins=[
    "https://www.ignixia.fr"
],
allow_methods=["GET", "POST"],
allow_headers=["*"]
)

@app.on_event("startup")
async def startup():
    from dlp.scanner import get_model
    get_model()

@app.get("/health")
async def health():

    return {
        "status": "ok"
    }


@app.post("/chat")
async def chat(
    request: ChatRequest
):
    logger.info(
        "Prompt received: %s",
        request.prompt
    )

    scan = scan_prompt(
        request.prompt
    )

    logger.info(
        "DLP scan: score=%s action=%s patterns=%s categories=%s sensitive_terms=%s entities=%s",
        scan["score"],
        scan["action"],
        scan["patterns"],
        scan["categories"],
        scan.get("sensitive_terms", []),
        scan["entities"],
    )
    
    policy = apply_dlp_policy(
        request.prompt,
        scan
    )

    reasons = (
        scan["patterns"]
        + scan["categories"]
        + [
            t["term"]
            for t in scan.get(
                "sensitive_terms",
                []
            )
        ]
    )

    if not policy["allowed"]:

        return {
            "provider": request.provider,
            "response":
                "Message bloqué par la politique DLP.",
            "dlp": {
                "risk_score":
                    scan["score"],
                "action":
                    "BLOCK",
                "reasons": reasons
            }
        }

    logger.info(
        "Prompt sent to LLM: %s",
        policy["redacted_prompt"]
    )
    
    response = await generate_response(
        request.provider,
        policy["redacted_prompt"]
    )

    logger.info(
        "LLM response: %s",
        response[:500]
    )

    response = restore_text(
        response,
        policy["mapping"]
    )

    logger.info(
        "Restored response: %s",
        response[:500]
    )

    return {
        "provider": request.provider,
        "response": response,
        "dlp": {
            "risk_score":
                scan["score"],
            "action":
                policy["final_action"],
            "reasons": reasons
        }
    }
