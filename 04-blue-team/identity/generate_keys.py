from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from pathlib import Path


KEY_DIR = Path("04-blue-team/identity/keys")


def generate_keys():
    KEY_DIR.mkdir(parents=True, exist_ok=True)

    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    private_path = KEY_DIR / "agent_private.pem"
    public_path = KEY_DIR / "agent_public.pem"

    private_path.write_bytes(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    )

    public_path.write_bytes(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )

    print("=" * 60)
    print("SECURENOVA BLUE TEAM")
    print("ED25519 AGENT IDENTITY")
    print("=" * 60)

    print("\nKey pair generated successfully.")
    print(f"Private key: {private_path}")
    print(f"Public key:  {public_path}")

    print("\nFiles created:")
    print(private_path.exists(), private_path)
    print(public_path.exists(), public_path)


if __name__ == "__main__":
    generate_keys()