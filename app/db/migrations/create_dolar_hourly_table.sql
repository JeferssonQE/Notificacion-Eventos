-- Tabla para almacenar datos horarios de casas de cambio
-- Permite análisis de variaciones de precios durante el día

CREATE TABLE IF NOT EXISTS dolar_hourly (
    id BIGSERIAL PRIMARY KEY,
    origen VARCHAR(100) NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    precio_compra DECIMAL(10, 4) NOT NULL,
    precio_venta DECIMAL(10, 4) NOT NULL,
    spread DECIMAL(10, 4),
    url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices para mejorar performance de consultas
CREATE INDEX idx_dolar_hourly_origen ON dolar_hourly(origen);
CREATE INDEX idx_dolar_hourly_fecha ON dolar_hourly(fecha);
CREATE INDEX idx_dolar_hourly_timestamp ON dolar_hourly(timestamp DESC);
CREATE INDEX idx_dolar_hourly_origen_timestamp ON dolar_hourly(origen, timestamp DESC);

-- Índice compuesto para consultas de análisis
CREATE INDEX idx_dolar_hourly_analysis ON dolar_hourly(origen, fecha, timestamp);

-- Comentarios para documentación
COMMENT ON TABLE dolar_hourly IS 'Almacena capturas horarias del tipo de cambio de casas de cambio para análisis de variaciones';
COMMENT ON COLUMN dolar_hourly.spread IS 'Diferencia entre precio de venta y compra (venta - compra)';
COMMENT ON COLUMN dolar_hourly.timestamp IS 'Timestamp exacto de la captura (incluye hora, minuto, segundo)';
