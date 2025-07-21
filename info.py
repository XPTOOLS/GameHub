"""
XPTOOLS - A Telegram Bot
Copyright (c) 2025

This program is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

Credits & Social Media:
- Telegram: https://t.me/Freenethubz
- Youtube: https://youtube.com/@Freenethubtech
- Whatsapp Channel: https://whatsapp.com/channel/0029VbB3G3BH5JM0s7gtKA2d
- Whatsapp Group: https://chat.whatsapp.com/Iwau9IDlCn4CR6fsmI3mc7
- Admin: https://t.me/Silando
- Github: https://github.com/XPTOOLS
- Instagram: https://www.instagram.com/silandodev?igsh=MWtlaTB6d251bDN2eQ==
- Email: freenethubbusiness@gmail.com
"""

# info.py

from os import environ
import re

# ID Pattern (used for checking chat IDs like channels/groups)
id_pattern = re.compile(r"^-100\d+$")

# ========== 🔐 Bot Token & API Config ==========
BOT_TOKEN = environ.get("BOT_TOKEN", "")  # Replace with your actual Bot Token
API_ID = int(environ.get("API_ID", ""))  # Replace with your actual API ID
API_HASH = environ.get("API_HASH", "")  # Replace with your actual API Hash
RENDER_EXTERNAL_HOSTNAME = environ.get("RENDER_EXTERNAL_HOSTNAME", "")

#========== 👑 Admin IDs (multiple space-separated IDs) ==========#
id_pattern = re.compile(r'^.\d+$')

ADMINS = [int(admin) if id_pattern.search(admin) else admin
          for admin in environ.get('ADMINS', '').split()] # Replace with your actual admin user IDs


# ========== 🌐 Force Join Channel ==========
# Add this for multiple required channels (usernames or IDs)
REQUIRED_CHANNELS = [
   # {"label": "𝐌𝐀𝐈𝐍 𝐂𝐇𝐀𝐍𝐍𝐄𝐋", "url": "https://t.me/xptoolslogs", "chat": "xptoolslogs"},
    {"label": "𝐂𝐇𝐀𝐍𝐍𝐄𝐋 𝐀𝐍𝐍𝐎𝐔𝐍𝐂𝐄𝐌𝐄𝐍𝐓", "url": "https://t.me/megahubbots", "chat": "megahubbots"}
]

# ========== 🔗 Social Buttons (Start Message) ==========
SOCIAL_BUTTONS = {
    "🌐 Website": "https://www.freenethubz.blogspot.com",
    "📺 YouTube": "https://youtube.com/@Freenethubtech",
    "📷 Instagram": "https://instagram.com/Silando",
    "💬 Support": "https://t.me/Megahubbots"
}

# ========== 🖼️ Optional Start Images ==========
PICS = (environ.get('PICS', 'https://i.ibb.co/R4VNFg0B/game-logo.jpg')).split()

# ========== 🧠 MongoDB Config ==========
DATABASE_URI = environ.get(
    'DATABASE_URI',
    ''
)

DATABASE_NAME = environ.get('DATABASE_NAME', 'GameBotDB')

# You can use this URI inside Games files as:
# from info import DATABASE_URI, DATABASE_NAME
