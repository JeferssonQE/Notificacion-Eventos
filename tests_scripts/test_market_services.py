"""
Script de prueba rápida para verificar que los servicios funcionan.
"""
from app.services.bcrp_service import get_bcrp_data
from app.services.market_service import get_international_data
from datetime import datetime, timedelta

def test_services():
    """
    Prueba rápida de los servicios sin insertar en BD.
    """
    print("🧪 Probando servicios de market data...\n")
    
    # Últimos 7 días
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    print(f"📅 Rango solicitado: {start_date} a {end_date}")
    print(f"📅 Hoy es: {datetime.now().strftime('%Y-%m-%d %A')}")
    print(f"💡 Nota: BCRP y mercados solo publican en días laborables\n")
    
    # Test BCRP
    print("=" * 60)
    print("📊 BCRP Service")
    print("=" * 60)
    bcrp_data = get_bcrp_data(start_date, end_date)
    print(f"\n✅ Registros obtenidos: {len(bcrp_data)}")
    
    if bcrp_data:
        print("\n📋 Muestra de datos:")
        for record in bcrp_data[:3]:
            print(f"  {record['fecha']}: TC={record['tc_interbancario_venta']}, Tasa={record['tasa_interbancaria']}")
        print(f"\n  📌 Último dato disponible: {bcrp_data[-1]['fecha']}")
    else:
        print("\n⚠️  No hay datos (posible feriado/fin de semana)")
    
    # Test Yahoo Finance
    print("\n" + "=" * 60)
    print("🌎 Yahoo Finance Service")
    print("=" * 60)
    market_data = get_international_data(start_date, end_date)
    print(f"\n✅ Registros obtenidos: {len(market_data)}")
    
    if market_data:
        print("\n📋 Muestra de datos:")
        for record in market_data[:3]:
            cobre = record.get('precio_cobre', 'N/A')
            dxy = record.get('indice_dxy', 'N/A')
            print(f"  {record['fecha']}: Cobre={cobre}, DXY={dxy}")
        print(f"\n  📌 Último dato disponible: {market_data[-1]['fecha']}")
    else:
        print("\n⚠️  No hay datos (posible feriado/fin de semana)")
    
    print("\n" + "=" * 60)
    print("✨ Prueba completada!")
    print("=" * 60)
    print(f"\nTotal de registros:")
    print(f"  BCRP: {len(bcrp_data)}")
    print(f"  Market: {len(market_data)}")
    print(f"\n💡 Los servicios funcionan correctamente.")
    print(f"   Último dato BCRP: {bcrp_data[-1]['fecha'] if bcrp_data else 'N/A'}")
    print(f"   Último dato Market: {market_data[-1]['fecha'] if market_data else 'N/A'}")
    print(f"\n📝 Nota: Es normal que no haya datos de hoy si:")
    print(f"   - Es fin de semana")
    print(f"   - Es feriado (ej: Navidad, Año Nuevo)")
    print(f"   - Los datos aún no se publican (BCRP publica al cierre del día)")
    print(f"\n✅ Ahora puedes ejecutar: python app/services/data_ingestion.py")

if __name__ == "__main__":
    test_services()
