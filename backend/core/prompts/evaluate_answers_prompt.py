from langchain_core.prompts import PromptTemplate

from core.llm.ollama_llm import evaluation_parser

PROMPT_TEMPLATES = {
    "zh": """你是一位严格的技能教练。学员完成了以下检验：

## 检验内容
{checklist}

## 学员反馈的成绩
{user_feedback}

## 学习目标
{target}

## 输出格式
{format_instructions}

评估标准：
- 如果所有部分都达到通过标准，passed 为 true。
- 如果有部分未达标，passed 为 false，并在 evaluation 中指出薄弱环节和改进建议。
- evaluation 要具体、可执行，不要泛泛而谈。
""",
    "en": """You are a strict skill coach. The learner has completed the following assessment:

## Assessment Content
{checklist}

## Learner's Reported Results
{user_feedback}

## Learning Goal
{target}

## Output Format
{format_instructions}

Evaluation Criteria:
- If all parts meet the passing standard, set passed to true.
- If any part does not meet the standard, set passed to false and point out weak areas and improvement suggestions in evaluation.
- The evaluation should be specific and actionable, not vague.
""",
}


def get_prompt(language: str) -> PromptTemplate:
    template = PROMPT_TEMPLATES.get(language)
    return PromptTemplate(
        template=template,
        input_variables=["target", "checklist", "user_feedback"],
        partial_variables={"format_instructions": evaluation_parser.get_format_instructions()},
    )
