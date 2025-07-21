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

# admins.py

from pyrogram import Client, filters, enums
from pyrogram.types import Message
from pymongo import MongoClient
from info import ADMINS, DATABASE_URI, DATABASE_NAME

# MongoDB setup
client_db = MongoClient(DATABASE_URI)
db = client_db[DATABASE_NAME]
users_col = db["Users"]


# ====================== /broadcast ==========================
def register_broadcast_command(app):
    @app.on_message(filters.command("broadcast") & filters.private)
    async def broadcast_command(client, message: Message):
        if message.from_user.id not in ADMINS:
            await message.reply("🚫 You are not authorized to use this command.")
            return
        if not message.reply_to_message:
            return await message.reply(
                "📌 <b>Rᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ</b>",
                parse_mode=enums.ParseMode.HTML
            )
        broadcast_msg = message.reply_to_message
        users = users_col.find()
        total = users_col.count_documents({})
        success, failed = 0, 0
        await message.reply(
            f"📡 <b>Bʀᴏᴀᴅᴄᴀsᴛ sᴛᴀʀᴛᴇᴅ...</b>\n\n"
            f"👥 <b>Tᴏᴛᴀʟ ᴜsᴇʀs:</b> <code>{total}</code>",
            parse_mode=enums.ParseMode.HTML
        )
        for user in users:
            try:
                await broadcast_msg.copy(chat_id=user["user_id"])
                success += 1
            except Exception:
                failed += 1
        await message.reply(
            f"✅ <b>Bʀᴏᴀᴅᴄᴀsᴛ Cᴏᴍᴘʟᴇᴛᴇ</b>\n\n"
            f"📤 Sᴇɴᴛ: <code>{success}</code>\n"
            f"❌ Fᴀɪʟᴇᴅ: <code>{failed}</code>\n"
            f"👥 Tᴏᴛᴀʟ: <code>{total}</code>",
            parse_mode=enums.ParseMode.HTML
        )

# ====================== /stats ==========================
def register_stats_command(app):
    @app.on_message(filters.command("stats") & filters.private)
    async def stats_command(client, message: Message):
        if message.from_user.id not in ADMINS:
            await message.reply("🚫 You are not authorized to use this command.")
            return
        total = users_col.count_documents({})
        await message.reply(
            f"📊 <b>Uꜱᴇʀ Sᴛᴀᴛɪꜱᴛɪᴄꜱ</b>\n\n"
            f"👤 <b>Tᴏᴛᴀʟ Rᴇɢɪꜱᴛᴇʀᴇᴅ:</b> <code>{total}</code>",
            parse_mode=enums.ParseMode.HTML
        )

# ====================== /resetwins ==========================
def register_resetwins_command(app):
    @app.on_message(filters.command("resetwins") & filters.private)
    async def reset_wins_handler(client, message: Message):
        if message.from_user.id not in ADMINS:
            await message.reply("🚫 You are not authorized to use this command.")
            return
        db = MongoClient(DATABASE_URI)[DATABASE_NAME]
        db["GameWins"].delete_many({})
        await message.reply(
            "♻️ <b>Wɪɴ Dᴀᴛᴀ Hᴀꜱ Bᴇᴇɴ Rᴇꜱᴇᴛ ꜰᴏʀ Aʟʟ Uꜱᴇʀꜱ</b>!",
            parse_mode=enums.ParseMode.HTML
        )

# ====================== /adminpanel ==========================
def register_adminpanel_command(app):
    @app.on_message(filters.command("adminpanel") & filters.private)
    async def admin_panel_handler(client, message: Message):
        if message.from_user.id not in ADMINS:
            await message.reply("🚫 You are not authorized to use this command.")
            return
        panel_text = (
            "🔐 <b>Aᴅᴍɪɴ Pᴀɴᴇʟ</b>\n\n"
            "📢 <b>/broadcast</b> — Sᴇɴᴅ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ᴀʟʟ ᴜꜱᴇʀꜱ (ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ).\n"
            "📊 <b>/stats</b> — Cʜᴇᴄᴋ ᴛᴏᴛᴀʟ ʀᴇɢɪsᴛᴇʀᴇᴅ ᴜꜱᴇʀꜱ.\n"
            "♻️ <b>/resetwins</b> — Rᴇsᴇᴛ ᴡɪɴs ᴏꜰ ᴀʟʟ ᴘʟᴀʏᴇʀꜱ.\n"
            "🛠️ <b>/adminpanel</b> — Sʜᴏᴡ ᴛʜɪꜱ ᴘᴀɴᴇʟ."
        )
        await message.reply(panel_text, parse_mode=enums.ParseMode.HTML)
