from langchain_core.prompts import PromptTemplate

from core.llm.ollama_llm import final_review_parser

PROMPT_TEMPLATES = {
    "zh": """你是一位严格的技能教练。学员完成了学习计划，请进行最终验收。

## 学习目标
{target}

## 学员学习后反馈
{actual_result}

## 输出格式
{format_instructions}

评估标准：
- 如果学员的反馈表明已经达到学习目标，target_achieved 为 true，diagnosis_detail 给出下一步进阶建议。
- 如果未达到目标，target_achieved 为 false，diagnosis_detail 给出新一轮学习调整方案，包括：
  - 薄弱环节分析
  - 具体改进方向
  - 建议的学习重点
""",
    "en": """You are a strict skill coach. The learner has completed the study plan; please conduct the final review.

## Learning Goal
{target}

## Learner's Post-Study Feedback
{actual_result}

## Output Format
{format_instructions}

Evaluation Criteria:
- If the learner's feedback indicates that the learning goal has been achieved, set target_achieved to true and provide next-step advanced suggestions in diagnosis_detail.
- If the goal has not been achieved, set target_achieved to false and provide a new round of learning adjustment plan in diagnosis_detail, including:
  - Weakness analysis
  - Specific improvement directions
  - Suggested learning focus
""",
}


def get_prompt(language: str) -> PromptTemplate:
    template = PROMPT_TEMPLATES.get(language)
    return PromptTemplate(
        template=template,
        input_variables=["target", "actual_result"],
        partial_variables={"format_instructions": final_review_parser.get_format_instructions()},
    )
