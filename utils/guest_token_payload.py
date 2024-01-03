class GuestTokenPayload:
    _instance = None
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GuestTokenPayload, cls).__new__(cls)
        return cls._instance

    def initialize(self, username, rls_rules=None, resources=None, first_name="Guest", last_name="Guest"):
        """
        Initialize GuestTokenPayload instance designed with the Singleton pattern.

        Parameters:
        - username (str): The username of the guest.
        - rls_rules (list): Functional list of Row Level Security (RLS) rules.
        - resources (list): List of resources, like dashboard(s).
        - first_name (str): First name of the guest, default=Guest.
        - last_name (str): Last name of the guest, default=Guest.
        """
        if self._initialized:
            return

        if rls_rules is None:
            rls_rules = []
        if resources is None:
            resources = []

        self.user = {
                "username": username,
                "first_name": first_name,
                "last_name": last_name
            }
        
        self.resources: resources
        
        self.rls_rules = rls_rules

        self._initialized = True

    def set_user(self, user):
        self.user = user

    def add_resource(self, resource):
        self.resources.append(resource)
    
    def set_resources(self, resources):
        self.resources = resources

    def add_rls_rule(self, rls_rule):
        self.rls_rules.append(rls_rule)

    def set_rls_rules(self, rls_rule):
        self.rls_rules = rls_rule

    def prepare_rls(self, parameters: dict):
        """
        Prepare RLS data for the payload.

        Parameters:
        - parameters (dict): Parameters for formatting clause.

        Returns:
        - dict: RLS data.
        """
        prepared_rls = []

        for rls_func in self.rls_rules:
            prepared_rls.append(rls_func(parameters))

        return prepared_rls
    
    def prepare_payload_data(self, parameters: dict):
        """
        Prepare payload data.

        Returns:
        - dict: Payload data.
        """
        return {
            "user": self.user,
            "resources": self.resources,
            "rls": self.prepare_rls(parameters)
        }

    def get_payload_data(self, parameters: dict):
        """Get the payload data."""

        return self.prepare_payload_data(parameters)
