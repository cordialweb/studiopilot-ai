from app.adk.engine import StudioPilotEngine

engine = StudioPilotEngine()

session = engine.create_session("umar")

print(session)
print(session.id)