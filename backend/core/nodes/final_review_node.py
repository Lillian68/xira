import logging

from core.llm.ollama_llm import final_review_parser, llm
from core.prompts.final_review_prompt import get_prompt
from models.schemas.state import StudyState

logger = logging.getLogger(__name__)


def final_review(state: StudyState) -> dict:
    logger.info("starting final review")

    target_achieved = False
    diagnosis_detail = ""

    prompt = get_prompt(state.language)
    chain = prompt | llm | final_review_parser
    try:
        result = chain.invoke({"target": state.target, "actual_result": state.result.actual_result})
        target_achieved = result.target_achieved
        diagnosis_detail = result.diagnosis_detail
        logger.info(f"final review succeeded: target_achieved={target_achieved}, diagnosis_detail={diagnosis_detail}")
    except Exception as e:
        logger.error(f"final review failed: {e}")

    state.result.target_achieved = target_achieved
    state.result.diagnosis_detail = diagnosis_detail
    return {"result": state.result}
