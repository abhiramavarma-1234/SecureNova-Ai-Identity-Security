from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization


PRIVATE_KEY = "04-blue-team/identity/keys/agent_private.pem"
PUBLIC_KEY = "04-blue-team/identity/keys/agent_public.pem"


def load_keys():
    with open(PRIVATE_KEY, "rb") as file:
        private_key = serialization.load_pem_private_key(
            file.read(),
            password=None
        )

    with open(PUBLIC_KEY, "rb") as file:
        public_key = serialization.load_pem_public_key(
            file.read()
        )

    return private_key, public_key


def sign_message(private_key, message):
    return private_key.sign(message.encode())


def verify_message(public_key, message, signature):
    try:
        public_key.verify(
            signature,
            message.encode()
        )
        return True
    except Exception:
        return False


def main():

    print("=" * 60)
    print("SECURENOVA BLUE TEAM")
    print("ED25519 AGENT MESSAGE VERIFICATION")
    print("=" * 60)

    private_key, public_key = load_keys()

    
    message = "Agent A: Generate the daily security report."

    signature = sign_message(
        private_key,
        message
    )

    print("\nOriginal message:")
    print(message)

    print("\nMessage signed successfully.")

    
    valid = verify_message(
        public_key,
        message,
        signature
    )

    print("\nOriginal message verification:")

    if valid:
        print("SIGNATURE VALID")
        print("Message accepted.")

    else:
        print("SIGNATURE INVALID")
        print("Message rejected.")

    # Attacker changes one character
    tampered_message = "Agent A: Generate the daily security report!"

    print("\nTampered message:")
    print(tampered_message)

    
    tampered_valid = verify_message(
        public_key,
        tampered_message,
        signature
    )

    print("\nTampered message verification:")

    if tampered_valid:
        print("SIGNATURE VALID")
        print("Message accepted.")

    else:
        print("SIGNATURE VERIFICATION FAILED")
        print("ERROR: Message was modified after signing.")
        print("Message rejected.")


if __name__ == "__main__":
    main()