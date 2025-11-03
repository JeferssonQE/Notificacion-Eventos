from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.domain.evento_service import EventoService
from app.services.domain.recordatorio_dolar_service import RecordatorioDolarService
from app.services.domain.dolar_service import DolarService
from app.services.infrastructure.whatsapp.whatsapp_service import send_whatsapp_template
from datetime import datetime, timedelta
from typing import List

class SchedulerService:
    def __init__(self, db: Session):
        self.db = db
        self.evento_service = EventoService(db)
        self.recordatorio_service = RecordatorioDolarService(db)
        self.dolar_service = DolarService(db)

    def verificar_eventos_pendientes(self) -> List[dict]:
        """
        Verifica eventos que deben ejecutarse en la fecha/hora actual
        """
        ahora = datetime.now()
        eventos_activados = []
        
        # Aquí implementarías la lógica para verificar eventos
        # Por ejemplo, eventos programados para esta hora
        # eventos = self.evento_service.listar_eventos_por_fecha(ahora.date())
        
        return eventos_activados

    def verificar_alertas_dolar(self) -> List[dict]:
        """
        Verifica si hay alertas de dólar que deben activarse
        """
        alertas_activadas = []
        
        try:
            # Obtener el último precio del dólar
            ultimo_dolar = self.dolar_service.obtener_ultimos_dolares_todos_origenes()
            
            if ultimo_dolar:
                for dolar in ultimo_dolar:
                    # Verificar recordatorios que se activan con este precio
                    recordatorios = self.recordatorio_service.listar_todos_recordatorios()
                    
                    for recordatorio in recordatorios:
                        if self._debe_activar_alerta(recordatorio, dolar.precio_venta):
                            alertas_activadas.append({
                                'recordatorio': recordatorio,
                                'dolar': dolar,
                                'mensaje': f"🚨 Alerta: El dólar {recordatorio.movimiento} a {dolar.precio_venta}"
                            })
                            
                            # Enviar notificación
                            self._enviar_notificacion_alerta(recordatorio, dolar)
        
        except Exception as e:
            print(f"Error verificando alertas de dólar: {e}")
        
        return alertas_activadas

    def _debe_activar_alerta(self, recordatorio, precio_actual: float) -> bool:
        """
        Determina si una alerta debe activarse basada en el recordatorio y precio actual
        """
        try:
            valor_objetivo = float(recordatorio.valor)
            porcentaje_objetivo = float(recordatorio.porcentaje)
            
            if recordatorio.movimiento == "sube":
                return precio_actual >= valor_objetivo
            elif recordatorio.movimiento == "baja":
                return precio_actual <= valor_objetivo
                
        except (ValueError, TypeError):
            return False
        
        return False

    def _enviar_notificacion_alerta(self, recordatorio, dolar):
        """
        Envía notificación de alerta por WhatsApp
        """
        try:
            mensaje = f"🚨 Alerta de Dólar\n\n" \
                     f"El dólar {recordatorio.movimiento} a {dolar.precio_venta}\n" \
                     f"Origen: {dolar.origen}\n" \
                     f"Fecha: {dolar.fecha}"
            
            # Aquí enviarías la notificación
            # send_whatsapp_template(recordatorio.numero, ...)
            
        except Exception as e:
            print(f"Error enviando notificación: {e}")

    def ejecutar_tareas_programadas(self):
        """
        Ejecuta todas las tareas programadas
        """
        print(f"🕐 Ejecutando tareas programadas: {datetime.now()}")
        
        # Verificar eventos
        eventos = self.verificar_eventos_pendientes()
        if eventos:
            print(f"📅 Eventos activados: {len(eventos)}")
        
        # Verificar alertas de dólar
        alertas = self.verificar_alertas_dolar()
        if alertas:
            print(f"🚨 Alertas activadas: {len(alertas)}")
        
        return {
            'eventos_activados': len(eventos),
            'alertas_activadas': len(alertas),
            'timestamp': datetime.now()
        }
