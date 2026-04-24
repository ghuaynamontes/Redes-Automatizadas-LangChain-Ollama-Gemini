import hvac
import os
from crewai import Agent, Task, Crew, LLM
from tools import ejecutar_ping, verificar_ip 

def obtener_secretos_vault():
    """Conecta con HashiCorp Vault y extrae la API Key de Gemini."""
    try:
        # Conexión al servidor local de Vault
        client = hvac.Client(url='http://127.0.0.1:8200', token='root')
        
        # Leer el secreto del path 'redes-automatizadas'
        read_response = client.secrets.kv.v2.read_secret_version(
            mount_point='secret',
            path='redes-automatizadas'
        )
        
        # Retornar la API KEY desde el diccionario de datos
        return read_response['data']['data']['GOOGLE_API_KEY']
    except Exception as e:
        print(f"❌ Error al conectar con Vault: {e}")
        return None

# --- FLUJO PRINCIPAL ---

# 1. Extraer la llave de forma segura desde Vault
api_key_segura = obtener_secretos_vault()

# 2. Configurar el motor de IA (Gemini 2.5) usando el envoltorio de CrewAI
# Usamos el prefijo 'google/' para garantizar el uso del conector estable
if api_key_segura:
    llm_final = LLM(
        model="google/gemini-2.5-flash-lite",
        api_key=api_key_segura
    )
else:
    llm_final = None

# 3. DEFINICIÓN DEL AGENTE
investigador_redes = Agent(
    role='Especialista en Redes Senior',
    goal='Diagnosticar la red local ejecutando comandos de Windows',
    backstory='Eres un experto técnico en infraestructura con acceso a consola real y gestión de secretos segura.',
    tools=[ejecutar_ping, verificar_ip], 
    llm=llm_final, 
    verbose=True,
    allow_delegation=False,
    memory=False
)

# 4. DEFINICIÓN DE LA TAREA
tarea_diagnostico = Task(
    description='Haz un ping a google.com y un ipconfig. Reporta los resultados en ESPAÑOL.',
    agent=investigador_redes,
    expected_output='Informe técnico de red con IP y latencia.'
)

# 5. CONFIGURACIÓN DEL EQUIPO
equipo_soporte = Crew(
    agents=[investigador_redes],
    tasks=[tarea_diagnostico],
    verbose=True
)

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 INICIANDO SISTEMA CON HASHICORP VAULT - GEMINI 2.5")
    print("="*50)
    
    # Verificación de seguridad antes de arrancar
    if not api_key_segura:
        print("❌ ERROR CRÍTICO: No se pudo obtener la llave desde Vault.")
        print("Asegúrate de que el servidor 'vault server -dev' esté corriendo.")
    else:
        try:
            resultado = equipo_soporte.kickoff()
            print("\n" + "="*30 + "\n✅ RESULTADO FINAL:\n" + "="*30)
            print(resultado)
        except Exception as e:
            print(f"\n❌ ERROR EN EJECUCIÓN: {str(e)}")