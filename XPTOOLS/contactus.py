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

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode

def register_contactus_handler(app: Client):
    @app.on_message(filters.command("contactus") & filters.private)
    async def contact_us_command(client: Client, message: Message):
        contact_info_msg = (
            "📞 ★彡( <b>𝕮𝖔𝖓𝖙𝖆𝖈𝖙 𝖀𝖘</b> )彡★ 📞\n\n"
            "📧 <b>Eᴍᴀɪʟ:</b> <code>freenethubbusiness@gmail.com</code>\n\n"
            "Fᴏʀ Aɴʏ Iꜱꜱᴜᴇꜱ, Bᴜꜱɪɴᴇꜱꜱ Dᴇᴀʟꜱ Oʀ IɴQᴜɪʀɪᴇꜱ,\n"
            "Pʟᴇᴀꜱᴇ Rᴇᴀᴄʜ Oᴜᴛ Tᴏ Uꜱ ⬇️\n\n"
            "❗ <i>ONLY FOR BUSINESS AND HELP, DON'T SPAM!</i>"
        )

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📩 Mᴇꜱꜱᴀɢᴇ Aᴅᴍɪɴ", url="https://t.me/SILANDO")]
        ])

        await message.reply(contact_info_msg, reply_markup=keyboard, parse_mode=ParseMode.HTML)
