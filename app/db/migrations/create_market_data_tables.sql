-- Tablas para datos de mercado (BCRP + Yahoo Finance)
-- Permite análisis de correlación entre variables macroeconómicas y tipo de cambio

-- Tabla para datos del BCRP (Banco Central de Reserva del Perú)
CREATE TABLE IF NOT EXISTS bcrp_data (
    id BIGSERIAL PRIMARY KEY,
    fecha DATE NOT NULL UNIQUE,
    tc_interbancario_venta DECIMAL(10, 4),
    tasa_interbancaria DECIMAL(10, 4),
    origen VARCHAR(50) DEFAULT 'BCRP_API',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla para datos internacionales (Yahoo Finance)
CREATE TABLE IF NOT EXISTS market_data (
    id BIGSERIAL PRIMARY KEY,
    fecha DATE NOT NULL UNIQUE,
    precio_cobre DECIMAL(10, 4),
    indice_dxy DECIMAL(10, 4),
    origen VARCHAR(50) DEFAULT 'YAHOO',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices para mejorar performance
CREATE INDEX idx_bcrp_fecha ON bcrp_data(fecha DESC);
CREATE INDEX idx_market_fecha ON market_data(fecha DESC);

-- Comentarios para documentación
COMMENT ON TABLE bcrp_data IS 'Datos diarios del Banco Central: tipo de cambio interbancario y tasa interbancaria';
COMMENT ON COLUMN bcrp_data.tc_interbancario_venta IS 'Tipo de cambio interbancario venta (USD/PEN)';
COMMENT ON COLUMN bcrp_data.tasa_interbancaria IS 'Tasa de interés interbancaria en soles';

COMMENT ON TABLE market_data IS 'Datos de mercados internacionales: cobre y índice dólar';
COMMENT ON COLUMN market_data.precio_cobre IS 'Precio de futuros de cobre (HG=F) en USD por libra';
COMMENT ON COLUMN market_data.indice_dxy IS 'Índice Dólar DXY (mide USD vs canasta de monedas)';
