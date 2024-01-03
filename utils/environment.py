from enum import Enum

class Environment(Enum):
    DEV = "development"
    TEST = "test"
    PROD = "production"

    @staticmethod
    def get_environment(environment):
        if environment == Environment.DEV.value:
            return Environment.DEV
        elif environment == Environment.TEST.value:
            return Environment.TEST
        elif environment == Environment.PROD.value:
            return Environment.PROD
        else:
            raise Exception(f"Invalid environment: {environment}")
   