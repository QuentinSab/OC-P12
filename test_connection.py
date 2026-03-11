from database import engine

with engine.connect() as connection:
    print("Connexion réussie.")
