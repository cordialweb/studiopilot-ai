from app.adk.engine import StudioPilotEngine


engine = StudioPilotEngine()

events = engine.run(
    user_id="test-user",
    text="Say hello to StudioPilot AI in one short sentence."
)

for event in events:
    if event.is_final_response():
        print(event.content.parts[0].text)