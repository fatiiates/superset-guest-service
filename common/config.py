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
RESOURCES = {
    Environment.DEV: [
        {"type": "dashboard", "id": "e9b1b1a2-5b0e-4b0e-9b0a-5b9b1b0e4b0e"}
    ],
    Environment.TEST: [
        {"type": "dashboard", "id": "dbe6592e-953b-4b58-8271-dc7178f9e42b"}
    ],
    Environment.PROD: [
        {"type": "dashboard", "id": "bd85e78a-ad23-4ae2-af10-f62566068844"}
    ]
}

# INFO: RLS rule is a function that takes a dictionary of data and returns a dictionary of RLS parameters.
RLS_RULES = {
    Environment.DEV: [
        lambda data: { "dataset": 55, "clause": f"company_id = {data.get('company_id')}" },
    ],
    Environment.TEST: [
        lambda data: { "dataset": 54, "clause": f"company_id = {data.get('company_id')}" },
    ],
    Environment.PROD: [
        lambda data: { "dataset": 52, "clause": f"company_id = {data.get('company_id')}" },
    ]
}

PAYLOAD.set_resources(RESOURCES[ENVIRONMENT])
PAYLOAD.set_rls_rules(RLS_RULES[ENVIRONMENT])