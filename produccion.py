import numpy as np
import pandas as pd

# Parámetros de la simulación
hours_per_day = 10  # La línea opera durante 10 horas al día
production_rate = 100  # Unidades producidas por hora
failure_rate = 1 / 8  # En promedio, ocurre un fallo cada 8 horas
repair_time = 0.5  # Tiempo promedio de reparación de una hora
maintenance_time = 1  # Una hora de mantenimiento programado
maintenance_interval = 5  # Se realiza mantenimiento cada 5 horas de operación

# Inicialización de variables
current_time = 0
total_production = 0
time_until_next_failure = np.random.exponential(1 / failure_rate)
time_until_maintenance = maintenance_interval
maintenance_done = False

# Registro de la simulación
log = []

# Simulación de la producción diaria
while current_time < hours_per_day:
    # El siguiente evento es un fallo o mantenimiento, lo que ocurra primero
    time_to_next_event = min(time_until_next_failure, time_until_maintenance)
    
    # Si el siguiente evento ocurre después de que acaba el turno, producir hasta el final
    if current_time + time_to_next_event >= hours_per_day:
        production_time = hours_per_day - current_time
        total_production += production_time * production_rate
        log.append({
            "Hora": current_time,
            "Evento": "Producción continua",
            "Tiempo de producción": production_time,
            "Producción acumulada": total_production
        })
        break
    
    # Actualizar el tiempo actual
    current_time += time_to_next_event
    
    # Caso 1: Fallo en la maquinaria
    if time_until_next_failure <= time_until_maintenance:
        # Producir hasta el momento del fallo
        total_production += time_to_next_event * production_rate
        log.append({
            "Hora": current_time,
            "Evento": "Fallo en la maquinaria",
            "Tiempo de producción": time_to_next_event,
            "Producción acumulada": total_production
        })
        
        # Tiempo de reparación
        current_time += repair_time
        
        # Registrar el tiempo de reparación
        log.append({
            "Hora": current_time,
            "Evento": "Reparación completada",
            "Tiempo de inactividad": repair_time,
            "Producción acumulada": total_production
        })
        
        # Reiniciar el tiempo hasta el siguiente fallo
        time_until_next_failure = np.random.exponential(1 / failure_rate)
    
    # Caso 2: Mantenimiento programado
    if time_until_maintenance < time_until_next_failure:
        # Producir hasta el mantenimiento
        total_production += time_to_next_event * production_rate
        log.append({
            "Hora": current_time,
            "Evento": "Mantenimiento programado",
            "Tiempo de producción": time_to_next_event,
            "Producción acumulada": total_production
        })
        
        # Tiempo de mantenimiento
        current_time += maintenance_time
        
        # Registrar el mantenimiento
        log.append({
            "Hora": current_time,
            "Evento": "Mantenimiento completado",
            "Tiempo de inactividad": maintenance_time,
            "Producción acumulada": total_production
        })
        
        # Reiniciar el tiempo hasta el siguiente mantenimiento
        time_until_maintenance = maintenance_interval
    
    # Reducir el tiempo hasta el siguiente evento (fallo o mantenimiento)
    time_until_next_failure -= time_to_next_event
    time_until_maintenance -= time_to_next_event

# Convertir los resultados en un DataFrame para su visualización
production_log = pd.DataFrame(log)

# Mostrar los primeros eventos de la simulación
print(production_log.head(10))

# Mostrar la producción total al final del día
print(f"\nProducción total al final del día: {total_production:.2f} unidades")
