import logging

from core.llm.ollama_llm import llm, plan_parser
from core.prompts.generate_plan_prompt import get_prompt
from models.schemas.state import StudyState

logger = logging.getLogger(__name__)


def generate_plan(state: StudyState) -> dict:
    logger.info("generating study plan")
    plan = None
    prompt = get_prompt(state.language)
    chain = prompt | llm | plan_parser
    try:
        result = chain.invoke(
            {
                "target": state.target,
                "target_type": state.target_type.value,
                "current_stage": state.current_stage,
                "daily_study_time": state.daily_study_time,
                "total_days": state.total_days,
                "platform": state.platform,
                "skills": state.skills,
            }
        )
        plan = result
        logger.info(f"generated plan successfully: {plan}")
    except Exception as e:
        logger.error(f"generated plan failed: {e}")

    return {"plan": plan, "current_day": 1}
