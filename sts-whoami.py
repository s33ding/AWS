import os
import boto3

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv optional; falls back to OS environment

# Account nickname mapping loaded from the ACCOUNT_NAMES env var.
# Format: "id:name,id:name" (see .env-template). Falls back to empty map.
def _load_account_names():
    raw = os.environ.get("ACCOUNT_NAMES", "")
    mapping = {}
    for pair in raw.split(","):
        pair = pair.strip()
        if ":" in pair:
            acct_id, name = pair.split(":", 1)
            mapping[acct_id.strip()] = name.strip()
    return mapping

ACCOUNT_NAMES = _load_account_names()

# Create a Boto3 session (uses current profile from AWS_PROFILE or default)
session = boto3.Session()
region = session.region_name
profile = session.profile_name

# Create an STS client using the session
sts_client = session.client('sts')

# Call get_caller_identity
identity = sts_client.get_caller_identity()
account_id = identity['Account']
account_name = ACCOUNT_NAMES.get(account_id, "unknown")

# Print the details
print("────────────────────────────────────────")
print("✅ Current Identity:")
print(f"   Account: {account_name} ({account_id})")
print(f"   Profile: {profile}")
print(f"   User:    {identity['UserId']}")
print(f"   ARN:     {identity['Arn']}")
print(f"   Region:  {region}")
print("────────────────────────────────────────")
