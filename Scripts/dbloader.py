import os
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

data = "./Data_Source"

def get_engine():
    url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(url)

def import_all_csv(engine):
    csv_files = [file for file in os.listdir(data) if file.endswith(".csv")]
    
    if not csv_files:
        print("❌ Aucun fichier CSV trouvé dans ./data")
        return

    print(f"📂 {len(csv_files)} fichiers CSV trouvés\n")

    for filename in csv_files:
        table_name = os.path.splitext(filename)[0].lower().replace(" ", "_").replace("-", "_")
        filepath = os.path.join(data, filename)

        try:
            df = pd.read_csv(filepath)
            df.to_sql(
                name=table_name,
                con=engine,
                if_exists="replace",  # ou "append" si tu ne veux pas écraser
                index=False
            )
            print(f"✅ {filename} → table '{table_name}' ({len(df)} lignes)")
        except Exception as e:
            print(f"❌ Erreur sur {filename} : {e}")

if __name__ == "__main__":
    print("🔌 Connexion à PostgreSQL...")
    engine = get_engine()
    print("✅ Connecté !\n")
    import_all_csv(engine)
    print("\n🎉 Import terminé !")