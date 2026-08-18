from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from google.genai import types

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
    
    def create_text_message(self, text: str):
        return types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=text)
            ]
        )
        
    def run(self, user_id: str, text: str):

        session = self.create_session(user_id)

        message = self.create_text_message(text)

        return self.runner.run(
            user_id=user_id,
            session_id=session.id,
            new_message=message,
        )