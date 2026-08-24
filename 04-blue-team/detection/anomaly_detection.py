from datetime import datetime, timedelta
from collections import deque


IDENTITY = "agent-001"
VOLUME_THRESHOLD = 20
WINDOW_SECONDS = 60


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def alert(event_type, details):
    print(f"[{now()}] ALERT")
    print(f"Identity: {IDENTITY}")
    print(f"Event: {event_type}")
    print(details)
    print()



def detect_volume_spike(events):
    request_times = deque()

    for event in events:
        if event["type"] == "LLM_REQUEST":
            request_times.append(event["timestamp"])

            # Remove requests outside the 60-second window
            while (
                request_times
                and event["timestamp"] - request_times[0]
                > timedelta(seconds=WINDOW_SECONDS)
            ):
                request_times.popleft()

            if len(request_times) > VOLUME_THRESHOLD:
                alert(
                    "LLM_API_VOLUME_SPIKE",
                    f"Requests in 60 seconds: {len(request_times)}\n"
                    f"Threshold: {VOLUME_THRESHOLD}"
                )
                return True

    return False



def detect_scope_change(events):
    previous_scope = None

    for event in events:
        if event["type"] != "AGENT_REQUEST":
            continue

        current_scope = event["scope"]

        if previous_scope is not None and current_scope != previous_scope:
            alert(
                "SCOPE_CHANGE",
                f"Previous scope: {previous_scope}\n"
                f"Current scope: {current_scope}"
            )
            return True

        previous_scope = current_scope

    return False


def detect_expired_token_reuse(events):
    for event in events:

        if event["type"] != "TOKEN_REQUEST":
            continue

        token = event["token"]
        expiry_time = event["exp"]

        current_time = datetime.now()

        if current_time >= expiry_time:
            alert(
                "TOKEN_REUSE_AFTER_EXPIRY",
                f"Token status: EXPIRED\n"
                f"Token expiry: {expiry_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Current time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Action: Request rejected"
            )
            return True

    return False


print("=" * 60)
print("SECURENOVA BLUE TEAM")
print("PROJECT 3 ATTACK REPLAY + ANOMALY DETECTION")
print("=" * 60)



print("\nReplaying Project 3: Indirect Prompt Injection")
print(f"Identity: {IDENTITY}")

base_time = datetime.now()

volume_events = []

for i in range(25):
    volume_events.append({
        "type": "LLM_REQUEST",
        "timestamp": base_time + timedelta(seconds=i)
    })

print("Simulated LLM requests: 25")
print("Detection window: 60 seconds")
print()

detect_volume_spike(volume_events)



print("Replaying Project 3: Agent Identity Spoofing")
print(f"Identity: {IDENTITY}")

scope_events = [
    {
        "type": "AGENT_REQUEST",
        "scope": "read:ai-data"
    },
    {
        "type": "AGENT_REQUEST",
        "scope": "admin:write"
    }
]

print("Previous scope: read:ai-data")
print("Current scope: admin:write")
print()

detect_scope_change(scope_events)




print("Replaying Project 3: Credential Replay")
print(f"Identity: {IDENTITY}")

replay_token = "simulated-refresh-token"


expired_time = datetime.now() - timedelta(seconds=10)

token_events = [
    {
        "type": "TOKEN_REQUEST",
        "token": replay_token,
        "exp": expired_time
    }
]

print(
    "Token expiry:",
    expired_time.strftime("%Y-%m-%d %H:%M:%S")
)

print(
    "Current time:",
    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
)

print("Replaying the same token after its expiry...")
print()

detect_expired_token_reuse(token_events)