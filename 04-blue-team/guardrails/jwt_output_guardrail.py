import re


FAKE_JWT = (
    "eyJhbGciOiJIUzI1NiJ9."
    "eyJhZ2VudF9pZCI6IlNOUy1BR0VOVC0wMSIs"
    "InJvbGUiOiJpbnRlcm5hbCJ9."
    "fake_signature"
)


def redact_jwt(text):
    jwt_pattern = r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+"

    return re.sub(
        jwt_pattern,
        "[REDACTED]",
        text
    )


def main():

    print("=" * 60)
    print("SECURENOVA BLUE TEAM")
    print("JWT OUTPUT GUARDRAIL")
    print("=" * 60)

    model_response = (
        "The agent processed the request successfully. "
        "Session credential: "
        + FAKE_JWT
    )

    print("\nOriginal model response:")
    print(model_response)

    protected_response = redact_jwt(model_response)

    print("\nGuardrail output:")
    print(protected_response)

    if "[REDACTED]" in protected_response:
        print("\nRESULT: JWT REDACTED")
    else:
        print("\nRESULT: JWT NOT DETECTED")


if __name__ == "__main__":
    main()