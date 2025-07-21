# info.py

from os import environ
import re

# ID Pattern (used for checking chat IDs like channels/groups)
id_pattern = re.compile(r"^-100\d+$")

# ========== 🔐 Bot Token & API Config ==========
BOT_TOKEN = environ.get("BOT_TOKEN", "7811309623:AAH9M9P46vDaUAz8oKznyXS4qYXUnLmoNQA")  # Replace with your actual Bot Token
API_ID = int(environ.get("API_ID", "25753873"))  # Replace with your actual API ID
API_HASH = environ.get("API_HASH", "3a5cdc2079cd76af80586102bd9761e2")  # Replace with your actual API Hash

#========== 👑 Admin IDs (multiple space-separated IDs) ==========#
id_pattern = re.compile(r'^.\d+$')

ADMINS = [int(admin) if id_pattern.search(admin) else admin
          for admin in environ.get('ADMINS', '5962658076').split()] # Replace with your actual admin user IDs


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
    'mongodb+srv://anonymousguywas:12345Trials@cluster0.t4nmrtp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
)

DATABASE_NAME = environ.get('DATABASE_NAME', 'GameBotDB')

# You can use this URI inside Games files as:
# from info import DATABASE_URI, DATABASE_NAME
