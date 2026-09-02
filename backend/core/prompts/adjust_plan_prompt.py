from langchain_core.prompts import PromptTemplate

from core.llm.ollama_llm import plan_parser

PROMPT_TEMPLATES = {
    "zh": """阶段检验未通过，需要调整后续学习计划。

## 学习目标
{target}

## 薄弱点评价
{evaluation}

## 剩余天数
{remaining_days}

## 可用资源
{skills}

## 要求
1. 针对薄弱点强化学习。
2. 重新设计后续{remaining_days}天的学习任务。
3. 每个任务必须包含：
   - day_number：从{start_day}开始连续递增
   - title：任务标题（注明属于哪个子技能）
   - content：详细学习内容和步骤，包括观看视频、刻意练习、时间分配
   - resources：从上面"可用资源"中选取，title 和 url 必须完全一致，禁止编造
4. resources 不能为空，每个任务至少1个视频。
5. 如果薄弱点对应的子技能没有资源，安排其他有资源的子技能。

{format_instructions}""",
    "en": """The stage assessment was not passed, so the subsequent study plan needs to be adjusted.

## Learning Goal
{target}

## Weakness Evaluation
{evaluation}

## Remaining Days
{remaining_days}

## Available Resources
{skills}

## Requirements
1. Strengthen learning on weak points.
2. Redesign the learning tasks for the next {remaining_days} days.
3. Each task must include:
   - day_number: starts from {start_day} and increases sequentially
   - title: task title (indicating which sub-skill it belongs to)
   - content: detailed learning content and steps, including watching videos, deliberate practice, and time allocation
   - resources: selected from the "Available Resources" above; title and url must be exactly the same, no fabrication
4. resources cannot be empty; each task must include at least 1 video.
5. If the sub-skill corresponding to the weakness has no resources, schedule other sub-skills that have resources.

{format_instructions}""",
}


def get_prompt(language: str) -> PromptTemplate:
    template = PROMPT_TEMPLATES.get(language)
    return PromptTemplate(
        template=template,
        input_variables=["target", "evaluation", "remaining_days", "start_day", "skills"],
        partial_variables={"format_instructions": plan_parser.get_format_instructions()},
    )
