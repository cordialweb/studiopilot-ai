from google.adk.agents.llm_agent import Agent

from app.adk.config import MODEL
from app.adk.document.prompts import DOCUMENT_AGENT_INSTRUCTION

root_agent = Agent(
    name="document_agent",
    model=MODEL,
    description="StudioPilot AI Document Agent",
    instruction=DOCUMENT_AGENT_INSTRUCTION,
    tools=[],
)