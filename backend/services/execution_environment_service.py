from backend.db.execution_config_model import (
    ExecutionConfigDB,
)


REDACTION_TEXT = "[REDACTED]"


def clean_optional_value(
    value: str | None
) -> str:

    if value is None:
        return ""

    return value.strip()


def build_execution_environment(
    config: ExecutionConfigDB,
    test_password: str | None
) -> dict[str, str]:

    base_url = clean_optional_value(
        config.base_url
    )

    if not base_url:
        raise ValueError(
            "BASE_URL is not configured"
        )

    username = clean_optional_value(
        config.test_username
    )

    password = clean_optional_value(
        test_password
    )

    if config.credentials_required:

        if not username:
            raise ValueError(
                "Test username is required"
            )

        if not password:
            raise ValueError(
                "Test password is required "
                "for this execution"
            )

    return {
        "BASE_URL": base_url,

        "TEST_USERNAME": username,

        "TEST_PASSWORD": password,

        "TEST_FIRST_NAME":
            clean_optional_value(
                config.test_first_name
            ),

        "TEST_LAST_NAME":
            clean_optional_value(
                config.test_last_name
            ),

        "TEST_POSTAL_CODE":
            clean_optional_value(
                config.test_postal_code
            ),

        "QUALIAGENT_ENVIRONMENT":
            clean_optional_value(
                config.environment_name
            )
    }


def get_environment_secrets(
    runtime_environment: dict[str, str]
) -> list[str]:

    secret_keys = {
        "TEST_PASSWORD"
    }

    secrets = []

    for key in secret_keys:

        value = runtime_environment.get(
            key,
            ""
        ).strip()

        if value:
            secrets.append(value)

    return secrets


def redact_text(
    value: str | None,
    secrets: list[str]
) -> str:

    redacted = value or ""

    safe_secrets = sorted(
        {
            secret
            for secret in secrets
            if secret
        },
        key=len,
        reverse=True
    )

    for secret in safe_secrets:
        redacted = redacted.replace(
            secret,
            REDACTION_TEXT
        )

    return redacted