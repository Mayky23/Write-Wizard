#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import subprocess
import os
from importlib.metadata import distribution, PackageNotFoundError, version
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from rich.markdown import Markdown

# Configuración de la API Key (Hardcoded)
DEEPSEEK_API_KEY = "tu_api_key_aqui"  # 🔑 Reemplaza con tu API Key real

# Configuración Rich
console = Console()

BANNER = r"""
[bold cyan]
 __    __      _ _         __    __ _                  _ 
/ / /\ \ \_ __(_) |_ ___  / / /\ \ (_)______ _ _ __ __| |
\ \/  \/ / '__| | __/ _ \ \ \/  \/ / |_  / _` | '__/ _` |
 \  /\  /| |  | | ||  __/  \  /\  /| |/ / (_| | | | (_| |
  \/  \/ |_|  |_|\__\___|   \/  \/ |_/___\__,_|_|  \__,_|

---- By: MARH -------------------------------------------
[/bold cyan]
"""

def verificar_entorno_virtual():
    """Verifica si estamos ejecutando dentro de un entorno virtual"""
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def crear_entorno_virtual():
    """Crea un nuevo entorno virtual"""
    venv_dir = "venv"
    if not os.path.exists(venv_dir):
        console.print("[bold yellow]⚡ Creando entorno virtual...[/bold yellow]")
        subprocess.check_call([sys.executable, "-m", "venv", venv_dir])
        console.print(f"[bold green]✅ Entorno virtual creado en: {venv_dir}[/bold green]")
    return venv_dir

def instalar_dependencias():
    """Instala las dependencias necesarias dentro del entorno virtual"""
    console.print("[bold yellow]⚡ Instalando dependencias...[/bold yellow]")
    subprocess.check_call([
        os.path.join("venv", "bin", "python"),
        "-m", "pip", "install", "openai", "requests", "rich"
    ])
    console.print("[bold green]✅ Dependencias instaladas correctamente[/bold green]")

def inicializar_entorno():
    """Configuración inicial del entorno"""
    if not verificar_entorno_virtual():
        crear_entorno_virtual()
        instalar_dependencias()
        console.print("\n[bold green]🔥 Entorno configurado correctamente![/bold green]")
        console.print("[bold yellow]Ejecuta los siguientes comandos para continuar:[/bold yellow]")
        console.print("source venv/bin/activate", style="bold cyan")
        console.print("python WriteWizard.py\n", style="bold cyan")
        sys.exit(0)

# ==================== Funcionalidad Principal ====================
def generar_writeup(nombre_maquina, ip):
    """Genera un write-up profesional usando DeepSeek"""
    client = OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url="https://api.deepseek.com/v1"
    )

    system_msg = f"""Eres un experto en hacking ético. Genera una guía detallada para la máquina {nombre_maquina} ({ip}):
    
1. **Reconocimiento**: Comandos de escaneo (nmap/rustscan)
2. **Enumeración**: Técnicas específicas por servicio
3. **Explotación**: 3 métodos con payloads actualizados
4. **Post-Explotación**: Comandos de pivoting
5. **Escalada**: 2 vías de escalada (SUID/sudo)
6. **Hardering**: Recomendaciones de seguridad

Formato: Markdown con código ejecutable"""

    with Progress() as progress:
        task = progress.add_task("[cyan]Generando write-up...", total=100)
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": "Genera el write-up en español"}
            ],
            temperature=0.3,
            max_tokens=3000
        )
        progress.update(task, completed=100)
    
    return response.choices[0].message.content

def menu_principal():
    """Muestra el menú interactivo principal"""
    console.print(Panel.fit(BANNER, style="bold cyan"))
    
    maquina = console.input("\n🔧 [bold]Nombre de la máquina CTF: [/bold]").strip()
    ip = console.input("🌐 [bold]Dirección IP objetivo: [/bold]").strip()
    
    writeup = None
    while True:
        console.print("\n" + "="*50, style="bold blue")
        console.print("1. Generar write-up completo\n2. Salir")
        opcion = console.input("⚡ Selecciona una opción: ").strip()
        
        if opcion == "1":
            writeup = generar_writeup(maquina, ip)
            console.print(Markdown(writeup))
        elif opcion == "2":
            console.print("[bold red]🚪 Saliendo...[/bold red]")
            break
        else:
            console.print("[bold red]⚠️ Opción inválida![/bold red]")

if __name__ == "__main__":
    inicializar_entorno()
    menu_principal()