from dlp.config import DLP_MODE
from dlp.redactor import redact_text
from dlp.sensitive_redactor import (
    redact_sensitive_terms
)


def apply_dlp_policy(
    prompt: str,
    scan_result: dict
):

    action = scan_result["action"]

    entities = scan_result["entities"]

    score = scan_result["score"]


    if DLP_MODE == "STRICT":

        if action == "BLOCK":

            return {
                "allowed": False,
                "redacted_prompt": None,
                "mapping": {},
                "final_action": "BLOCK"
            }


        return {
            "allowed": True,
            "redacted_prompt": prompt,
            "mapping": {},
            "final_action": action
        }


    if DLP_MODE == "SMART":


        if action == "BLOCK":

            return {
                "allowed": False,
                "redacted_prompt": None,
                "mapping": {},
                "final_action": "BLOCK"
            }


        if score >= 40:

            redacted_prompt, mapping = (
                redact_text(
                    prompt,
                    entities
                )
            )


            redacted_prompt = redact_sensitive_terms(
                redacted_prompt,
                scan_result.get(
                    "sensitive_terms",
                    []
                )
            )


            return {
                "allowed": True,
                "redacted_prompt": redacted_prompt,
                "mapping": mapping,
                "final_action": "REDACT"
            }


        return {
            "allowed": True,
            "redacted_prompt": prompt,
            "mapping": {},
            "final_action": "ALLOW"
        }


    raise ValueError(
        f"Unknown DLP_MODE={DLP_MODE}"
    )
