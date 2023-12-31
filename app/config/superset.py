import requests
from requests.exceptions import RequestException
from common.config import ENVIRONMENT, CSRF_URL, GUEST_TOKEN_URL, LOGIN_URL
from app.config.config import ApiConfig

def login(username, password):
    session = requests.Session()
    payload = {
        "password": password,
        "provider": "db",
        "refresh": True,
        "username": username,
    }
    
    url = ApiConfig.get_login_url()
    verify_option = ApiConfig.get_verify_option(ENVIRONMENT)

    response = session.post(url, json=payload, verify=verify_option)
    response.raise_for_status()
    
    return session

def fetch_csrf_token(session):
    try:
        csrf_res = session.get(CSRF_URL, verify=False)
        csrf_res.raise_for_status()
    except RequestException as e:
        raise Exception(f"Error fetching CSRF token: {e}")

    return csrf_res.json()['result']


def create_guest_token(data=None):
    try:
        username, password = ApiConfig.get_superset_credentials()
        session = login(username, password)

        csrf_token = fetch_csrf_token(session)
        session.headers['Referer'] = CSRF_URL
        session.headers['X-CSRFToken'] = csrf_token

        response = session.post(GUEST_TOKEN_URL, json=data, verify=False)
        response.raise_for_status()
        session.close()
    except RequestException as e:
        raise Exception(f"Error creating guest token: {e}")
    
    return response.json().get('token')
