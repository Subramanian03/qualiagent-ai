from backend.models.requirement import (
    RequirementAnalysisResponse,
    RequirementInput,
)


KEYWORDS = {
    "login": "functional",
    "log in": "functional",
    "sign in": "functional",
    "password": "security",
    "email": "validation",
    "username": "validation",
    "payment": "security",
    "checkout": "end-to-end",
    "search": "functional",
    "upload": "file-validation",
    "download": "functional",
    "token": "security",
    "authentication": "security",
    "response": "api",
    "status code": "api",
}


def identify_keywords(description):
    normalised_description = description.lower()

    found_keywords = []

    for keyword in KEYWORDS:
        if keyword in normalised_description:
            found_keywords.append(keyword)

    return found_keywords


def suggest_test_types(application_type, identified_keywords):
    test_types = {
        "functional",
        "negative",
        "boundary",
    }

    for keyword in identified_keywords:
        test_types.add(KEYWORDS[keyword])

    if application_type == "web":
        test_types.add("user-interface")
        test_types.add("cross-browser")

    elif application_type == "mobile":
        test_types.add("device-compatibility")
        test_types.add("orientation")

    elif application_type == "api":
        test_types.add("schema-validation")
        test_types.add("response-validation")

    return sorted(test_types)


def determine_risk_level(description, identified_keywords):
    high_risk_keywords = {
        "payment",
        "password",
        "token",
        "authentication",
    }

    for keyword in identified_keywords:
        if keyword in high_risk_keywords:
            return "high"

    if len(description.split()) < 8:
        return "medium"

    return "low"


def generate_acceptance_criteria(requirement, identified_keywords):
    criteria = [
        f"The {requirement.title.lower()} behaviour works as described.",
        "Valid input should produce the expected successful result.",
        "Invalid input should produce a clear and controlled response.",
    ]

    if "password" in identified_keywords:
        criteria.append(
            "The password must not be displayed as readable text."
        )

    if "email" in identified_keywords:
        criteria.append(
            "The system must validate the email address format."
        )

    if requirement.application_type == "api":
        criteria.append(
            "The API must return the expected HTTP status code."
        )

    return criteria


def generate_questions(requirement, identified_keywords):
    questions = [
        "What should happen when invalid input is submitted?",
        "What message should be shown when the operation fails?",
        "Are there any role or permission restrictions?",
    ]

    if "password" in identified_keywords:
        questions.append(
            "What are the password rules and account-locking conditions?"
        )

    if requirement.application_type == "web":
        questions.append(
            "Which browsers and screen sizes must be supported?"
        )

    elif requirement.application_type == "mobile":
        questions.append(
            "Which mobile operating systems and versions must be supported?"
        )

    elif requirement.application_type == "api":
        questions.append(
            "What authentication method and response schema are required?"
        )

    return questions


def analyse_requirement(requirement):
    identified_keywords = identify_keywords(
        requirement.description
    )

    risk_level = determine_risk_level(
        requirement.description,
        identified_keywords
    )

    suggested_test_types = suggest_test_types(
        requirement.application_type,
        identified_keywords
    )

    acceptance_criteria = generate_acceptance_criteria(
        requirement,
        identified_keywords
    )

    questions = generate_questions(
        requirement,
        identified_keywords
    )

    return RequirementAnalysisResponse(
        requirement_id=requirement.requirement_id,
        summary=requirement.title,
        application_type=requirement.application_type,
        testable=True,
        risk_level=risk_level,
        identified_keywords=identified_keywords,
        suggested_test_types=suggested_test_types,
        acceptance_criteria=acceptance_criteria,
        questions=questions,
        message="Requirement analysis completed successfully.",
    )