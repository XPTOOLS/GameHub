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

# main.py

from pyrogram import Client, filters, enums
from pyrogram.types import CallbackQuery
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.errors import UserNotParticipant
from info import BOT_TOKEN, API_ID, API_HASH, PICS, SOCIAL_BUTTONS, DATABASE_URI, DATABASE_NAME, REQUIRED_CHANNELS
from Games import tictactoe, rps
import os
import asyncio
from aiohttp import web
from admins import (
    register_broadcast_command,
    register_stats_command,
    register_resetwins_command,
    register_adminpanel_command,
    ADMINS
)
from pymongo import MongoClient

app = Client("GameBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Register admin commands
register_broadcast_command(app)
register_stats_command(app)
register_resetwins_command(app)
register_adminpanel_command(app)

# Register leaderboard handler from XPTOOLS
from XPTOOLS.leaderboard import register_leaderboard_handler
register_leaderboard_handler(app)

from XPTOOLS.profile import register_profile_handler
register_profile_handler(app)

from XPTOOLS.contactus import register_contactus_handler
register_contactus_handler(app)

from XPTOOLS.games import register_game_handlers
register_game_handlers(app)

#=================== Bot Configuration ====================
WEBHOOK_PATH = f"/{BOT_TOKEN}"
WEBHOOK_URL = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME', '')}{WEBHOOK_PATH}"
PORT = int(os.environ.get("PORT", 10000))

# Force Join Checker (fixed version)
async def is_user_member(client, user_id):
    for ch in REQUIRED_CHANNELS:
        chat = ch.get("chat") or ch.get("url").split("/")[-1]
        try:
            # Handle both channel IDs and usernames
            if str(chat).startswith('-100'):
                chat_id = int(chat)
            else:
                chat_id = chat.lstrip('@')  # Remove @ if present
                
            member = await client.get_chat_member(chat_id, user_id)
            if member.status not in [enums.ChatMemberStatus.MEMBER, 
                                   enums.ChatMemberStatus.ADMINISTRATOR, 
                                   enums.ChatMemberStatus.OWNER]:
                return False
        except UserNotParticipant:
            return False
        except Exception as e:
            print(f"Error checking membership for {chat}: {e}")
            return False
    return True

async def ask_user_to_join(client, message):
    buttons = [[InlineKeyboardButton(ch["label"], url=ch["url"])] for ch in REQUIRED_CHANNELS]
    buttons.append([InlineKeyboardButton("✅ 𝗩𝗲𝗿𝗶𝗳𝘆 𝗠𝗲𝗺𝗯𝗲𝗿𝘀𝗵𝗶𝗽", callback_data="verify_membership")])
    await message.reply(
        "🚨 ᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ ʙᴏᴛ, ʏᴏᴜ ᴍᴜꜱᴛ ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟꜱ ꜰɪʀꜱᴛ! 🚨\n"
        "ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴꜱ ʙᴇʟᴏᴡ ᴛᴏ ᴊᴏɪɴ, ᴛʜᴇɴ ᴘʀᴇꜱꜱ '✅ 𝗩𝗲𝗿𝗶𝗳𝘆 𝗠𝗲𝗺𝗯𝗲𝗿𝘀𝗵𝗶𝗽' ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ.",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=enums.ParseMode.HTML
    )

# ==================== Start Command ====================
client_db = MongoClient(DATABASE_URI)
db = client_db[DATABASE_NAME]
users_col = db["Users"]
wins_col = db["GameWins"]

@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    if not await is_user_member(client, message.from_user.id):
        await ask_user_to_join(client, message)
        return

    # ✅ Register user in MongoDB
    user_data = {
        "user_id": message.from_user.id,
        "first_name": message.from_user.first_name,
        "username": message.from_user.username,
    }

    if not users_col.find_one({"user_id": message.from_user.id}):
        users_col.insert_one(user_data)
        print(f"[REGISTER] User {message.from_user.id} ({message.from_user.first_name}) registered.")

    # 📸 Send welcome message
    photo_url = PICS[0] if PICS else None

    # Arrange social buttons side by side (2 per row)
    social_items = list(SOCIAL_BUTTONS.items())
    keyboard_buttons = []
    for i in range(0, len(social_items), 2):
        row = []
        for j in range(2):
            if i + j < len(social_items):
                text, url = social_items[i + j]
                row.append(InlineKeyboardButton(text, url=url))
        keyboard_buttons.append(row)

    keyboard = InlineKeyboardMarkup(keyboard_buttons)

    await message.reply_photo(
        photo=photo_url,
        caption=(
            f"👋 <b>Hello {message.from_user.mention}!</b>\n\n"
            "🎮 Wᴇʟᴄᴏᴍᴇ ᴛᴏ *GameHub Bot* 🎉\n"
            "Use /games to play your first game!"
        ),
        reply_markup=keyboard,
        parse_mode=enums.ParseMode.HTML
    )

# Callback for "Verify Membership"
@app.on_callback_query(filters.regex("verify_membership"))
async def refresh_join_status(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    if await is_user_member(client, user_id):
        await callback_query.message.delete()
        await client.send_message(
            user_id,
            "✅ 𝙑𝙚𝙧𝙞𝙛𝙞𝙘𝙖𝙩𝙞𝙤𝙣 𝙨𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡! 𝙔𝙤𝙪 𝙘𝙖𝙣 𝙣𝙤𝙬 𝙪𝙨𝙚 𝙖𝙡𝙡 �𝙗𝙤𝙩 𝙘𝙤𝙢𝙢𝙖𝙣𝙙𝙨."
        )
    else:
        await callback_query.answer("❌ 𝙔𝙤𝙪 𝙝𝙖𝙫𝙚𝙣'𝙩 𝙟𝙤𝙞𝙣𝙚𝙙 𝙖𝙡𝙡 𝙘𝙝𝙖𝙣𝙣𝙚𝙡𝙨 𝙮𝙚𝙩!", show_alert=True)

# ==================== Tic Tac Toe Command ==================== #
@app.on_message(filters.command("tictactoe") & filters.private)
async def tictactoe_handler(client, message: Message):
    if not await is_user_member(client, message.from_user.id):
        await ask_user_to_join(client, message)
        return
    
    # Start new game with medium difficulty by default
    await tictactoe.play_game(client, message, difficulty="medium")

# ==================== Rock Paper Scissors Command ==================== #
@app.on_message(filters.command("rps") & filters.private)
async def rps_handler(client, message: Message):
    if not await is_user_member(client, message.from_user.id):
        await ask_user_to_join(client, message)
        return
    await rps.play_rps(client, message)

# Add this with your other imports
from Games import number_guess

# Add this with your other command handlers
@app.on_message(filters.command("guess") & filters.private)
async def number_game_handler(client, message: Message):
    if not await is_user_member(client, message.from_user.id):
        await ask_user_to_join(client, message)
        return
    await number_guess.start_number_game(client, message)

# Add this with your other message handlers
@app.on_message(filters.text & filters.private)
async def handle_all_messages(client, message: Message):
    if message.chat.id in number_guess.active_games:
        await number_guess.handle_number_guess(client, message)

# ==================== Game Button Callbacks ==================== #
@app.on_callback_query(filters.regex(r"^(move_|restart|change_diff)"))
async def game_callbacks(client, callback_query: CallbackQuery):
    await tictactoe.handle_callback(client, callback_query)

# callback handlers (Rock Paper Scissors)
@app.on_callback_query(filters.regex(r"^rps_"))
async def rps_callbacks(client, callback_query: CallbackQuery):
    await rps.handle_rps_callback(client, callback_query)

# callback handlers (Number Guessing Game)
@app.on_callback_query(filters.regex(r"^num_"))
async def number_callbacks(client, callback_query: CallbackQuery):
    await number_guess.handle_number_callback(client, callback_query)

#================ Webhook and Health Check =================#
async def handle_webhook(request):
    data = await request.json()
    await app.process_update(data)
    return web.Response(status=200)

async def health_check(request):
    return web.Response(text="OK")

async def main():
    if os.environ.get('RENDER_EXTERNAL_HOSTNAME'):
        print("🌐 Running in webhook mode...")
        await app.start()
        await app.set_webhook(
            url=WEBHOOK_URL,
            drop_pending_updates=True,
            allowed_updates=["message", "callback_query"]
        )
        server = web.Application()
        server.router.add_post(WEBHOOK_PATH, handle_webhook)
        server.router.add_get('/', health_check)
        runner = web.AppRunner(server)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", PORT)
        await site.start()
        print(f"Webhook server started on port {PORT}")
        while True:
            await asyncio.sleep(3600)

if __name__ == "__main__":
    if os.environ.get('RENDER_EXTERNAL_HOSTNAME'):
        asyncio.run(main())
    else:
        print("🤖 Running in polling mode...")
        app.run()
