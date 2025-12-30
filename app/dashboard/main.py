"""
DólarBot Analytics Dashboard
Dashboard interactivo para análisis de tipo de cambio
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd

# Importar funciones de data loader
from app.analytics.data_loader import (
    get_historical_data,
    get_data_by_origen,
    get_latest_by_origen,
    get_all_origenes,
    get_summary_stats,
    get_last_n_days,
)

# Configuración de la página
st.set_page_config(
    page_title="DólarBot Analytics",
    page_icon="💱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("💱 DólarBot Analytics")
st.markdown("Dashboard de análisis de tipo de cambio del dólar en Perú")

# Sidebar - Filtros
st.sidebar.header("⚙️ Filtros")

# Obtener orígenes disponibles
origenes = get_all_origenes()

if not origenes:
    st.error("❌ No se pudieron cargar los datos. Verifica tu conexión a Supabase.")
    st.stop()

# Filtro de origen
origen_seleccionado = st.sidebar.selectbox(
    "Selecciona origen:",
    ["Todos"] + origenes,
    index=0
)

# Filtro de período
periodo = st.sidebar.selectbox(
    "Período:",
    ["Última semana", "Último mes", "Últimos 3 meses", "Último año", "Todo"],
    index=1
)

# Mapear período a días
periodo_dias = {
    "Última semana": 7,
    "Último mes": 30,
    "Últimos 3 meses": 90,
    "Último año": 365,
    "Todo": None
}

# Cargar datos según filtros
if origen_seleccionado == "Todos":
    if periodo_dias[periodo]:
        df = get_last_n_days(periodo_dias[periodo])
    else:
        df = get_historical_data()
else:
    if periodo_dias[periodo]:
        df = get_last_n_days(periodo_dias[periodo], origen=origen_seleccionado)
    else:
        df = get_data_by_origen(origen_seleccionado)

if df.empty:
    st.warning("⚠️ No hay datos disponibles para los filtros seleccionados.")
    st.stop()

# ============================================
# SECCIÓN 1: MÉTRICAS PRINCIPALES
# ============================================
st.header("📊 Métricas Principales")

# Obtener últimos datos
df_latest = get_latest_by_origen()

if not df_latest.empty:
    # Encontrar mejor compra y venta
    mejor_compra = df_latest.loc[df_latest['precio_compra'].idxmax()]
    mejor_venta = df_latest.loc[df_latest['precio_venta'].idxmin()]
    
    # SUNAT actual
    sunat_latest = df_latest[df_latest['origen'] == 'SUNAT_API']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if not sunat_latest.empty:
            precio_sunat = sunat_latest.iloc[0]['precio_compra']
            st.metric(
                "💵 SUNAT Compra",
                f"S/ {precio_sunat:.4f}",
                help="Tipo de cambio oficial SUNAT"
            )
        else:
            st.metric("💵 SUNAT Compra", "N/A")
    
    with col2:
        if not sunat_latest.empty:
            precio_sunat_venta = sunat_latest.iloc[0]['precio_venta']
            st.metric(
                "💵 SUNAT Venta",
                f"S/ {precio_sunat_venta:.4f}",
                help="Tipo de cambio oficial SUNAT"
            )
        else:
            st.metric("💵 SUNAT Venta", "N/A")
    
    with col3:
        st.metric(
            "🏆 Mejor Compra",
            f"S/ {mejor_compra['precio_compra']:.4f}",
            help=f"{mejor_compra['origen']}"
        )
        st.caption(f"📍 {mejor_compra['origen']}")
    
    with col4:
        st.metric(
            "💰 Mejor Venta",
            f"S/ {mejor_venta['precio_venta']:.4f}",
            help=f"{mejor_venta['origen']}"
        )
        st.caption(f"📍 {mejor_venta['origen']}")

# ============================================
# SECCIÓN 2: GRÁFICO DE TENDENCIAS
# ============================================
st.header("📈 Tendencias Históricas")

# Tabs para diferentes vistas
tab1, tab2, tab3 = st.tabs(["Precio Compra", "Precio Venta", "Spread"])

with tab1:
    fig_compra = px.line(
        df,
        x='fecha',
        y='precio_compra',
        color='origen',
        title='Evolución del Precio de Compra',
        labels={'precio_compra': 'Precio (S/)', 'fecha': 'Fecha'},
        template='plotly_white'
    )
    fig_compra.update_layout(height=500)
    st.plotly_chart(fig_compra, use_container_width=True)

with tab2:
    fig_venta = px.line(
        df,
        x='fecha',
        y='precio_venta',
        color='origen',
        title='Evolución del Precio de Venta',
        labels={'precio_venta': 'Precio (S/)', 'fecha': 'Fecha'},
        template='plotly_white'
    )
    fig_venta.update_layout(height=500)
    st.plotly_chart(fig_venta, use_container_width=True)

with tab3:
    fig_spread = px.line(
        df,
        x='fecha',
        y='spread',
        color='origen',
        title='Evolución del Spread (Venta - Compra)',
        labels={'spread': 'Spread (S/)', 'fecha': 'Fecha'},
        template='plotly_white'
    )
    fig_spread.update_layout(height=500)
    st.plotly_chart(fig_spread, use_container_width=True)

# ============================================
# SECCIÓN 3: COMPARACIÓN DE CASAS DE CAMBIO
# ============================================
st.header("🏦 Comparación de Casas de Cambio")

if not df_latest.empty:
    col1, col2 = st.columns(2)
    
    with col1:
        # Top 5 mejores para comprar (mayor precio de compra)
        top_compra = df_latest.nlargest(5, 'precio_compra')[['origen', 'precio_compra']]
        
        fig_top_compra = px.bar(
            top_compra,
            x='precio_compra',
            y='origen',
            orientation='h',
            title='Top 5 - Mejores para Comprar Dólares',
            labels={'precio_compra': 'Precio Compra (S/)', 'origen': ''},
            color='precio_compra',
            color_continuous_scale='Greens'
        )
        fig_top_compra.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_top_compra, use_container_width=True)
    
    with col2:
        # Top 5 mejores para vender (menor precio de venta)
        top_venta = df_latest.nsmallest(5, 'precio_venta')[['origen', 'precio_venta']]
        
        fig_top_venta = px.bar(
            top_venta,
            x='precio_venta',
            y='origen',
            orientation='h',
            title='Top 5 - Mejores para Vender Dólares',
            labels={'precio_venta': 'Precio Venta (S/)', 'origen': ''},
            color='precio_venta',
            color_continuous_scale='Blues'
        )
        fig_top_venta.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_top_venta, use_container_width=True)

# ============================================
# SECCIÓN 4: ESTADÍSTICAS
# ============================================
st.header("📊 Estadísticas")

if origen_seleccionado == "Todos":
    stats = get_summary_stats()
else:
    stats = get_summary_stats(origen_seleccionado)

if stats:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Precio de Compra")
        st.metric("Promedio", f"S/ {stats['avg_compra']:.4f}")
        st.metric("Mínimo", f"S/ {stats['min_compra']:.4f}")
        st.metric("Máximo", f"S/ {stats['max_compra']:.4f}")
        st.metric("Volatilidad (σ)", f"{stats['volatilidad_compra']:.4f}")
    
    with col2:
        st.subheader("Precio de Venta")
        st.metric("Promedio", f"S/ {stats['avg_venta']:.4f}")
        st.metric("Mínimo", f"S/ {stats['min_venta']:.4f}")
        st.metric("Máximo", f"S/ {stats['max_venta']:.4f}")
        st.metric("Volatilidad (σ)", f"{stats['volatilidad_venta']:.4f}")
    
    st.divider()
    
    col3, col4, col5 = st.columns(3)
    with col3:
        st.metric("Total Registros", f"{stats['total_registros']:,}")
    with col4:
        st.metric("Fecha Inicio", stats['fecha_inicio'])
    with col5:
        st.metric("Fecha Fin", stats['fecha_fin'])

# ============================================
# SECCIÓN 5: TABLA DE DATOS
# ============================================
st.header("📋 Datos Detallados")

# Mostrar últimos registros
st.dataframe(
    df_latest[['origen', 'fecha', 'precio_compra', 'precio_venta', 'spread']]\
        .sort_values('precio_compra', ascending=False),
    use_container_width=True,
    hide_index=True
)

# Opción de descargar datos
st.download_button(
    label="📥 Descargar datos (CSV)",
    data=df.to_csv(index=False).encode('utf-8'),
    file_name=f'dolar_data_{datetime.now().strftime("%Y%m%d")}.csv',
    mime='text/csv',
)

# ============================================
# FOOTER
# ============================================
st.divider()
st.caption(f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.caption("Datos obtenidos de SUNAT y casas de cambio peruanas")
