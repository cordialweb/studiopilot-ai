import json

from app.adk.engine import StudioPilotEngine
from app.adk.document.producer_observation_prompt import (
    PRODUCER_OBSERVATION_INSTRUCTION,
)
from app.schemas.producer_observation import ProducerObservationResultV1


class ProducerObservationService:

    def __init__(self, engine: StudioPilotEngine):
        self.engine = engine

    def observe(self, screenplay_text: str) -> ProducerObservationResultV1:

        prompt = f"""
{PRODUCER_OBSERVATION_INSTRUCTION}

Analyze the following screenplay information:

{screenplay_text}

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

        for event in self.engine.run(
            user_id="producer-observation",
            text=prompt,
        ):
            if event.is_final_response():

                raw_text = event.content.parts[0].text

                data = json.loads(raw_text)

                return ProducerObservationResultV1.model_validate(data)

        raise RuntimeError(
            "Producer observation agent did not return a final response"
        )