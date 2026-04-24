import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import ejecutar_ping, verificar_ip 

# 1. CARGA DE VARIABLES DE ENTORNO
# load_dotenv() busca el archivo .env y carga las variables en os.environ
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# 2. CONFIGURACIÓN DEL MOTOR (LangChain + Gemini 2.5)
# Mantenemos ChatGoogleGenerativeAI para asegurar que el SDK de Google responda correctamente
llm_langchain = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=api_key,
    temperature=0.3
)

# 3. ENVOLTORIO PARA CREWAI (Solución para Pydantic y versiones de modelo)
# Usamos el prefijo 'google/' para que CrewAI utilice el conector estable
llm_final = LLM(
    model="google/gemini-2.5-flash-lite",
    api_key=api_key
)

# 4. DEFINICIÓN DEL AGENTE
# Como investigador en ingeniería de redes, este agente usará tus herramientas personalizadas
investigador_redes = Agent(
    role='Especialista en Redes Senior',
    goal='Diagnosticar la red local ejecutando comandos de Windows',
    backstory='Eres un experto técnico en infraestructura con acceso a consola real.',
    tools=[ejecutar_ping, verificar_ip], 
    llm=llm_final, 
    verbose=True,
    allow_delegation=False,
    memory=False
)

# 5. TAREA
tarea_diagnostico = Task(
    description='Haz un ping a google.com y un ipconfig. Reporta los resultados en ESPAÑOL.',
    agent=investigador_redes,
    expected_output='Informe técnico de red con IP y latencia.'
)

# 6. EQUIPO
equipo_soporte = Crew(
    agents=[investigador_redes],
    tasks=[tarea_diagnostico],
    verbose=True
)

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 INICIANDO SISTEMA AUTOMATIZADO - MODELO GEMINI 2.5")
    print("="*50)
    
    if not api_key:
        print("❌ ERROR: No se encontró la GOOGLE_API_KEY en el archivo .env")
    else:
        try:
            resultado = equipo_soporte.kickoff()
            print("\n" + "="*30 + "\n✅ RESULTADO FINAL:\n" + "="*30)
            print(resultado)
        except Exception as e:
            print(f"\n❌ ERROR EN EJECUCIÓN: {str(e)}")