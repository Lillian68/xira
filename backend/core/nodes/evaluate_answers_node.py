import logging

from core.llm.ollama_llm import evaluation_parser, llm
from core.prompts.evaluate_answers_prompt import get_prompt
from models.schemas.state import StudyState

logger = logging.getLogger(__name__)


def evaluate_answers(state: StudyState) -> dict:
    logger.info("generating evaluations")

    passed = False
    evaluation = ""

    prompt = get_prompt(state.language)
    chain = prompt | llm | evaluation_parser
    try:
        result = chain.invoke(
            {"checklist": state.check.checklist, "user_feedback": state.check.assessment, "target": state.target}
        )
        passed = result.passed
        evaluation = result.evaluation
        logger.info(f"evaluated successfully: passed={passed}, evaluation={evaluation}")
    except Exception as e:
        logger.error(f"evaluated failed: {e}")

    state.check.evaluation = evaluation
    state.check.passed = passed
    return {"check": state.check}
