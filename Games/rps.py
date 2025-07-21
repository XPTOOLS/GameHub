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

# Games/rps.py

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from pyrogram import enums
from pymongo import MongoClient
from info import DATABASE_URI, DATABASE_NAME
import random

# MongoDB Setup
client = MongoClient(DATABASE_URI)
db = client[DATABASE_NAME]
collection = db["GameWins"]

# Game choices
CHOICES = ["🗿 Rock", "📄 Paper", "✂️ Scissors"]
BEATS = {
    "🗿 Rock": "✂️ Scissors",
    "📄 Paper": "🗿 Rock",
    "✂️ Scissors": "📄 Paper"
}

async def play_rps(client, message: Message):
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🗿 Rock", callback_data="rps_rock"),
            InlineKeyboardButton("📄 Paper", callback_data="rps_paper"),
            InlineKeyboardButton("✂️ Scissors", callback_data="rps_scissors")
        ],
        [InlineKeyboardButton("🔄 Play Again", callback_data="rps_restart")]
    ])
    
    await message.reply(
        "🎮 <b>Rock Paper Scissors</b>\nChoose your move:",
        reply_markup=keyboard,
        parse_mode=enums.ParseMode.HTML
    )

async def handle_rps_callback(client, callback_query: CallbackQuery):
    user_choice_raw = callback_query.data.split("_")[1]

    if user_choice_raw == "restart":
        await play_rps(client, callback_query.message)
        return await callback_query.answer("New game started!")

    # Map raw choice to emoji+text
    choice_map = {
        "rock": "🗿 Rock",
        "paper": "📄 Paper",
        "scissors": "✂️ Scissors"
    }
    user_choice = choice_map.get(user_choice_raw)
    if not user_choice:
        await callback_query.answer("Invalid choice!", show_alert=True)
        return

    user = callback_query.from_user
    bot_choice = random.choice(list(BEATS.keys()))

    if BEATS[user_choice] == bot_choice:
        result = "🎉 You win!"
        # Update database
        existing = collection.find_one({"user_id": user.id})
        if existing:
            collection.update_one({"user_id": user.id}, {"$inc": {"wins": 1}})
        else:
            collection.insert_one({"user_id": user.id, "name": user.first_name, "wins": 1})
    elif BEATS[bot_choice] == user_choice:
        result = "🤖 Bot wins!"
    else:
        result = "🤝 It's a tie!"

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Play Again", callback_data="rps_restart")]
    ])

    await callback_query.message.edit_text(
        f"🎮 <b>Rock Paper Scissors</b>\n\n"
        f"👤 Your choice: {user_choice}\n"
        f"🤖 Bot's choice: {bot_choice}\n\n"
        f"<b>{result}</b>",
        reply_markup=keyboard,
        parse_mode=enums.ParseMode.HTML
    )
    await callback_query.answer()