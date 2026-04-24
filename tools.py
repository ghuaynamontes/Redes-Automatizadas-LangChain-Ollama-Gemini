import os
from crewai.tools import tool

@tool("ejecutar_ping")
def ejecutar_ping(host: str):
    """
    Ejecuta un comando ping hacia un host específico en Windows.
    Útil para medir latencia y pérdida de paquetes.
    """
    # El comando 'ping -n 4' es específico para Windows
    response = os.popen(f"ping -n 4 {host}").read()
    return response

@tool("verificar_ip")
def verificar_ip():
    """
    Obtiene la configuración IP local completa mediante el comando ipconfig.
    Útil para conocer la IP privada, máscara de subred y puerta de enlace.
    """
    return os.popen("ipconfig").read()