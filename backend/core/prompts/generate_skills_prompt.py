from langchain_core.prompts import PromptTemplate

from core.llm.ollama_llm import skills_parser

PROMPT_TEMPLATES = {
    "zh": """
你是一位元学习专家。请分析用户的学习目标，完成以下两项任务，并只输出一个JSON对象，不要包含任何额外文字或markdown标记。

## 任务
1. 将目标“{target}”拆解为4-6个核心子技能/动作单元（从易到难）。
2. 为每个子技能生成5个在{platform}上搜索教学视频的精准关键词/动作术语。

## 要求
- 每个子技能恰好5个关键词。
- 每个SearchResult的keyword要具体、可搜索，如"雅思听力 填空题 技巧"而不是"听力"。
- resources字段保持为空数组[]。

## 输出格式
{format_instructions}
""",
    "en": """
You are a meta-learning expert. Analyze the user's learning goal, complete the following two tasks, and output only one JSON object without any extra text or markdown markers.

## Tasks
1. Break down the goal "{target}" into 4-6 core sub-skills/action units (from easy to difficult).
2. For each sub-skill, generate 5 precise keywords/action terms for searching instructional videos on {platform}.

## Requirements
- Each sub-skill must have exactly 5 keywords.
- Each SearchResult's keyword should be specific and searchable, such as "IELTS listening fill-in-the-blank techniques" instead of just "listening".
- Keep the resources field as an empty array [].

## Output Format
{format_instructions}
""",
}


def get_prompt(language: str) -> PromptTemplate:
    template = PROMPT_TEMPLATES.get(language)
    return PromptTemplate(
        template=template,
        input_variables=["target", "platform"],
        partial_variables={"format_instructions": skills_parser.get_format_instructions()},
    )
