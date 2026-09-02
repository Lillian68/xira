import logging

from core.llm.ollama_llm import llm, skills_parser
from core.prompts.generate_skills_prompt import get_prompt
from models.schemas.state import StudyState

logger = logging.getLogger(__name__)


def generate_skills(state: StudyState) -> dict:
    logger.info("generating skills")
    prompt = get_prompt(state.language)
    chain = prompt | llm | skills_parser

    skills = []
    try:
        result = chain.invoke({"target": state.target, "platform": state.platform})
        skills = result.skills
        logger.info(f"generated {len(skills)} skills: {[s.name for s in skills]}")
    except Exception as e:
        logger.error(f"generated skills failed: {e}")

    return {"skills": skills}
