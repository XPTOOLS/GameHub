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

# XPTOOLS/games.py
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode

def register_game_handlers(app: Client):
    @app.on_message(filters.command("games") & filters.private)
    async def games_command(client: Client, message: Message):
        await message.reply(
            "🎮 <b>Gᴀᴍᴇ Mᴇɴᴜ</b>\n\n"
            "🔢 <b>/guess</b> — Gᴜᴇꜱꜱ ᴛʜᴇ Nᴜᴍʙᴇʀ\n"
            "❌⭕ <b>/tictactoe</b> — Tɪᴄ Tᴀᴄ Tᴏᴇ\n"
            "🪨📄✂️ <b>/rps</b> — Rᴏᴄᴋ Pᴀᴘᴇʀ Sᴄɪssᴏʀꜱ",
            parse_mode=ParseMode.HTML
        )
