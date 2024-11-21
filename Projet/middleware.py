from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class SessionPerAppMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Si l'URL commence par "parcoursup", on change le cookie de session
        if request.path.startswith("/parcoursup"):
            settings.SESSION_COOKIE_NAME = "session_parcoursup"
        elif request.path.startswith("/ecole"):
            settings.SESSION_COOKIE_NAME = "session_ecole"
        else:
            settings.SESSION_COOKIE_NAME = "sessionid"