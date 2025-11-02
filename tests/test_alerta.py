from app.utils.task_alerts import verificar_alertas

if __name__ == "__main__":
    # Simulamos un precio actual
    precio_actual = 3.50
    result = verificar_alertas.delay(precio_actual)
    print("Tarea enviada a Celery:", result.id,"result:", result.get(timeout=10))
