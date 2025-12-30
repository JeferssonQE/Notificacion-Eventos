"""
Celery tasks para Data Analytics Pipeline
Tareas asíncronas para scraping, análisis y reportes
"""
from app.celery.config import celery_app
from datetime import datetime, timedelta


# ===== TAREAS DE SCRAPING =====

@celery_app.task(name="tasks.scrape_hourly_casas")
def scrape_hourly_casas():
    """Scrapea precios de casas de cambio (ejecutado por workflow)"""
    from app.scraper.hourly_scraper import scrape_and_store_hourly
    
    try:
        result = scrape_and_store_hourly()
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@celery_app.task(name="tasks.ingest_daily_data")
def ingest_daily_data():
    """Ingesta datos diarios de BCRP y Market (últimos 3 días para asegurar días hábiles)"""
    from app.services.data_ingestion import ingest_recent
    
    try:
        ingest_recent()  # Últimos 3 días en lugar de solo hoy
        return {"status": "success", "message": "Datos diarios ingestados"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


# ===== TAREAS DE ANÁLISIS =====

@celery_app.task(name="tasks.calculate_analytics")
def calculate_analytics(days: int = 7):
    """Calcula métricas de analytics para todas las casas"""
    from app.analytics.price_analysis import analyze_all_casas
    
    try:
        analysis = analyze_all_casas(days=days)
        return {
            "status": "success",
            "casas_analyzed": len(analysis),
            "data": analysis
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


@celery_app.task(name="tasks.detect_arbitrage")
def detect_arbitrage():
    """Detecta oportunidades de arbitraje"""
    from app.analytics.price_analysis import get_best_opportunities
    
    try:
        opportunities = get_best_opportunities()
        
        # Si hay arbitraje, podría enviar alerta
        if opportunities.get("arbitrage", {}).get("possible"):
            print(f"🚀 ARBITRAJE DETECTADO: {opportunities['arbitrage']}")
        
        return {"status": "success", "opportunities": opportunities}
    except Exception as e:
        return {"status": "error", "error": str(e)}


# ===== TAREAS DE REPORTES =====

@celery_app.task(name="tasks.generate_daily_report")
def generate_daily_report():
    """Genera y envía reporte diario por email"""
    from app.services.infrastructure.test_gmail import send_gmail_with_dolar
    
    try:
        send_gmail_with_dolar()
        return {"status": "success", "message": "Reporte enviado"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@celery_app.task(name="tasks.generate_weekly_summary")
def generate_weekly_summary():
    """Genera resumen semanal con insights profundos"""
    from app.analytics.price_analysis import analyze_all_casas
    
    try:
        analysis = analyze_all_casas(days=7)
        
        # Aquí podrías generar un PDF o enviar un email especial
        summary = {
            "period": "weekly",
            "casas_count": len(analysis),
            "most_volatile": sorted(analysis, key=lambda x: x.get("volatility_compra", 0), reverse=True)[:3],
            "most_stable": sorted(analysis, key=lambda x: x.get("volatility_compra", 0))[:3],
            "timestamp": datetime.now().isoformat()
        }
        
        return {"status": "success", "summary": summary}
    except Exception as e:
        return {"status": "error", "error": str(e)}


# ===== TAREAS DE LIMPIEZA =====

@celery_app.task(name="tasks.cleanup_old_data")
def cleanup_old_data(days_to_keep: int = 90):
    """Limpia datos antiguos para optimizar storage"""
    from app.db.supabase.client import get_supabase_client
    
    try:
        supabase = get_supabase_client()
        cutoff_date = (datetime.now() - timedelta(days=days_to_keep)).strftime("%Y-%m-%d")
        
        # Eliminar datos horarios antiguos (mantener solo últimos 90 días)
        result = supabase.table("dolar_hourly")\
            .delete()\
            .lt("fecha", cutoff_date)\
            .execute()
        
        return {
            "status": "success",
            "message": f"Datos anteriores a {cutoff_date} eliminados",
            "deleted_count": len(result.data) if result.data else 0
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


# ===== TAREAS DE PRUEBA =====

@celery_app.task(name="tasks.health_check")
def health_check():
    """Verifica que Celery esté funcionando"""
    return {
        "status": "healthy",
        "message": "✅ Celery está funcionando correctamente",
        "timestamp": datetime.now().isoformat()
    }
