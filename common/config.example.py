from dotenv import load_dotenv
import os
from utils.guest_token_payload import GuestTokenPayload
from utils.environment import Environment

load_dotenv()

# ATTN: Please set the following environment variables in your .env file.

ENVIRONMENT = Environment(os.environ['GUEST_SERVICE_ENVIRONMENT'])
PORT = os.environ['GUEST_SERVICE_PORT']

SUPERSET_BASE = os.environ['GUEST_SERVICE_SUPERSET_BASE_URL']
SUPERSET_ADMIN_USERNAME = os.environ['SUPERSET_ADMIN_USERNAME']
SUPERSET_ADMIN_PASSWORD = os.environ['SUPERSET_ADMIN_PASSWORD']

LOG_LEVEL = os.environ.get('GUEST_SERVICE_LOG_LEVEL', 'INFO')

CSRF_URL = f"{SUPERSET_BASE}/api/v1/security/csrf_token/"
GUEST_TOKEN_URL = f"{SUPERSET_BASE}/api/v1/security/guest_token/"
LOGIN_URL = f"{SUPERSET_BASE}/api/v1/security/login"
DASHBOARDS_URL = f"{SUPERSET_BASE}/api/v1/dashboard/"
DASHBOARDS_EMBEDDED_URL = lambda id: f"{DASHBOARDS_URL}{id}/embedded"

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
RESOURCES = [
    # {"type": "dashboard", "id": "9b22e158-4d5d-435f-90d6-f5b46d1d53f0"}
]

# INFO: RLS rule is a function that takes a dictionary of data and returns a dictionary of RLS parameters.
# TODO: Update the RLS rules according to your needs
RLS_RULES = [
    # lambda data: { "dataset": 23, "clause": f"company_id = {data.get('company_id')}" },
    lambda data: {"clause": f"company_id = {data.get('company_id')}"},
]

PAYLOAD.set_resources(RESOURCES)
PAYLOAD.set_rls_rules(RLS_RULES)
