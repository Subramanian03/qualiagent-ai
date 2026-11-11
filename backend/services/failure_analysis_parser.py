import json

from pydantic import ValidationError

from backend.models.failure_analysis_ai import (
    FailureAnalysisAIOutput,
)


class FailureAnalysisProviderError(
    ValueError
):
    pass


def extract_json_object(
    value
) -> dict:

    if isinstance(
        value,
        dict
    ):

        return value


    text = str(
        value or ""
    ).strip()


    if not text:

        raise FailureAnalysisProviderError(
            "AI provider returned an empty response."
        )


    if text.startswith(
        "```"
    ):

        lines = text.splitlines()


        if lines:

            lines = lines[1:]


        if (
            lines
            and
            lines[-1].strip().startswith(
                "```"
            )
        ):

            lines = lines[:-1]


        text = "\n".join(
            lines
        ).strip()


    try:

        parsed = json.loads(
            text
        )


    except json.JSONDecodeError as exc:

        raise FailureAnalysisProviderError(
            (
                "AI provider did not return "
                "valid JSON."
            )
        ) from exc


    if not isinstance(
        parsed,
        dict
    ):

        raise FailureAnalysisProviderError(
            (
                "AI provider response must be "
                "a JSON object."
            )
        )


    return parsed


def parse_failure_analysis_output(
    value
) -> FailureAnalysisAIOutput:

    payload = extract_json_object(
        value
    )


    try:

        return (
            FailureAnalysisAIOutput
            .model_validate(
                payload
            )
        )


    except ValidationError as exc:

        raise FailureAnalysisProviderError(
            (
                "AI failure-analysis response "
                "did not match the required "
                "structured contract."
            )
        ) from exc