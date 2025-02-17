#!/usr/bin/env python3
# -- coding: utf-8 --
import sys
import subprocess
import pkg_resources
import requests
from openai import OpenAI
import json
import re
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress
from rich.markdown import Markdown
from rich.style import Style
import warnings

# Ignorar advertencias de deprecación
warnings.filterwarnings("ignore", category=DeprecationWarning)

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

# Configuración DeepSeek
DEEPSEEK_API_KEY = "TU_API_KEY_AQUI"  # 👉 Obténla en: https://platform.deepseek.com/api_keys
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

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
                messages=[{
                    "role": "system", "content": system_msg},
                    {"role": "user", "content": f"Genera write-up para {nombre_maquina}"}
                ],
                temperature=0.3,
                max_tokens=3000
            )
            progress.update(task, completed=100)
    
    return response.choices[0].message.content

def analizar_puerto(ip, puerto):
    """Análisis avanzado de un puerto específico"""
    with console.status("[bold green]Analizando puerto...[/bold green]") as status:
        response = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=[{
                "role": "user", 
                "content": f"Analiza {ip}:{puerto} y lista 5 CVE recientes con PoCs"
            }]
        )
        return response.choices[0].message.content

def modo_automatico(ip):
    """Genera un script Bash automático"""
    with console.status("[bold yellow]Generando script automático...[/bold yellow]") as status:
        response = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=[{
                "role": "user",
                "content": f"Genera script Bash automático para {ip} con: escaneo, explotación y post-explotación"
            }]
        )
        return response.choices[0].message.content

def exportar_writeup(writeup, nombre_maquina):
    """Exporta el write-up en el formato y ruta especificados"""
    console.print("\n📤 [bold]Opciones de exportación:[/bold]")
    console.print("1. Markdown (.md)")
    console.print("2. Texto plano (.txt)")
    console.print("3. HTML (.html)")
    formato = console.input("⚡ Selecciona el formato (1-3): ").strip()
    
    if formato == "1":
        extension = ".md"
    elif formato == "2":
        extension = ".txt"
    elif formato == "3":
        extension = ".html"
    else:
        console.print("[bold red]❌ Formato no válido. Usando Markdown por defecto.[/bold red]")
        extension = ".md"
    
    ruta = console.input(f"📂 Ruta para guardar el archivo (deja vacío para ./{nombre_maquina}_writeup{extension}): ").strip()
    if not ruta:
        ruta = f"./{nombre_maquina}_writeup{extension}"
    
    try:
        with open(ruta, "w") as f:
            if formato == "3":  # HTML
                f.write(f"<h1>Write-up de {nombre_maquina}</h1>\n<pre>{writeup}</pre>")
            else:
                f.write(f"# Write-up de {nombre_maquina}\n\n{writeup}")
        console.print(f"✅ [bold green]Write-up guardado en {ruta}[/bold green]")
    except Exception as e:
        console.print(f"[bold red]❌ Error al guardar el archivo: {e}[/bold red]")

def mostrar_menu():
    console.print("\n" + "="*50, style="bold blue")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Opción", style="cyan")
    table.add_column("Descripción", style="green")
    table.add_row("1", "🧙‍♂️ Generar write-up completo")
    table.add_row("2", "🔍 Analizar puerto específico")
    table.add_row("3", "🤖 Modo Automático (Autopwn)")
    table.add_row("4", "📤 Exportar write-up")
    table.add_row("5", "❌ Salir")
    console.print(table)

def main():
    verificar_dependencias()  # Verifica e instala dependencias antes de continuar
    console.print(Panel.fit(BANNER, style="bold cyan"))
    maquina = console.input("\n🔧 [bold]Nombre de la máquina: [/bold]").strip()
    ip = console.input("🌐 [bold]Dirección IP: [/bold]").strip()
    
    while True:
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
