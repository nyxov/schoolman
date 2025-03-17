#from channels.routing import ProtocolTypeRouter, URLRouter

class AuthASGIMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Проверяем авторизацию пользователя
        if scope["type"] == "http":
            user = scope.get("user")
            if not user or not user.is_authenticated:
                await send({
                    "type": "http.response.start",
                    "status": 401,
                    "headers": [(b"content-type", b"text/plain")],
                })
                await send({
                    "type": "http.response.body",
                    "body": b"Unauthorized",
                })
                return
        
        await self.app(scope, receive, send)