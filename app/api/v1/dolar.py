from fastapi import APIRouter, HTTPException, Query
from datetime import date, datetime, timedelta
from typing import Optional
from app.db.supabase.client import get_supabase_client
from app.analytics.price_analysis import (
    analyze_all_casas,
    get_best_opportunities,
    get_casa_history
)

router = APIRouter()


@router.get("/casas/latest")
def get_latest_casas_prices():
    """Obtiene los precios más recientes de todas las casas de cambio"""
    try:
        supabase = get_supabase_client()
        
        # Obtener el último registro de cada casa
        result = supabase.rpc('get_latest_prices_by_casa').execute()
        
        if not result.data:
            # Fallback: obtener últimos registros manualmente
            result = supabase.table("dolar_hourly")\
                .select("*")\
                .order("timestamp", desc=True)\
                .limit(20)\
                .execute()
        
        return {"data": result.data, "count": len(result.data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/casas/history/{casa_name}")
def get_casa_price_history(
    casa_name: str,
    days: int = Query(7, ge=1, le=90, description="Días de historial (1-90)")
):
    """Obtiene el historial de precios de una casa específica"""
    try:
        history = get_casa_history(casa_name, days)
        return {"casa": casa_name, "days": days, "data": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/casas/analytics")
def get_casas_analytics(
    days: int = Query(7, ge=1, le=30, description="Días para análisis (1-30)")
):
    """Análisis estratégico de todas las casas de cambio"""
    try:
        analysis = analyze_all_casas(days)
        return {"days": days, "total_casas": len(analysis), "data": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/casas/opportunities")
def get_trading_opportunities():
    """Obtiene las mejores oportunidades de compra/venta y arbitraje"""
    try:
        opportunities = get_best_opportunities()
        return opportunities
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/bcrp/latest")
def get_latest_bcrp_data():
    """Obtiene los datos más recientes del BCRP"""
    try:
        supabase = get_supabase_client()
        result = supabase.table("bcrp_data")\
            .select("*")\
            .order("fecha", desc=True)\
            .limit(1)\
            .execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="No hay datos del BCRP")
        
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/bcrp/history")
def get_bcrp_history(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: int = Query(30, ge=1, le=365)
):
    """Obtiene historial de datos del BCRP"""
    try:
        supabase = get_supabase_client()
        query = supabase.table("bcrp_data").select("*")
        
        if start_date:
            query = query.gte("fecha", start_date.isoformat())
        if end_date:
            query = query.lte("fecha", end_date.isoformat())
        
        result = query.order("fecha", desc=True).limit(limit).execute()
        
        return {"data": result.data, "count": len(result.data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/market/latest")
def get_latest_market_data():
    """Obtiene los datos más recientes del mercado internacional (Cobre, DXY)"""
    try:
        supabase = get_supabase_client()
        result = supabase.table("market_data")\
            .select("*")\
            .order("fecha", desc=True)\
            .limit(1)\
            .execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="No hay datos de mercado")
        
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/market/history")
def get_market_history(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: int = Query(30, ge=1, le=365)
):
    """Obtiene historial de datos del mercado internacional"""
    try:
        supabase = get_supabase_client()
        query = supabase.table("market_data").select("*")
        
        if start_date:
            query = query.gte("fecha", start_date.isoformat())
        if end_date:
            query = query.lte("fecha", end_date.isoformat())
        
        result = query.order("fecha", desc=True).limit(limit).execute()
        
        return {"data": result.data, "count": len(result.data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard/summary")
def get_dashboard_summary():
    """Resumen completo para dashboard: BCRP, Market, Casas y Oportunidades"""
    try:
        supabase = get_supabase_client()
        
        # BCRP latest
        bcrp = supabase.table("bcrp_data")\
            .select("*")\
            .order("fecha", desc=True)\
            .limit(1)\
            .execute()
        
        # Market latest
        market = supabase.table("market_data")\
            .select("*")\
            .order("fecha", desc=True)\
            .limit(1)\
            .execute()
        
        # Casas analytics
        casas_analysis = analyze_all_casas(days=7)
        
        # Opportunities
        opportunities = get_best_opportunities()
        
        return {
            "bcrp": bcrp.data[0] if bcrp.data else None,
            "market": market.data[0] if market.data else None,
            "casas_count": len(casas_analysis),
            "opportunities": opportunities,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
