from google.genai import types

message = types.Content(
    role="user",
    parts=[
        types.Part(text="Hello StudioPilot AI")
    ]
)

print(message)