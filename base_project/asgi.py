import os
import channels
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base_project.settings")
from channels.asgi import get_channel_layer



channel_layer = get_channel_layer()