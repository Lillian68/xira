from langchain_core.prompts import PromptTemplate

PROMPT_TEMPLATES = {
    "zh": """你是一位技能教练。学员的学习目标是：{target}

学员已经学习了以下内容：
{learned_content}

请设计阶段检验。**根据目标自动判断检验方式**：
- 如果是语言考试（雅思、托福、四六级），推荐具体真题套题和在线练习平台。
- 如果是翻译考试（CATTI、MTI），推荐翻译真题段落。
- 如果是编程学习，推荐实际项目或算法题。
- 如果是运动/乐器，设计动作自测清单。

## 检验设计原则
1. **真题明确**：指定具体套题（如"剑桥雅思15 Test 2"）。
2. **推荐平台**：推荐可以做题并自动批改的网站/APP（如雅思哥、新东方雅思、剑桥官方模考、LeetCode等）。
3. **覆盖已学内容**：检验应覆盖学员学过的所有子技能。

## 输出格式
### [子技能1]
- **真题**：具体套题
- **平台**：推荐在哪里做（网站/APP）

### [子技能2]
...

### 反馈要求
完成后请反馈：
- 各部分的正确率/分数
- 错题类型（如果有）
- 时间是否够用

## 示例（雅思）
### 听力
- **真题**：剑桥雅思15 Test 2 听力 Section 1-2
- **平台**：雅思哥APP 或 新东方雅思网

### 阅读
- **真题**：剑桥雅思15 Test 2 阅读 Passage 1
- **平台**：雅思哥APP
""",
    "en": """You are a skill coach. The learner's goal is: {target}

The learner has already studied the following content:
{learned_content}

Please design a stage assessment. **Automatically determine the assessment method based on the goal**:
- For language exams (IELTS, TOEFL, CET-4/6), recommend specific past papers and online practice platforms.
- For translation exams (CATTI, MTI), recommend translation passages from past exams.
- For programming learning, recommend practical projects or algorithm problems.
- For sports/music, design a self-check checklist.

## Assessment Design Principles
1. **Specific past papers**: Specify the exact test set (e.g., "Cambridge IELTS 15 Test 2").
2. **Recommended platforms**: Recommend websites/apps where the learner can practice and get automatic grading (e.g., IELTS Online Tests, British Council practice platform, Cambridge official mock tests, LeetCode, etc.).
3. **Cover all learned content**: The assessment should cover all sub-skills the learner has studied.

## Output Format
### [Sub-skill 1]
- **Past Paper**: specific test set
- **Platform**: where to practice (website/app)

### [Sub-skill 2]
...

### Feedback Requirements
After completing, please provide feedback on:
- Accuracy/score for each part
- Types of mistakes (if any)
- Whether time was sufficient

## Example (IELTS)
### Listening
- **Past Paper**: Cambridge IELTS 15 Test 2 Listening Sections 1-2
- **Platform**: IELTS Online Tests or British Council practice platform

### Reading
- **Past Paper**: Cambridge IELTS 15 Test 2 Reading Passage 1
- **Platform**: IELTS Online Tests
""",
}


def get_prompt(language: str) -> PromptTemplate:
    template = PROMPT_TEMPLATES.get(language)
    return PromptTemplate(
        template=template,
        input_variables=["target", "learned_content"],
    )
