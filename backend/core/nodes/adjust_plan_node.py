import logging

from core.llm.ollama_llm import llm, plan_parser
from core.prompts.adjust_plan_prompt import get_prompt
from models.schemas.state import StudyState

logger = logging.getLogger(__name__)


def adjust_plan(state: StudyState) -> dict:
    logger.info("adjusting study plan")

    remaining_tasks = [t for t in state.plan.tasks if t.day_number >= state.current_day]
    remaining_days = state.total_days if len(remaining_tasks) == 0 else len(remaining_tasks)
    plan_adjusted = False
    new_tasks = []

    prompt = get_prompt(state.language)
    chain = prompt | llm | plan_parser
    try:
        result = chain.invoke(
            {
                "target": state.target,
                "evaluation": state.check.evaluation,
                "remaining_days": remaining_days,
                "start_day": state.current_day,
                "skills": state.skills,
            }
        )
        new_tasks = result.tasks
        plan_adjusted = True
    except Exception as e:
        logger.error(f"failed to adjust plan: {e}")

    completed_tasks = [t for t in state.plan.tasks if t.day_number < state.current_day]
    if plan_adjusted:
        state.plan.tasks = completed_tasks + new_tasks
        total_days = len(completed_tasks) + len(new_tasks)
    else:
        total_days = state.total_days

    return {"plan": state.plan, "total_days": total_days, "plan_adjusted": plan_adjusted}
