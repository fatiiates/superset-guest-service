from common.config import SUPERSET_ADMIN_PASSWORD, SUPERSET_ADMIN_USERNAME, LOGIN_URL, ENVIRONMENT
from utils.environment import Environment

class ApiConfig:

    @staticmethod
    def get_login_url():
        return LOGIN_URL

    @staticmethod
    def get_verify_option():
        return not (ENVIRONMENT == Environment.DEV)
    
    @staticmethod
    def get_superset_credentials():
        return SUPERSET_ADMIN_USERNAME, SUPERSET_ADMIN_PASSWORD
