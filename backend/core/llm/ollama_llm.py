from langchain_core.output_parsers import PydanticOutputParser
from langchain_ollama import ChatOllama

from config.config import Config
from models.schemas.state import Check, Plan, Result, SkillsOutput

llm = ChatOllama(model=Config.OLLAMA_MODEL, base_url=Config.OLLAMA_BASE_URL, temperature=Config.OLLAMA_TEMPERATURE)

plan_parser = PydanticOutputParser(pydantic_object=Plan)
skills_parser = PydanticOutputParser(pydantic_object=SkillsOutput)
evaluation_parser = PydanticOutputParser(pydantic_object=Check)
final_review_parser = PydanticOutputParser(pydantic_object=Result)
