# Superset Guest Service

Superset Guest Service is a lightweight middleware that employs the connector pattern to seamlessly integrate with Superset, streamlining the process of efficiently retrieving guest tokens.

# Prerequisites

- [Python](https://www.python.org/downloads/) 
- [Docker](https://docs.docker.com/get-docker/)

# Run

- Clone the repository
- Copy the `.env.example` file to `.env` and update the environment variables accordingly
- Copy the `common/config.example.py` file to `common/config.py` and update the configuration accordingly

## Configuration 

**common/config.py**

> [!NOTE]
> `GuestTokenPayload` was designed using Singleton.  

- Update user information via initializer.

    ```python
    PAYLOAD.initialize(
        username="guest",
        rls_rules=[],
        resources=[],
        first_name="Guest",
        last_name="Guest"
    )
    ```

- **MUST** update RESOURCES variable according to your Superset resources.

    ```python
    RESOURCES = {
        Environment.DEV: [
            {"type": "dashboard", "id": "9b22e158-4d5d-435f-90d6-f5b46d1d53f0"}
        ],
    }
    ```

- **MUST** update RLS_RULES variable according to your needs.
- They are callable functions that return a dictionary. It **CAN** include `dataset` key but it **MUST** include the `clause` key. For more information, you can find the API documentation below.
- Callable functions takes `data` parameter which is a dictionary. This gives the opportunity to create dynamic rules. You can create it this dictionary variable in your api endpoints using path parameters and so on, like below.

    ```python
    # in common/config.py

    RLS_RULES = {
        Environment.DEV: [
            lambda data: { "dataset": 23, "clause": f"company_id = {data.get('company_id')}" },
        ],
    }

    # in app/api/routes.py

    @routes.route('/api/guest-token-by-company', methods=['GET'])
    def get_guest_token():
        company_id = request.args.get('company_id')

        # created data dictionary
        parameters = {
            "company_id": company_id
        }

        payload = GuestTokenPayload()

        # get payload data with dynamic RLS rules
        data = payload.get_payload_data(parameters)

        guest_token = create_guest_token(data)

        return jsonify(guest_token=guest_token)
    ```

**app/api/routes.py**

- Add more endpoints if you need 

    ```python
    @api.route("/guest-token", methods=["POST"])
    def get_guest_token():
        ...
    ```

**utils/environment.py**

- By default there are three environments: DEV, TEST and PROD. You can add more environments if you need.

    ```python
    class Environment(Enum):
        DEV = "dev"
        TEST = "test"
        PROD = "prod"
    ```

# Resources

- [Superset API](https://superset.apache.org/docs/api/)
- [Superset Embedded SDK](https://www.npmjs.com/package/@superset-ui/embedded-sdk)