#!/usr/bin/env python3
# -- coding: utf-8 --
import sys
import subprocess
import pkg_resources
import os
import json
import re
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress
from rich.markdown import Markdown
from rich.style import Style

# Verificación de dependencias
REQUIRED_PACKAGES = ["requests>=2.31.0", "openai>=1.0.0", "rich>=13.0.0"]

def verificar_dependencias():
    """Verifica si las dependencias están instaladas y las instala si es necesario."""
    try:
        pkg_resources.require(REQUIRED_PACKAGES)
    except pkg_resources.DistributionNotFound as e:
        console.print(f"[bold red]❌ Dependencia faltante: {e}[/bold red]")
        console.print("[bold yellow]Instalando dependencias...[/bold yellow]")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        console.print("[bold green]✅ Dependencias instaladas correctamente.[/bold green]")
    except pkg_resources.VersionConflict as e:
        console.print(f"[bold red]❌ Versión incorrecta de dependencia: {e}[/bold red]")
        console.print("[bold yellow]Actualizando dependencias...[/bold yellow]")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "-r", "requirements.txt"])
        console.print("[bold green]✅ Dependencias actualizadas correctamente.[/bold green]")

# Verifica si el script se está ejecutando dentro de un entorno virtual
def verificar_entorno_virtual():
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        console.print("[bold yellow]⚡ No se detectó un entorno virtual. Creando y activando uno...[/bold yellow]")
        crear_entorno_virtual()
    else:
        console.print("[bold green]✅ Entorno virtual ya activado.[/bold green]")

# Crear entorno virtual
def crear_entorno_virtual():
    venv_dir = "myenv"
    if not os.path.exists(venv_dir):
        subprocess.check_call([sys.executable, "-m", "venv", venv_dir])
        console.print(f"[bold green]✅ Entorno virtual creado en: {venv_dir}[/bold green]")
    else:
        console.print(f"[bold yellow]⚡ El entorno virtual ya existe: {venv_dir}[/bold yellow]")
    
    # Activar el entorno virtual
    activar_entorno_virtual(venv_dir)

# Activar entorno virtual
def activar_entorno_virtual(venv_dir):
    activate_script = os.path.join(venv_dir, "bin", "activate")
    if sys.platform == "win32":
        activate_script = os.path.join(venv_dir, "Scripts", "activate.bat")
    if os.path.exists(activate_script):
        subprocess.check_call([activate_script])
        console.print(f"[bold green]✅ Entorno virtual activado.[/bold green]")
    else:
        console.print(f"[bold red]❌ No se pudo activar el entorno virtual.[/bold red]")

# Instalar las dependencias necesarias dentro del entorno virtual
def instalar_dependencias():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openai", "requests", "rich"])

# Configuración Rich
console = Console()

BANNER = """
[bold cyan]
 __    __      _ _         __    __ _                  _ 
/ / /\ \ \_ __(_) |_ ___  / / /\ \ (_)______ _ _ __ __| |
\ \/  \/ / '__| | __/ _ \ \ \/  \/ / |_  / _` | '__/ _` |
 \  /\  /| |  | | ||  __/  \  /\  /| |/ / (_| | | | (_| |
  \/  \/ |_|  |_|\__\___|   \/  \/ |_/___\__,_|_|  \__,_|

---- By: MARH -------------------------------------------
"""
def generar_writeup(nombre_maquina, ip):
    """Genera un write-up profesional usando DeepSeek"""
    system_msg = f"""Eres un experto en CTFs y pentesting. Para {nombre_maquina} ({ip}), genera:
1. *Reconocimiento*: Comandos de escaneo (nmap, masscan)
2. *Enumeración*: Técnicas específicas por servicio
3. *Explotación*: 3 métodos con payloads actualizados
4. *Post-Explotación*: Comandos de pivoting
5. *Escalada*: 2 vías de escalada (kernel/sudo)
6. *Hardening*: Recomendaciones de seguridad

Formato: Markdown con tabs de código ejecutables"""

    with Progress() as progress:
        task = progress.add_task("[cyan]Generando write-up...", total=100)
        while not progress.finished:
            progress.update(task, advance=10)
            response = client.chat.completions.create(
                model="deepseek-reasoner",
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": f"Genera write-up para {nombre_maquina}"}
                ],
                temperature=0.3,
                max_tokens=3000
            )
            progress.update(task, completed=100)
    
    return response.choices[0].message.content

def main():
    # Verificar entorno virtual
    verificar_entorno_virtual()

    # Instalar dependencias si es necesario
    instalar_dependencias()

    # Continuar con el resto del código
    maquina = console.input("\n🔧 [bold]Nombre de la máquina: [/bold]").strip()
    ip = console.input("🌐 [bold]Dirección IP: [/bold]").strip()
    
    while True:
        # Mostrar el menú y ejecutar las opciones
        mostrar_menu()
        opcion = console.input("\n⚡ [bold]Selecciona opción: [/bold]")
        
        if opcion == "1":
            console.print(f"\n📜 [bold]Generando write-up para {maquina}...[/bold]\n")
            writeup = generar_writeup(maquina, ip)
            console.print(Markdown(writeup))
        elif opcion == "2":
            puerto = console.input("🔦 [bold]Puerto a analizar (ej: 445): [/bold]")
            console.print(f"\n🔎 [bold]Análisis de {ip}:{puerto}:[/bold]\n")
            analisis = analizar_puerto(ip, puerto)
            console.print(Panel.fit(analisis, style="bold green"))
        elif opcion == "3":
            console.print(f"\n🤖 [bold]Iniciando modo automático para {ip}...[/bold]\n")
            script = modo_automatico(ip)
            console.print(Panel.fit(script, style="bold yellow"))
        elif opcion == "4":
            writeup = generar_writeup(maquina, ip)
            exportar_writeup(writeup, maquina)
        elif opcion == "5":
            console.print("\n🧙‍♂️ [bold cyan]¡WriteWizard ha completado su magia! Saliendo...[/bold cyan]")
            break

if __name__ == "__main__":
    main()
