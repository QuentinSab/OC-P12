from database.connection import engine
from database.base import Base
from models.user import User  # Models to import # noqa: F401
from models.departement import Departement  # Models to import # noqa: F401
from models.client import Client  # Models to import # noqa: F401


Base.metadata.create_all(bind=engine)
print("Base initialisée.")
