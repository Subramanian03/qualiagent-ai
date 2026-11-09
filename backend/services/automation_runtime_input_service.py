from urllib.parse import urlparse

from backend.models.automation_input_schema import (
    AutomationInputSchema,
)

from backend.models.automation_runtime_input import (
    AutomationRuntimeInputSubmission,
    ValidatedAutomationRuntimeInputs,
)

def get_persisted_input_schema(
    automation
) -> AutomationInputSchema:

    raw_schema = getattr(
        automation,
        "input_schema",
        None
    )


    if not raw_schema:

        raise ValueError(
            "Automation version does not "
            "contain a persisted input schema"
        )


    try:

        return (
            AutomationInputSchema
            .model_validate(
                raw_schema
            )
        )

    except Exception as exc:

        raise ValueError(
            "Persisted automation input "
            "schema is invalid"
        ) from exc


def validate_runtime_inputs(
    schema: AutomationInputSchema,
    submission: AutomationRuntimeInputSubmission
) -> ValidatedAutomationRuntimeInputs:

    definitions = {
        item.key: item
        for item in schema.inputs
    }


    submitted_keys = set(
        submission.values.keys()
    )

    allowed_keys = set(
        definitions.keys()
    )


    extra_keys = (
        submitted_keys -
        allowed_keys
    )


    if extra_keys:

        raise ValueError(
            "Unexpected automation input "
            "keys: "
            + ", ".join(
                sorted(extra_keys)
            )
        )


    missing_keys = []


    for key, definition in (
        definitions.items()
    ):

        if not definition.required:
            continue


        if key not in submission.values:
            missing_keys.append(
                key
            )

            continue


        value = submission.values[
            key
        ]


        if (
            isinstance(value, str) and
            not value.strip()
        ):
            missing_keys.append(
                key
            )


        if value is None:
            missing_keys.append(
                key
            )


    if missing_keys:

        raise ValueError(
            "Missing required automation "
            "inputs: "
            + ", ".join(
                sorted(
                    set(missing_keys)
                )
            )
        )


    non_secret_values = {}
    secret_values = {}


    for key, value in (
        submission.values.items()
    ):

        definition = definitions[
            key
        ]


        validated_value = (
            validate_runtime_value(
                definition.input_type,
                value,
                key
            )
        )


        if definition.secret:

            secret_values[
                key
            ] = str(
                validated_value
            )

        else:

            non_secret_values[
                key
            ] = validated_value


    return (
        ValidatedAutomationRuntimeInputs(
            non_secret_values=(
                non_secret_values
            ),
            secret_values=(
                secret_values
            )
        )
    )


def validate_runtime_value(
    input_type: str,
    value,
    key: str
):

    if input_type == "boolean":

        if not isinstance(
            value,
            bool
        ):
            raise ValueError(
                f"{key} must be boolean"
            )

        return value


    if input_type == "number":

        if isinstance(
            value,
            bool
        ):
            raise ValueError(
                f"{key} must be numeric"
            )

        try:

            return float(
                value
            )

        except (
            TypeError,
            ValueError
        ) as exc:

            raise ValueError(
                f"{key} must be numeric"
            ) from exc


    if not isinstance(
        value,
        str
    ):

        raise ValueError(
            f"{key} must be text"
        )


    cleaned = value.strip()


    if input_type == "url":

        parsed = urlparse(
            cleaned
        )

        if (
            parsed.scheme not in {
                "http",
                "https"
            } or
            not parsed.netloc
        ):

            raise ValueError(
                f"{key} must be a valid "
                "HTTP or HTTPS URL"
            )


    if input_type == "email":

        if (
            "@" not in cleaned or
            cleaned.startswith("@") or
            cleaned.endswith("@")
        ):

            raise ValueError(
                f"{key} must be a valid "
                "email address"
            )


    return cleaned