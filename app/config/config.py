from common.config import SUPERSET_PASSWORD, SUPERSET_USERNAME, LOGIN_URL
from utils.environment import Environment

class ApiConfig:

    @staticmethod
    def get_login_url():
        return LOGIN_URL

    @staticmethod
    def get_verify_option(environment):
        return not (environment == Environment.DEV)
    
    @staticmethod
    def get_superset_credentials():
        return SUPERSET_USERNAME, SUPERSET_PASSWORD
