"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# application = get_asgi_application()



import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

from chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    # Just HTTP for now. (We can add other protocols later.)
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
    ),    
})


# This root routing configuration specifies that when a connection is made to the Channels development server, 
# the ProtocolTypeRouter will first inspect the type of connection. 
# If it is a WebSocket connection (ws:// or wss://), the connection will be given to the AuthMiddlewareStack.
# The AuthMiddlewareStack will populate the connection’s scope with a reference to the currently authenticated user, 
# similar to how Django’s AuthenticationMiddleware populates the request object of a view function with the currently authenticated user. 
# Then the connection will be given to the URLRouter.
# The URLRouter will examine the HTTP path of the connection to route it to a particular consumer, based on the provided url patterns.


# Configure SSL/TLS certificates ?
#from daphne.server import HTTPFactory

# Path to your SSL/TLS certificate and private key files
ssl_certfile = '/etc/letsencrypt/live/mihai-corciu.go.ro/fullchain.pem'
ssl_keyfile = '/etc/letsencrypt/live/mihai-corciu.go.ro/privkey.pem'

# # Create Daphne HTTP factory with SSL/TLS support
# http_factory = HTTPFactory(
#     application,
#     certfile=ssl_certfile,
#     keyfile=ssl_keyfile
# )

# # Assign the HTTP factory to the ASGI application
# application = http_factory

