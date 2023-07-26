from litestar import Litestar
from oauth2_example.oauth2_github import OAuth2Controller
from oauth2_example.settings import settings


def create_app() -> Litestar:

  # route handlers
  route_handlers = [
    OAuth2Controller
  ]

  app = Litestar(route_handlers=route_handlers, debug=settings.DEBUG)
  
  return app
