import pandas as pd
import os 
def load_data(df):
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/jobs_processed.csv", index=False, encoding="utf-8-sig")
    print("Datos procesados guardados en data/processed/jobs_processed.csv")
    
    
