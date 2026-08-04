from google.adk.agents.llm_agent import Agent

from app.core.config import settings


document_agent = Agent(
    name="document_agent",
    model=settings.GOOGLE_MODEL,
    description="Analyzes screenplay documents.",
    instruction="""
You are StudioPilot AI's Document Agent.

Your job is to analyze screenplay documents.

Always produce structured and accurate responses.
""",
    tools=[]
)