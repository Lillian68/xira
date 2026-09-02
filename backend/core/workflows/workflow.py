import logging
from datetime import datetime

from core.llm.ollama_llm import llm
from models.schemas.state import Check, Plan, Result, StudyState

logger = logging.getLogger(__name__)


class Workflow:
    def __init__(self, graph):
        self.graph = graph

    def generate_plan(self, workflow_id: str, interview: dict) -> Plan:
        start_str = interview.get("start_date")
        end_str = interview.get("end_date")

        if start_str and end_str:
            start_date = datetime.fromisoformat(start_str)
            end_date = datetime.fromisoformat(end_str)
            total_days = (end_date - start_date).days + 1
        else:
            total_days = 0

        config = {"configurable": {"thread_id": workflow_id}}
        initial_state = StudyState(
            target=interview.get("target"),
            target_type=interview.get("target_type"),
            current_stage=interview.get("current_stage"),
            daily_study_time=int(interview.get("daily_minutes")),
            total_days=total_days,
            check_interval=int(interview.get("check_interval_days")),
            platform=interview.get("platform"),
            language=interview.get("language"),
        )

        self.graph.invoke(initial_state, config)
        current_state = self.graph.get_state(config)
        vals = current_state.values
        return vals.get("plan")

    def spirit_dialogue(self, workflow_id: str) -> str:
        config = {"configurable": {"thread_id": workflow_id}}
        self.graph.invoke(None, config)
        current_state = self.graph.get_state(config)
        vals = current_state.values
        messages = vals.get("messages")
        for msg in messages:
            if msg["role"] == "assistant":
                return msg["content"]

        return ""

    def generate_exam(self, workflow_id: str) -> str:
        config = {"configurable": {"thread_id": workflow_id}}
        current_state = self.graph.get_state(config)
        vals = current_state.values
        check = vals.get("check")
        if not check:
            raise ValueError("Checklist not ready yet")
        return check.checklist

    def evaluate_practice(self, workflow_id: str, submission: str) -> Check:
        config = {"configurable": {"thread_id": workflow_id}}
        current_state = self.graph.get_state(config)
        vals = current_state.values
        check = vals.get("check")
        check.assessment = submission
        self.graph.update_state(config, {"check": check})
        self.graph.invoke(None, config)
        current_state = self.graph.get_state(config)
        vals = current_state.values
        check = vals.get("check")
        return check

    def remedial_analysis(self, workflow_id: str, actual_result: str) -> Result:
        config = {"configurable": {"thread_id": workflow_id}}
        current_state = self.graph.get_state(config)
        vals = current_state.values
        result = Result()
        result.actual_result = actual_result
        self.graph.update_state(config, {"result": result})
        self.graph.invoke(None, config)
        current_state = self.graph.get_state(config)
        vals = current_state.values
        result = vals.get("result")
        return result

    def spirit_chat(self, content: str):
        resp = llm.invoke([{"role": "user", "content": content}])
        return resp.content

    def adjust_plan(self, workflow_id: str) -> Plan:
        plan = None
        config = {"configurable": {"thread_id": workflow_id}}
        current_state = self.graph.get_state(config)
        vals = current_state.values
        plan_adjusted = bool(vals.get("plan_adjusted"))
        if not plan_adjusted:
            raise ValueError("Plan not adjusted yet")
        plan = vals.get("plan")
        self.graph.update_state(config, {"plan_adjusted": False})
        return plan
