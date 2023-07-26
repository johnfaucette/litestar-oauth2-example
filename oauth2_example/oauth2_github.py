from typing import Dict, Any, cast, List
from litestar import Controller, get, Request
from litestar.response import Redirect
from litestar.exceptions import HTTPException
from httpx_oauth.oauth2 import OAuth2
from oauth2_example.settings import settings
import httpx
from pydantic import BaseModel

PROFILE_ENDPOINT = "https://api.github.com/user"
EMAILS_ENDPOINT = "https://api.github.com/user/emails"

github_client = OAuth2(
  client_id=settings.GITHUB_CLIENT_ID,
  client_secret=settings.GITHUB_CLIENT_SECRET,
  authorize_endpoint="https://github.com/login/oauth/authorize",
  access_token_endpoint="https://github.com/login/oauth/access_token",
  base_scopes=["user", "user:email"]
)

PROVIDERS = {
    'github' : github_client
}

class OAuth2Result(BaseModel):
    id: str
    email: str

def check_provider(provider: str) -> None:
    if provider not in PROVIDERS:
        raise HTTPException(detail=f"Unknown OAuth authenticator: {provider}", status_code=400)


class OAuth2Controller(Controller):
    path = "/oauth2"
    
    @get(path="/{provider:str}/login")
    async def login_via_provider(self, provider: str) -> Redirect:
        check_provider(provider)
        
        provider_client = PROVIDERS[provider]
        redirect_uri = f"http://localhost:8000/oauth2/{provider}/authorize"
        auth_url = await provider_client.get_authorization_url(redirect_uri=redirect_uri)
        return Redirect(path=auth_url, status_code=302)

    @get(path="/{provider:str}/authorize")
    async def authorize(self, code: str, provider: str, request: Request) -> OAuth2Result:
        check_provider(provider)

        provider_client = PROVIDERS[provider]
        redirect_uri = f"http://localhost:8000/oauth2/{provider}/authorize"

        # returns an OAuth2Token
        oauth2_token = await provider_client.get_access_token(code=code, redirect_uri=redirect_uri)
        access_token = oauth2_token['access_token']
        # result = await provider_client.get_id_email(access_token['access_token'])
        response = httpx.get(PROFILE_ENDPOINT, headers = {
            'Authorization' : f"token {access_token}"
        })
        if response.status_code >= 400:
            raise HTTPException(details=response.json(), status_code=400)
        data = cast(Dict[str, Any], response.json())

        id = data["id"]
        email = data.get("email")

        if email is None:
            # the user has no public email
            response = httpx.get(EMAILS_ENDPOINT, headers = {
                  'Authorization' : f"token {access_token}"
            })

            if response.status_code >= 400:
                raise HTTPException(details=response.json(), status_code=400)

            emails = cast(List[Dict[str, Any]], response.json())

            email = emails[0]["email"]

        return OAuth2Result(id=str(id), email=email)
        