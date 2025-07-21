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

# Games/number_guess.py

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from pyrogram import enums
from pymongo import MongoClient
from info import DATABASE_URI, DATABASE_NAME
import random

# MongoDB Setup
client = MongoClient(DATABASE_URI)
db = client[DATABASE_NAME]
collection = db["GameWins"]

# Game state tracking
active_games = {}

async def start_number_game(client, message: Message):
    chat_id = message.chat.id
    secret_number = random.randint(1, 100)
    active_games[chat_id] = {
        "secret": secret_number,
        "attempts": 0,
        "max_attempts": 10,
        "game_over": False
    }
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 New Game", callback_data="num_new")],
        [InlineKeyboardButton("❌ Cancel", callback_data="num_cancel")]
    ])
    
    await message.reply(
        "🔢 <b>Number Guessing Game</b>\n\n"
        "I've picked a number between 1 and 100.\n"
        "You have 10 attempts to guess it!\n\n"
        "Send me your guess as a number (1-100):",
        reply_markup=keyboard,
        parse_mode=enums.ParseMode.HTML
    )

async def handle_number_guess(client, message: Message):
    chat_id = message.chat.id
    if chat_id not in active_games or active_games[chat_id]["game_over"]:
        return
    
    try:
        guess = int(message.text)
        if guess < 1 or guess > 100:
            raise ValueError
    except (ValueError, TypeError):
        await message.reply("Please enter a valid number between 1 and 100!")
        return
    
    game = active_games[chat_id]
    game["attempts"] += 1
    
    if guess == game["secret"]:
        # Player won
        await handle_win(client, message, game)
        active_games[chat_id]["game_over"] = True
    elif game["attempts"] >= game["max_attempts"]:
        # Player lost
        await handle_loss(client, message, game)
        active_games[chat_id]["game_over"] = True
    else:
        # Give hint
        hint = "higher" if guess < game["secret"] else "lower"
        remaining = game["max_attempts"] - game["attempts"]
        await message.reply(
            f"🔄 Try again! My number is {hint} than {guess}.\n"
            f"Attempts left: {remaining}",
            parse_mode=enums.ParseMode.HTML
        )

async def handle_number_callback(client, callback_query: CallbackQuery):
    data = callback_query.data.split("_")[1]
    chat_id = callback_query.message.chat.id
    
    if data == "new":
        await start_number_game(client, callback_query.message)
    elif data == "cancel":
        if chat_id in active_games:
            del active_games[chat_id]
        await callback_query.message.edit_text(
            "❌ Game cancelled.",
            parse_mode=enums.ParseMode.HTML
        )
    
    await callback_query.answer()

async def handle_win(client, message: Message, game):
    user = message.from_user
    existing = collection.find_one({"user_id": user.id})
    if existing:
        collection.update_one({"user_id": user.id}, {"$inc": {"number_wins": 1}})
    else:
        collection.insert_one({
            "user_id": user.id,
            "name": user.first_name,
            "number_wins": 1,
            "number_attempts": game["attempts"]
        })
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Play Again", callback_data="num_new")]
    ])
    
    await message.reply(
        f"🎉 <b>Congratulations {user.first_name}!</b>\n"
        f"You guessed the number {game['secret']} in {game['attempts']} attempts!",
        reply_markup=keyboard,
        parse_mode=enums.ParseMode.HTML
    )

async def handle_loss(client, message: Message, game):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Try Again", callback_data="num_new")]
    ]) 
    
    await message.reply(
        f"😢 <b>Game Over!</b>\n"
        f"The number was {game['secret']}.\n"
        f"Better luck next time!",
        reply_markup=keyboard,
        parse_mode=enums.ParseMode.HTML
    )