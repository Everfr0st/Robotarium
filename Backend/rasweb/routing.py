from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from Apps.Chat import routing as chat_routing
from Apps.LiveStream import routing as live_routing


application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat_routing.websocket_urlpatterns +
            live_routing.websocket_urlpatterns

        ),
    ),
})