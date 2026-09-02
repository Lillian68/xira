import logging

from core.llm.ollama_llm import llm
from core.prompts.daily_checkin_prompt import get_prompt
from models.schemas.state import StudyState

logger = logging.getLogger(__name__)


def daily_checkin(state: StudyState) -> dict:
    logger.info(f"processing day {state.current_day} check-in")
    current_task = None
    for task in state.plan.tasks:
        if task.day_number == state.current_day:
            current_task = task
            break
    task_content = current_task.content if current_task else "学习任务"
    task_content = task_content[:100] + "..." if len(task_content) > 100 else task_content
    is_last_day = state.current_day == state.total_days
    if is_last_day:
        next_info = "这是最后一天，完成后将进行最终验收，你已经走完了全程！"
    else:
        next_task = None
        for t in state.plan.tasks:
            if t.day_number == state.current_day + 1:
                next_task = t
                break
        next_info = f"明天主题：{next_task.title if next_task else '继续学习'}"

    prompt = get_prompt(state.language)
    chain = prompt | llm
    try:
        response = chain.invoke(
            {
                "day": state.current_day,
                "task_title": current_task.title if current_task else "学习任务",
                "task_content": task_content,
                "next_info": next_info,
            }
        )
        feedback = response.content.strip()
    except Exception as e:
        logger.error(f"generated feedback failed: {e}")
        feedback = "太棒了！你又做到了！每一步都算数！明天继续加油 💪"

    return {"current_day": state.current_day + 1, "messages": [{"role": "assistant", "content": feedback}]}
