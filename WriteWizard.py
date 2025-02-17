#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import subprocess
from importlib.metadata import distribution, PackageNotFoundError, version
import os
import json
import re
from openai import OpenAI
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
    for package in REQUIRED_PACKAGES:
        try:
            dist = distribution(package.split(">=")[0])
            required_version = package.split(">=")[1] if ">=" in package else None
            if required_version and version(dist) < required_version:
                raise ValueError(f"Versión insuficiente: {dist.version} < {required_version}")
        except PackageNotFoundError:
            console.print(f"[bold red]❌ Dependencia faltante: {package}[/bold red]")
            console.print("[bold yellow]Instalando dependencias...[/bold yellow]")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            console.print("[bold green]✅ Dependencias instaladas correctamente.[/bold green]")
        except ValueError as e:
            console.print(f"[bold red]❌ {e}[/bold red]")
            console.print("[bold yellow]Actualizando dependencias...[/bold yellow]")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "-r", "requirements.txt"])
            console.print("[bold green]✅ Dependencias actualizadas correctamente.[/bold green]")

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


# Configuración del cliente de DeepSeek
API_KEY = "tu_api_key_aqui"  # ⚠️ Inserta tu API Key de DeepSeek aquí
client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.deepseek.com/v1"  # Endpoint oficial de DeepSeek
)

def generar_writeup(nombre_maquina, ip):
    """Genera un write-up usando DeepSeek"""
    system_msg = f"""Eres un experto en hacking ético. Genera una guía detallada para la máquina {nombre_maquina} ({ip}):
    
1. **Reconocimiento**: Comandos de escaneo (nmap/rustscan)
2. **Enumeración**: Técnicas específicas por servicio
3. **Explotación**: 3 métodos con payloads actualizados
4. **Post-Explotación**: Comandos de pivoting
5. **Escalada**: 2 vías de escalada (SUID/sudo)
6. **Hardening**: Recomendaciones de seguridad

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

def analizar_puerto(ip, puerto):
    """Analiza un puerto usando DeepSeek"""
    with console.status("[bold green]Analizando puerto...[/bold green]"):
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{
                "role": "user",
                "content": f"Enumera vulnerabilidades y técnicas de explotación para {ip}:{puerto}"
            }]
        )
        return response.choices[0].message.content

def modo_automatico(ip):
    """Genera script de automatización con DeepSeek"""
    with console.status("[bold yellow]Generando script...[/bold yellow]"):
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{
                "role": "user",
                "content": f"Genera script Bash para hackear {ip} incluyendo: escaneo, explotación y post-explotación"
            }]
        )
        return response.choices[0].message.content

def exportar_writeup(writeup, nombre_maquina):
    """Exporta el write-up generado"""
    console.print("\n📤 [bold]Opciones de exportación:[/bold]")
    console.print("1. Markdown (.md)\n2. Texto (.txt)\n3. HTML")
    formato = console.input("⚡ Selección: ").strip()
    
    extension = {1: ".md", 2: ".txt", 3: ".html"}.get(int(formato), ".md")
    ruta = console.input(f"📂 Ruta (Enter para default): ") or f"./{nombre_maquina}_writeup{extension}"
    
    try:
        with open(ruta, "w") as f:
            if extension == ".html":
                f.write(f"<h1>Write-up {nombre_maquina}</h1>\n<pre>{writeup}</pre>")
            else:
                f.write(writeup)
        console.print(f"✅ [bold green]Guardado en: {ruta}[/bold green]")
    except Exception as e:
        console.print(f"[bold red]❌ Error: {e}[/bold red]")

def main():
    verificar_dependencias()
    console.print(Panel.fit(BANNER, style="bold cyan"))
    
    # Obtener datos de la máquina
    maquina = console.input("\n🔧 [bold]Nombre máquina CTF: [/bold]").strip()
    ip = console.input("🌐 [bold]Dirección IP: [/bold]").strip()
    
    writeup = None
    while True:
        console.print("\n" + "="*50, style="bold blue")
        console.print("1. Generar write-up\n2. Analizar puerto\n3. Script automático\n4. Exportar\n5. Salir")
        opcion = console.input("⚡ Opción: ").strip()
        
        if opcion == "1":
            writeup = generar_writeup(maquina, ip)
            console.print(Markdown(writeup))
        elif opcion == "2":
            puerto = console.input("🔌 Puerto a analizar: ").strip()
            analisis = analizar_puerto(ip, puerto)
            console.print(Panel.fit(analisis, style="bold green"))
        elif opcion == "3":
            script = modo_automatico(ip)
            console.print(Panel.fit(script, style="bold yellow"))
        elif opcion == "4":
            if writeup:
                exportar_writeup(writeup, maquina)
            else:
                console.print("[bold red]❌ Primero genera un write-up[/bold red]")
        elif opcion == "5":
            console.print("[bold red]🚪 Saliendo...[/bold red]")
            break
        else:
            console.print("[bold red]⚠️ Opción inválida[/bold red]")

if __name__ == "__main__":
    main()