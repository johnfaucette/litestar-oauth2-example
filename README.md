## OAuth2 Example

This is an example of how to get OAuth2 Working with `litestar` and `httpx-oauth`.

### Running

```bash
# setup
poetry shell && poetry install

# start the app
uvicorn oauth2_example.app:create_app --reload
```

OAuth2 Flow: `http://localhost:8000/oauth2/github/login`, starts the oauth2 process chain.

Check the swagger docs: `http://localhost:8000/schema/swagger`.
