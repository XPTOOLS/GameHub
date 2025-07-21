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

# XPTOOLS/leaderboard.py
from pyrogram import filters, enums
from pyrogram.types import Message
from pymongo import MongoClient
from info import DATABASE_URI, DATABASE_NAME

def register_leaderboard_handler(app):
    db = MongoClient(DATABASE_URI)[DATABASE_NAME]
    wins_col = db["GameWins"]
    users_col = db["Users"]

    @app.on_message(filters.command("leaderboard") & filters.private)
    async def leaderboard_command(client, message: Message):
        top_players = wins_col.find().sort("wins", -1).limit(10)
        leaderboard_text = "🏆 <b>Gᴀᴍᴇ Lᴇᴀᴅᴇʀʙᴏᴀʀᴅ</b>\n\n"
        found = False
        for rank, player in enumerate(top_players, 1):
            found = True
            user_id = player["user_id"]
            total_wins = player.get("wins", 0)
            user_data = users_col.find_one({"user_id": user_id})
            if user_data and "username" in user_data and user_data["username"]:
                mention = f"@{user_data['username']}"
            else:
                mention = f"<code>{user_id}</code>"
            leaderboard_text += f"{rank}. {mention} – <b>{total_wins}</b> 🏅\n"
        if not found:
            return await message.reply("📛 <b>No wins recorded yet!</b>", parse_mode=enums.ParseMode.HTML)
        await message.reply(leaderboard_text, parse_mode=enums.ParseMode.HTML)
