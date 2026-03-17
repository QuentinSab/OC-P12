from database.connection import engine

with engine.connect() as connection:
    print("Connexion réussie.")
