import re
from dataclasses import dataclass

ALLOWED_FAILURE_STATUSES = {
    "failed",
    "error",
}


MAX_ERROR_EXCERPT_LENGTH = 4000

MAX_OUTPUT_EXCERPT_LENGTH = 8000

MAX_AUTOMATION_CODE_LENGTH = 12000


REDACTION_TEXT = "[REDACTED]"


SENSITIVE_FIELD_NAMES = {
    "password",
    "passwd",
    "pwd",
    "secret",
    "token",
    "access_token",
    "refresh_token",
    "api_key",
    "apikey",
    "authorization",
    "cookie",
    "set-cookie",
    "client_secret",
    "private_key",
    "test_password",
    "username_password",
}


SECRET_ASSIGNMENT_PATTERN = re.compile(
    r"""(?ix)
    \b(
        password
        |passwd
        |pwd
        |secret
        |token
        |access[_-]?token
        |refresh[_-]?token
        |api[_-]?key
        |apikey
        |client[_-]?secret
        |test[_-]?password
    )
    \b
    \s*
    (
        =
        |:
    )
    \s*
    (
        ["'][^"'\r\n]*["']
        |
        [^\s,;}\]\r\n]+
    )
    """
)


AUTHORIZATION_PATTERN = re.compile(
    r"""(?ix)
    \b(
        authorization
        |proxy-authorization
    )
    \s*:
    \s*
    (
        bearer
        |basic
        |token
    )
    \s+
    [^\s,\r\n]+
    """
)


COOKIE_PATTERN = re.compile(
    r"""(?ix)
    \b(
        cookie
        |set-cookie
    )
    \s*:
    \s*
    [^\r\n]+
    """
)


URL_CREDENTIAL_PATTERN = re.compile(
    r"""(?i)
    (https?://)
    ([^/\s:@]+)
    :
    ([^/\s@]+)
    @
    """
)


ENV_SECRET_PATTERN = re.compile(
    r"""(?ix)
    \b(
        GROQ_API_KEY
        |OPENAI_API_KEY
        |API_KEY
        |TEST_PASSWORD
        |PASSWORD
        |ACCESS_TOKEN
        |REFRESH_TOKEN
        |CLIENT_SECRET
    )
    \s*=\s*
    [^\s\r\n]+
    """
)


FORBIDDEN_AUTOMATIC_ACTIONS = {
    "change_execution_result",
    "approve_automation",
    "overwrite_ready_automation",
    "modify_cycle_history",
    "delete_execution_evidence",
}

@dataclass
class RedactionResult:

    text: str | None

    redaction_count: int

def normalise_status(
    value
) -> str:

    return str(
        value or ""
    ).strip().lower()


def ensure_execution_can_be_analysed(
    execution
) -> None:

    status = normalise_status(
        execution.status
    )


    if status not in ALLOWED_FAILURE_STATUSES:

        raise ValueError(
            (
                "AI failure analysis is available "
                "only for FAILED or ERROR executions."
            )
        )


def safe_excerpt(
    value,
    max_length: int
) -> str | None:

    if value is None:
        return None


    cleaned = str(
        value
    ).strip()


    if not cleaned:

        return None


    if len(
        cleaned
    ) <= max_length:

        return cleaned


    return (
        cleaned[
            :max_length
        ]
        +
        "\n...[truncated]"
    )

def redact_sensitive_text(
    value
) -> RedactionResult:

    if value is None:

        return RedactionResult(
            text=None,
            redaction_count=0
        )


    text = str(
        value
    )


    if not text.strip():

        return RedactionResult(
            text=None,
            redaction_count=0
        )


    redaction_count = 0


    def replace_secret_assignment(
        match
    ):

        nonlocal redaction_count

        redaction_count += 1


        return (
            f"{match.group(1)}"
            f"{match.group(2)}"
            f"{REDACTION_TEXT}"
        )


    text = SECRET_ASSIGNMENT_PATTERN.sub(
        replace_secret_assignment,
        text
    )


    def replace_authorization(
        match
    ):

        nonlocal redaction_count

        redaction_count += 1


        return (
            f"{match.group(1)}: "
            f"{REDACTION_TEXT}"
        )


    text = AUTHORIZATION_PATTERN.sub(
        replace_authorization,
        text
    )


    def replace_cookie(
        match
    ):

        nonlocal redaction_count

        redaction_count += 1


        return (
            f"{match.group(1)}: "
            f"{REDACTION_TEXT}"
        )


    text = COOKIE_PATTERN.sub(
        replace_cookie,
        text
    )


    def replace_url_credentials(
        match
    ):

        nonlocal redaction_count

        redaction_count += 1


        return (
            f"{match.group(1)}"
            f"{REDACTION_TEXT}@"
        )


    text = URL_CREDENTIAL_PATTERN.sub(
        replace_url_credentials,
        text
    )


    def replace_environment_secret(
        match
    ):

        nonlocal redaction_count

        redaction_count += 1


        variable_name = (
            match.group(1)
        )


        return (
            f"{variable_name}="
            f"{REDACTION_TEXT}"
        )


    text = ENV_SECRET_PATTERN.sub(
        replace_environment_secret,
        text
    )


    return RedactionResult(
        text=text.strip(),
        redaction_count=(
            redaction_count
        )
    )


def redact_and_excerpt(
    value,
    max_length: int
) -> RedactionResult:

    redacted = (
        redact_sensitive_text(
            value
        )
    )


    excerpt = safe_excerpt(
        redacted.text,
        max_length
    )


    return RedactionResult(
        text=excerpt,
        redaction_count=(
            redacted.redaction_count
        )
    )