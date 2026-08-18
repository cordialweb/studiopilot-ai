import json

from app.schemas.producer_observation import ProducerObservationResultV1
from app.adk.config import MODEL
from app.adk.engine import StudioPilotEngine
from app.adk.document.producer_observation_prompt import (
    PRODUCER_OBSERVATION_INSTRUCTION,
)


engine = StudioPilotEngine()

text = """
SCREENPLAY: THE LAST LANTERN

SCENE 5
EXT. SEA WALL — NIGHT

Lena Park tries to call Harbor Control from a fishing boat
battling rough waves right as the lighthouse light abruptly goes dark.

CHARACTER:
Lena Park

PROP:
Handheld Radio

SCENE 6
INT. LIGHTHOUSE — LANTERN ROOM — NIGHT

Maya and Daniel find the lantern stopped and follow a trail
of seawater to a locked maintenance hatch, which Daniel cuts open.

CHARACTERS:
Maya Reyes
Daniel Reyes

PROPS:
Brass Lighthouse Lantern
Pocketknife

SCENE 10
INT. LIGHTHOUSE — LANTERN ROOM — CONTINUOUS

Maya pulls the emergency lever to restart the turning lens,
beaming light to save the offshore fishing boat.

CHARACTERS:
Maya Reyes
Daniel Reyes
Lena Park

PROP:
Brass Lighthouse Lantern
"""

prompt = f"""
{PRODUCER_OBSERVATION_INSTRUCTION}

Analyze the following screenplay information:

{text}

For every observation, provide:

- basis_type = EXPLICIT when the screenplay directly supports the observation.
- basis_type = INFERRED when the observation is a reasonable production inference.
- basis = the specific screenplay information that supports the observation.

Return JSON matching this structure:

{{
  "observations": [
    {{
      "type": "REQUIREMENT | RISK | DEPENDENCY | OVERLOOKED_ITEM | DECISION",
      "severity": "LOW | MEDIUM | HIGH",
      "title": "short title",
      "description": "producer-focused explanation",
      "basis_type": "EXPLICIT | INFERRED",
      "basis": "specific screenplay evidence supporting this observation",
      "scene_number": 0,
      "confidence": 0.0,
      "requires_human_decision": false
    }}
  ]
}}
"""

for event in engine.run(
    user_id="producer-observation-test",
    text=prompt,
):
    if event.is_final_response():

        raw_text = event.content.parts[0].text

        print("RAW RESPONSE:")
        print(raw_text)

        data = json.loads(raw_text)

        result = ProducerObservationResultV1.model_validate(data)

        print()
        print("VALIDATION SUCCESSFUL")
        print()

        print(result.model_dump(mode="json"))