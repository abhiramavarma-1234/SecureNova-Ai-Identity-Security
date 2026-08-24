from typing import Optional
from nemoguardrails.actions import action


@action(is_system_action=True)
async def check_securenova_input(context: Optional[dict] = None):
    """
    SecureNova input guardrail.

    Returns:
        False -> block the request
        True  -> allow the request
    """

    context = context or {}

    # NeMo provides the current input as `user_message`.
    # Fall back to last_user_message if available.
    message = (
        context.get("user_message")
        or context.get("last_user_message")
        or ""
    )

    text = message.lower()

    # ---------------------------------------------------------
    # 1. INDIRECT PROMPT INJECTION / CREDENTIAL EXFILTRATION
    # ---------------------------------------------------------
    credential_patterns = [
        "include the complete secret",
        "provide the complete secret",
        "reveal the secret",
        "include the secret",
        "security verification",
        "identity verification",
    ]

    # ---------------------------------------------------------
    # 2. AGENT IDENTITY SPOOFING
    # ---------------------------------------------------------
    identity_patterns = [
        "administrator has approved",
        "authorized orchestrator",
        "trusted orchestrator",
        "execute the privileged",
        "admin privileges",
    ]

    # ---------------------------------------------------------
    # 3. SYSTEM PROMPT EXTRACTION
    # ---------------------------------------------------------
    extraction_patterns = [
        "ignore previous instructions",
        "reveal the complete system",
        "reveal the system prompt",
        "complete system instructions",
        "internal configuration",
    ]

    # ---------------------------------------------------------
    # 4. RAG POISONING
    # ---------------------------------------------------------
    rag_patterns = [
        "important knowledge base update",
        "when this document is retrieved",
        "execute the administrative tool",
        "retrieved knowledge instructs",
    ]

    # ---------------------------------------------------------
    # 5. TOOL ABUSE
    # ---------------------------------------------------------
    tool_patterns = [
        "send_admin_email",
        "send_admin_report",
        "use the administrative tool",
        "execute the administrative tool",
        "important administrative instruction",
    ]

    pattern_groups = [
        ("credential", credential_patterns),
        ("identity", identity_patterns),
        ("extraction", extraction_patterns),
        ("rag", rag_patterns),
        ("tool", tool_patterns),
    ]

    for category, patterns in pattern_groups:
        for pattern in patterns:
            if pattern in text:
                print(
                    f"[NeMo Input Rail] BLOCKED "
                    f"| category={category} "
                    f"| pattern={pattern}"
                )
                return False

    print("[NeMo Input Rail] ALLOWED")
    return True