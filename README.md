# Superset Guest Service

Superset Guest Service is a lightweight middleware that employs the connector pattern to seamlessly integrate with Superset, streamlining the process of efficiently retrieving guest tokens.

# Prerequisites

- [Python](https://www.python.org/downloads/) 
- [Docker](https://docs.docker.com/get-docker/)

# Run

:warning **Note:** For testing alerts.

- Clone the repository
- Copy the `.env.example` file to `.env` and update the environment variables accordingly
- Copy the `common/config.example.py` file to `common/config.py` and update the configuration accordingly
    - :info `GuestTokenPayload` was designed using Singleton. You can update user information via initializer.
    ```python
        PAYLOAD.initialize(
            username="guest",
            rls_rules=[],
            resources=[],
            first_name="Guest",
            last_name="Guest"
        )
    ```

# Resources

- [Superset API](https://superset.apache.org/docs/api/)
- [Superset Embedded SDK](https://www.npmjs.com/package/@superset-ui/embedded-sdk)