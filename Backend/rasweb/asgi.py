import os

import django_eventstream
from django.conf.urls import url
from django.core.asgi import get_asgi_application

# Fetch Django ASGI application early to ensure AppRegistry is populated
# before importing consumers and AuthMiddlewareStack that may import ORM
# models.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rasweb.settings")
django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from Apps.Chat import routing as chat_routing
from Apps.LiveStream import routing as live_routing
from Apps.Notifications import routing as notify_routing
from Apps.Robotarium import routing as robotarium_routing

application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    'http': URLRouter([
        url(r'^notifications/', AuthMiddlewareStack(
            URLRouter(django_eventstream.routing.urlpatterns)
        ), {'channels': ['posts']}),
        django_asgi_app,
    ]),
    # WebSocket chat handler
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat_routing.websocket_urlpatterns +
            live_routing.websocket_urlpatterns +
            notify_routing.websocket_urlpatterns +
            robotarium_routing.websocket_urlpatterns
        ),
    ),
})
