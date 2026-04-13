from database.connection import engine
from database.base import Base

# Models to import
from models.user import User  # noqa: F401
from models.departement import Departement  # noqa: F401
from models.client import Client  # noqa: F401
from models.contract import Contract  # noqa: F401
from models.event import Event  # noqa: F401


Base.metadata.create_all(bind=engine)
print("Base initialisée.")
