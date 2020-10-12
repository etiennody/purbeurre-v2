import os

ENV = os.getenv('ENV', 'local')
if ENV == "local":
    from .dev import *
else:
    from .prod import *