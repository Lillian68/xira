from langchain_core.prompts import PromptTemplate

from core.llm.ollama_llm import plan_parser

PROMPT_TEMPLATES = {
    "zh": """你是一位全球顶级技能教练与元学习专家。基于以下信息生成自学计划。

## 用户信息
- 学习目标：{target}
- 目标类型：{target_type}
- 当前基础：{current_stage}
- 每日可用时间：{daily_study_time}分钟
- 总学习天数：{total_days}天
- 平台：{platform}

## 子技能及可用资源
{skills}

## 要求
1. 计划必须覆盖上述所有子技能，每个子技能至少安排1天。
2. 避免连续2天以上都是同一子技能。
3. 每天围绕一个子技能设计主题，content包含：
   - 当天学习主题
   - 观看视频（从对应子技能的资源中选，注明预计时长）
   - 刻意练习/笔记/输出
   - 时间分配（≤{daily_study_time}分钟）
4. resources不能为空：每个任务的resources必须至少包含1个视频，从上面JSON中对应子技能的resources数组中选取。
5. 每个资源对象必须包含且仅包含以下字段：title、url、snippet、platform。这些字段的值必须与JSON中提供的完全一致，不得修改、缩写或编造。
6. 如果某个子技能确实没有可用资源，不要为该子技能安排任务，改为安排其他有资源的子技能。
7. 只返回JSON，格式：{format_instructions}
""",
    "en": """You are a world-class skill coach and meta-learning expert. Generate a self-study plan based on the following information.

## User Information
- Learning Goal: {target}
- Goal Type: {target_type}
- Current Level: {current_stage}
- Daily Study Time: {daily_study_time} minutes
- Total Days: {total_days} days
- Platform: {platform}

## Sub-skills and Available Resources
{skills}

## Requirements
1. The plan must cover all sub-skills listed above. Each sub-skill must be scheduled for at least 1 day.
2. Avoid scheduling the same sub-skill for more than 2 consecutive days.
3. Each day should focus on one sub-skill. The "content" field must include:
   - Daily learning topic
   - Video to watch (select from the resources of the corresponding sub-skill, note the estimated duration)
   - Deliberate practice / notes / output
   - Time allocation (≤ {daily_study_time} minutes)
4. "resources" cannot be empty: each task's resources must include at least 1 video, selected from the resources array of the corresponding sub-skill in the JSON above.
5. Each resource object must contain exactly the following fields: title, url, snippet, platform. Their values must be identical to those provided in the JSON. Do not modify, abbreviate, or fabricate.
6. If a sub-skill truly has no available resources, do not schedule tasks for that sub-skill; schedule other sub-skills that have resources instead.
7. Return only JSON in the following format: {format_instructions}
""",
}


def get_prompt(language: str) -> PromptTemplate:
    template = PROMPT_TEMPLATES.get(language)
    return PromptTemplate(
        template=template,
        input_variables=[
            "target",
            "target_type",
            "current_stage",
            "daily_study_time",
            "total_days",
            "platform",
            "skills",
        ],
        partial_variables={"format_instructions": plan_parser.get_format_instructions()},
    )
