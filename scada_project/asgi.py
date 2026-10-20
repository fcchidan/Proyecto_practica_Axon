import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import telemetry.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scada_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            telemetry.routing.websocket_urlpatterns
        )
    ),
})