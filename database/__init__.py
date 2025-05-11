# database/__init__.py

from .db import get_connection, release_connection, close_pool
from .models import create_tables
