from dotenv import load_dotenv
import os
from utils.guest_token_payload import GuestTokenPayload
from utils.environment import Environment

load_dotenv()

# ATTN: Please set the following environment variables in your .env file.

ENVIRONMENT = Environment(os.environ['ENVIRONMENT'])
PORT = os.environ['PORT']

SUPERSET_BASE = os.environ['SUPERSET_BASE_URL']
SUPERSET_USERNAME = os.environ['SUPERSET_USERNAME'] 
SUPERSET_PASSWORD = os.environ['SUPERSET_PASSWORD'] 

CSRF_URL = f"{SUPERSET_BASE}/api/v1/security/csrf_token/"
GUEST_TOKEN_URL = f"{SUPERSET_BASE}/api/v1/security/guest_token/"
LOGIN_URL = f"{SUPERSET_BASE}/api/v1/security/login"

# ATTN: Please set the following variables according to your needs.

PAYLOAD = GuestTokenPayload()
PAYLOAD.initialize(
    username="guest",
    rls_rules=[],
    resources=[],
    first_name="Guest",
    last_name="Guest"
)

# INFO: Resources are a list of dictionaries with the following keys:
# TODO: Update the dashboards according to you
RESOURCES = {
    Environment.DEV: [
        {"type": "dashboard", "id": "9b22e158-4d5d-435f-90d6-f5b46d1d53f0"}
    ],
    Environment.TEST: [
        {"type": "dashboard", "id": "ad83cb93-4d53-435f-90d6-f5b46d1d53f0"}
    ],
    Environment.PROD: [
        {"type": "dashboard", "id": "323dsbfa-4d52-435f-90d6-f5b46d1d53f0"}
    ]
}

# INFO: RLS rule is a function that takes a dictionary of data and returns a dictionary of RLS parameters.
# TODO: Update the RLS rules according to your needs
RLS_RULES = {
    Environment.DEV: [
        lambda data: { "dataset": 23, "clause": f"company_id = {data.get('company_id')}" },
    ],
    Environment.TEST: [
        lambda data: { "dataset": 22, "clause": f"company_id = {data.get('company_id')}" },
    ],
    Environment.PROD: [
        lambda data: { "dataset": 21, "clause": f"company_id = {data.get('company_id')}" },
    ]
}

PAYLOAD.set_resources(RESOURCES[ENVIRONMENT])
PAYLOAD.set_rls_rules(RLS_RULES[ENVIRONMENT])
