from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from Apps.Chat import routing as chat_routing
from Apps.LiveStream import routing as live_routing
from Apps.Notifications import routing as notify_routing
from Apps.Robotarium import routing as robotarium_routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat_routing.websocket_urlpatterns +
            live_routing.websocket_urlpatterns +
            notify_routing.websocket_urlpatterns +
            robotarium_routing.websocket_urlpatterns
        ),
    ),
    'http': URLRouter(notify_routing.urlpatterns),
})
