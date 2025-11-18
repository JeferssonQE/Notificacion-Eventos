from supabase import create_client, Client
from dotenv import load_dotenv
import os
from app.core.config import settings

load_dotenv()

SUPABASE_URL = settings.SUPABASE_URL
SUPABASE_KEY = settings.SUPABASE_API_KEY

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

if __name__ == "__main__":
    print("Supabase client created successfully.")
    result = supabase.table("dolar").select("*").execute()
    print("Data from 'dolar' table:", result.data)