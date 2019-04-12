#from channels.staticfiles import StaticFilesConsumer
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import eventos.routing

application = ProtocolTypeRouter({
    #'http.request': StaticFilesConsumer(),
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            eventos.routing.websocket_urlpatterns
        )
    ),
})
