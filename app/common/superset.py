import logging
import requests
from requests.exceptions import RequestException
from common.config import CSRF_URL, GUEST_TOKEN_URL, DASHBOARDS_URL, DASHBOARDS_EMBEDDED_URL
from app.common.config import ApiConfig

verify_option = ApiConfig.get_verify_option()


def fetch_csrf_token(session):
    try:
        csrf_res = session.get(CSRF_URL, verify=verify_option)
        csrf_res.raise_for_status()
    except RequestException as e:
        logging.error("Error fetching CSRF token: " + str(e))
        raise Exception("Internal server error.")

    return csrf_res.json()['result']

def login(username, password):
    session = requests.Session()
    payload = {
        "password": password,
        "provider": "db",
        "refresh": True,
        "username": username,
    }
    
    url = ApiConfig.get_login_url()
    response = session.post(url, json=payload, verify=verify_option)

    response.raise_for_status()
    access_token = response.json().get('access_token')
    
    session.headers['Authorization'] = f"Bearer {access_token}"
    session.headers['Content-Type'] = 'application/json'

    csrf_token = fetch_csrf_token(session)
    session.headers['Referer'] = CSRF_URL
    session.headers['X-CSRFToken'] = csrf_token

    return session

def fetch_embedded_dashboard(session, id):
    """  
    Fetch the embedded dashboard using the provided session.  
    """

    # prepare the endpoint
    DASHBOARDS_EMBEDDED_ENDPOINT = DASHBOARDS_EMBEDDED_URL(id)

    try:
        embedded_dashboard_res = session.get(DASHBOARDS_EMBEDDED_ENDPOINT, verify=verify_option)
        embedded_dashboard_res.raise_for_status()
        if embedded_dashboard_res.json()['result']['uuid'] == None:
            return None
    except RequestException as e:
        logging.error("Error fetching embedded dashboard: " + str(e))
        return None
    
    return embedded_dashboard_res.json()['result']['uuid']

def fetch_dashboard_resources(session):
    """  
    Fetch the dashboards using the provided session.  
    """
    payload_query_params = {
        "columns": ["ids"],
        "page_size": 100
    }
    try:
        dashboards_res = session.get(DASHBOARDS_URL, params=payload_query_params, verify=verify_option)
        dashboards_res.raise_for_status()
        dashboard_ids = []
        for dashboard in dashboards_res.json()['result']:
            # check if it is published
            if not dashboard.get('published'):
                continue

            dashboard_ids.append(dashboard.get('id'))

        dashboard_uuids = []
        for dashboard_id in dashboard_ids:
            embedded_dashboard_uuid = fetch_embedded_dashboard(session, dashboard_id)
            
            if not embedded_dashboard_uuid:
                continue

            dashboard_uuids.append(embedded_dashboard_uuid)

    except RequestException as e:
        logging.error("Error fetching dashboards: " + str(e))
        raise Exception("Internal server error.")
    
    dashboard_resources = []
    for dashboard_uuid in dashboard_uuids:
        dashboard_resources.append({"type": "dashboard", "id": dashboard_uuid})

    return dashboard_resources

def create_guest_token(data={}, auto_generate_resources=True):
    try:
        data = data.copy()
        username, password = ApiConfig.get_superset_credentials()
        session = login(username, password)
        
        if auto_generate_resources:
            resources = data.get('resources', [])[:]
            resources.extend(fetch_dashboard_resources(session))
            data['resources'] = resources

        response = session.post(GUEST_TOKEN_URL, json=data, verify=verify_option)
        response.raise_for_status()
        session.close()
    except RequestException as e:
        logging.error("Error creating guest token: " + str(e))
        raise Exception("Internal server error.")
    
    return response.json().get('token')
