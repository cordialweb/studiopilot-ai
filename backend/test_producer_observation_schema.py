from app.schemas.producer_observation import (
    ObservationSeverity,
    ObservationType,
    ProducerObservationResultV1,
)


result = ProducerObservationResultV1(
    observations=[
        {
            "type": ObservationType.RISK,
            "severity": ObservationSeverity.HIGH,
            "title": "Night exterior",
            "description": (
                "Scene requires a night exterior at the sea wall."
            ),
            "scene_number": 5,
            "confidence": 0.95,
            "requires_human_decision": True,
        }
    ]
)

print(result.model_dump())
print()
print(result.model_json_schema())