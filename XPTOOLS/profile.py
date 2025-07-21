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

from pyrogram import Client, filters, enums
from pyrogram.types import Message
from pymongo import MongoClient
from datetime import datetime
from info import DATABASE_URI, DATABASE_NAME

def register_profile_handler(app: Client):
    db = MongoClient(DATABASE_URI)[DATABASE_NAME]
    wins_col = db["GameWins"]

    @app.on_message(filters.command("profile") & filters.private)
    async def profile_command(client: Client, message: Message):
        user_id = message.from_user.id
        username = message.from_user.username or "N/A"

        # Fetch profile photos
        photo_file_id = None
        try:
            photos = await client.get_profile_photos(user_id, limit=1)
            if photos.total_count > 0:
                photo_file_id = photos.photos[0][-1].file_id  # Largest size
        except Exception as e:
            print(f"❌ Error fetching profile photo: {e}")

        # Fetch wins
        win_record = wins_col.find_one({"user_id": user_id})
        wins = win_record.get("wins", 0) if win_record else 0

        now = datetime.now()
        time_now = now.strftime("%I:%M %p")
        date_now = now.strftime("%Y-%m-%d")

        caption = f"""
<b><u>𝗠𝘆 𝗔𝗰𝗰𝗼𝘂𝗻𝘁</u></b>

🆔 Uꜱᴇʀ Iᴅ: <code>{user_id}</code>
👤 Uꜱᴇʀɴᴀᴍᴇ: @{username}

⏰ Tɪᴍᴇ: {time_now}
📅 Dᴀᴛᴇ: {date_now}
👑 Wɪɴꜱ: <b>{wins}</b> 🏆
"""

        try:
            if photo_file_id:
                await client.send_photo(
                    chat_id=message.chat.id,
                    photo=photo_file_id,
                    caption=caption,
                    parse_mode=enums.ParseMode.HTML
                )
            else:
                await message.reply(caption, parse_mode=enums.ParseMode.HTML)
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            await message.reply(caption, parse_mode=enums.ParseMode.HTML)
