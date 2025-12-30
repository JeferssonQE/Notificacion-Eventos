"""
Cliente de Supabase para uso en servicios.
"""
from app.db.supabase.config import supabase

def get_supabase_client():
    """
    Retorna el cliente de Supabase configurado.
    Lanza excepción si no está disponible.
    """
    if supabase is None:
        raise Exception("Supabase client no está configurado. Verifica SUPABASE_URL y SUPABASE_API_KEY en .env")
    
    return supabase
