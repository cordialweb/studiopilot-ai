from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from app.adk.studio.agent import root_agent


class StudioPilotEngine:

    def __init__(self):

        self.session_service = InMemorySessionService()

        self.runner = Runner(
            app_name="StudioPilot AI",
            agent=root_agent,
            session_service=self.session_service,
        )
        
    def create_session(self, user_id: str):
        return self.session_service.create_session_sync(
            app_name="StudioPilot AI",
            user_id=user_id,
        )