import logging

from core.llm.ollama_llm import llm
from core.prompts.generate_quiz_prompt import get_prompt
from models.schemas.state import Check, StudyState

logger = logging.getLogger(__name__)


def generate_quiz(state: StudyState) -> dict:
    logger.info(f"generating quiz for day {state.current_day}")

    learned_tasks = [t for t in state.plan.tasks if t.day_number <= state.current_day]
    learned_text = "\n".join([f"第{t.day_number}天「{t.title}」: {t.content}\n" for t in learned_tasks])

    checklist = ""
    prompt = get_prompt(state.language)
    chain = prompt | llm
    try:
        response = chain.invoke({"target": state.target, "learned_content": learned_text})
        checklist = response.content.strip()
    except Exception as e:
        logger.error(f"generated quiz failed: {e}")

    check = Check(day_number=state.current_day, checklist=checklist)
    return {"check": check}
