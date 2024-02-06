from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import eProc_Chat.routing

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
                URLRouter(
                    eProc_Chat.routing.websocket_urlpatterns
                )
    ),
})