import logging

from core.tools.searxng_tool import search_study_resources
from models.schemas.state import StudyState

logger = logging.getLogger(__name__)


def search(state: StudyState) -> StudyState:
    logger.info("searching study resources")
    for skill in state.skills:
        for sr in skill.search_results:
            resources = search_study_resources.invoke({"keyword": sr.keyword, "platform": state.platform})
            if isinstance(resources, list):
                sr.resources = resources
            else:
                sr.resources = []
            logger.info(f"skill={skill.name}, keyword={sr.keyword}, found {len(sr.resources)} resources")

    return {"skills": state.skills}
