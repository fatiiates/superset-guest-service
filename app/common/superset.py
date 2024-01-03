import requests
from requests.exceptions import RequestException
from common.config import ENVIRONMENT, CSRF_URL, GUEST_TOKEN_URL
from app.common.config import ApiConfig

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
    access_token = response.json().get('access_token')
    
    session.headers['Authorization'] = f"Bearer {access_token}"
    session.headers['Content-Type'] = 'application/json'

    return session

def fetch_csrf_token(session):
    try:
        verify_option = ApiConfig.get_verify_option(ENVIRONMENT)
        csrf_res = session.get(CSRF_URL, verify=verify_option)
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

        verify_option = ApiConfig.get_verify_option(ENVIRONMENT)
        response = session.post(GUEST_TOKEN_URL, json=data, verify=verify_option)
        response.raise_for_status()
        session.close()
    except RequestException as e:
        raise Exception(f"Error creating guest token: {e}")
    
    return response.json().get('token')
