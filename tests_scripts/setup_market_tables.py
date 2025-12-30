"""
Script para crear las tablas de market data en Supabase.
Ejecuta la migración SQL directamente.
"""
from app.db.supabase.client import get_supabase_client
from pathlib import Path

def run_migration():
    """
    Ejecuta la migración SQL para crear las tablas de market data.
    """
    print("🚀 Iniciando migración de tablas de market data...\n")
    
    # Leer el archivo SQL
    migration_file = Path("app/db/migrations/create_market_data_tables.sql")
    
    if not migration_file.exists():
        print(f"❌ Error: No se encontró el archivo {migration_file}")
        return
    
    with open(migration_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    print("📄 SQL a ejecutar:")
    print("-" * 60)
    print(sql_content)
    print("-" * 60)
    print()
    
    try:
        supabase = get_supabase_client()
        
        # Ejecutar el SQL
        result = supabase.rpc('exec_sql', {'sql': sql_content}).execute()
        
        print("✅ Migración ejecutada exitosamente!")
        print("\nTablas creadas:")
        print("  - bcrp_data")
        print("  - market_data")
        print("\n✨ Listo para ingestar datos!")
        
    except Exception as e:
        print(f"❌ Error ejecutando migración: {e}")
        print("\n💡 Alternativa: Ejecuta el SQL manualmente en el SQL Editor de Supabase:")
        print("   1. Ve a tu proyecto en Supabase")
        print("   2. Abre el SQL Editor")
        print("   3. Copia y pega el contenido de:")
        print(f"      {migration_file}")
        print("   4. Ejecuta el query")

if __name__ == "__main__":
    run_migration()
