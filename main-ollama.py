import os
from crewai import Agent, Task, Crew, LLM
from tools import ejecutar_ping, verificar_ip 

# 1. CONFIGURACIÓN OLLAMA (Usando Llama 3.1 que SÍ soporta tools)
mi_llm_local = LLM(
    model="ollama/llama3.1",
    base_url="http://localhost:11434"
)

# 2. AGENTE
investigador_redes = Agent(
    role='Especialista en Soporte de Redes',
    goal='Diagnosticar la red local usando comandos de Windows',
    backstory='Eres un experto técnico que usa la consola para resolver problemas.',
    tools=[ejecutar_ping, verificar_ip], 
    llm=mi_llm_local,
    verbose=True,
    allow_delegation=False
)

# 3. TAREA
tarea_diagnostico = Task(
    description='Ejecuta un ping a google.com y un ipconfig. Resume los resultados.',
    agent=investigador_redes,
    expected_output='Informe técnico de red.'
)

# 4. EQUIPO
equipo_soporte = Crew(
    agents=[investigador_redes],
    tasks=[tarea_diagnostico],
    verbose=True
)

if __name__ == "__main__":
    print("\n🚀 INICIANDO AGENTE LOCAL CON LLAMA 3.1")
    try:
        resultado = equipo_soporte.kickoff()
        print("\n✅ RESULTADO FINAL:\n", resultado)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")