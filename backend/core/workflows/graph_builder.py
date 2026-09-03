from langgraph.graph import END, StateGraph

from core.nodes.adjust_plan_node import adjust_plan
from core.nodes.daily_checkin_node import daily_checkin
from core.nodes.evaluate_answers_node import evaluate_answers
from core.nodes.final_review_node import final_review
from core.nodes.generate_plan_node import generate_plan
from core.nodes.generate_quiz_node import generate_quiz
from core.nodes.generate_skills_node import generate_skills
from core.nodes.search_node import search
from models.schemas.state import StudyState


def build_graph(checkpointer):
    builder = StateGraph(StudyState)

    builder.add_node("generate_skills", generate_skills)
    builder.add_node("search", search)
    builder.add_node("generate_plan", generate_plan)
    builder.add_node("daily_checkin", daily_checkin)
    builder.add_node("generate_quiz", generate_quiz)
    builder.add_node("evaluate_answers", evaluate_answers)
    builder.add_node("adjust_plan", adjust_plan)
    builder.add_node("final_review", final_review)

    builder.set_entry_point("generate_skills")
    builder.add_edge("generate_skills", "search")
    builder.add_edge("search", "generate_plan")
    builder.add_edge("generate_plan", "daily_checkin")

    def after_checkin(state: StudyState):
        completed_day = state.current_day - 1
        if completed_day >= state.total_days:
            if state.check_interval > 0 and completed_day % state.check_interval == 0:
                return "generate_quiz"
            else:
                return "final_review"
        elif completed_day > 0 and completed_day % state.check_interval == 0:
            return "generate_quiz"
        else:
            return "daily_checkin"

    builder.add_conditional_edges(
        "daily_checkin",
        after_checkin,
        {"final_review": "final_review", "generate_quiz": "generate_quiz", "daily_checkin": "daily_checkin"},
    )
    builder.add_edge("generate_quiz", "evaluate_answers")

    def after_evaluate(state):
        if not state.check.passed:
            return "adjust_plan"
        if state.current_day - 1 >= state.total_days:
            return "final_review"
        return "daily_checkin"

    builder.add_conditional_edges(
        "evaluate_answers",
        after_evaluate,
        {
            "adjust_plan": "adjust_plan",
            "final_review": "final_review",
            "daily_checkin": "daily_checkin",
        },
    )
    builder.add_edge("adjust_plan", "daily_checkin")

    def after_review(state: StudyState):
        return END if state.result.target_achieved else "adjust_plan"

    builder.add_conditional_edges("final_review", after_review, {"adjust_plan": "adjust_plan", END: END})

    return builder.compile(
        checkpointer=checkpointer, interrupt_before=["daily_checkin", "evaluate_answers", "final_review"]
    )
