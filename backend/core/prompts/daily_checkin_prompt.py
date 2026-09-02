from langchain_core.prompts import PromptTemplate

PROMPT_TEMPLATES = {
    "zh": """你是一位充满热情的学习教练，擅长用真诚、具体、有能量的语言鼓励学员。

学员今天完成了第{day}天的学习任务：
- 任务主题：{task_title}
- 任务内容：{task_content}
- 明天安排：{next_info}

请给学员一段鼓励（30-60字），要求：
1. 具体提到今天完成的任务内容，不要泛泛而谈
2. 用比喻或画面感的语言
3. 语气真诚、有能量，像朋友一样，不要官方套话
4. 可以适当使用emoji
5. 结尾可以自然地衔接明天的任务

示例：
"太棒了！今天你攻克了雅思听力的填空题技巧，那些曾经让你头疼的数字和地名，现在已经开始变得听话了。明天我们继续乘胜追击，向选择题发起挑战！"
""",
    "en": """You are an enthusiastic learning coach, skilled at encouraging students with sincere, specific, and energetic language.

The student completed the learning task for Day {day} today:
- Task Title: {task_title}
- Task Content: {task_content}
- Tomorrow's Plan: {next_info}

Please give the student a short encouraging message (30-60 words), requirements:
1. Specifically mention the task content completed today, avoid generic praise
2. Use metaphors or vivid imagery
3. Sincere, energetic, like a friend, not official clichés
4. You may use emojis appropriately
5. Naturally connect to tomorrow's task at the end

Example:
"Awesome! Today you conquered the IELTS listening fill-in-the-blank techniques. Those numbers and place names that once gave you headaches are now starting to behave. Tomorrow let's keep the momentum and tackle the multiple choice questions!"
""",
}


def get_prompt(language: str) -> PromptTemplate:
    template = PROMPT_TEMPLATES.get(language)
    return PromptTemplate(
        template=template,
        input_variables=["day", "task_title", "task_content", "next_info"],
    )
