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

# Games/tictactoe.py

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from pyrogram import enums
import random
from pymongo import MongoClient
from info import DATABASE_URI, DATABASE_NAME

# MongoDB Setup
client = MongoClient(DATABASE_URI)
db = client[DATABASE_NAME]
collection = db["GameWins"]

# Game state tracking - now using message_id as key for better persistence
active_games = {}

def new_board():
    return [" " for _ in range(9)]

def check_winner(board):
    wins = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    for a, b, c in wins:
        if board[a] == board[b] == board[c] != " ":
            return board[a]
    if " " not in board:
        return "draw"
    return None

def render_board(board, difficulty):
    buttons = []
    for i in range(0, 9, 3):
        row = []
        for j in range(3):
            cell = board[i + j]
            symbol = cell if cell != " " else "⬜"
            row.append(InlineKeyboardButton(symbol, callback_data=f"move_{i+j}"))
        buttons.append(row)
    
    buttons.append([
        InlineKeyboardButton("🔄 Restart", callback_data="restart"),
        InlineKeyboardButton(f"🔧 {difficulty.capitalize()}", callback_data="change_diff")
    ])
    return InlineKeyboardMarkup(buttons)

def bot_move(board, difficulty):
    # Simple bot logic for demonstration; replace with minimax for 'hard'
    empty_cells = [i for i, cell in enumerate(board) if cell == " "]
    if not empty_cells:
        return None
    if difficulty == "easy":
        return random.choice(empty_cells)
    elif difficulty == "medium":
        # Block player win if possible
        for i in empty_cells:
            board_copy = board[:]
            board_copy[i] = "⭕"
            if check_winner(board_copy) == "⭕":
                return i
        for i in empty_cells:
            board_copy = board[:]
            board_copy[i] = "❌"
            if check_winner(board_copy) == "❌":
                return i
        return random.choice(empty_cells)
    elif difficulty == "hard":
        # Implement minimax or advanced logic here
        # For now, just pick randomly
        return random.choice(empty_cells)
    return random.choice(empty_cells)

async def play_game(client, message: Message, difficulty="medium"):
    # Use message.id as the key for better persistence
    active_games[message.id] = {
        "board": new_board(),
        "difficulty": difficulty,
        "chat_id": message.chat.id
    }
    text = f"🎮 <b>Tic Tac Toe</b> (Difficulty: {difficulty.capitalize()})\nYou are ❌. Tap to play!"
    game_message = await message.reply(
        text, 
        reply_markup=render_board(active_games[message.id]["board"], difficulty),
        quote=True, 
        parse_mode=enums.ParseMode.HTML
    )
    # Store the game message ID too
    active_games[message.id]["game_message_id"] = game_message.id

async def handle_callback(client, callback_query: CallbackQuery):
    message = callback_query.message
    user = callback_query.from_user
    data = callback_query.data
    
    # Find the game by message ID (more reliable than chat ID)
    game = None
    for msg_id, game_data in active_games.items():
        if game_data.get("game_message_id") == message.id:
            game = game_data
            break
    
    if not game:
        return await callback_query.answer("Game session expired. Start a new game with /tictactoe", show_alert=True)

    board = game["board"]
    difficulty = game["difficulty"]

    if data == "restart":
        # Reset the board and update the message
        game["board"] = new_board()
        await message.edit_text(
            f"🎮 <b>Tic Tac Toe</b> (Difficulty: {difficulty.capitalize()})\nYou are ❌. Tap to play!",
            reply_markup=render_board(game["board"], difficulty),
            parse_mode=enums.ParseMode.HTML
        )
        return await callback_query.answer("Game restarted!")

    elif data == "change_diff":
        # Cycle through difficulties
        difficulties = ["easy", "medium", "hard"]
        current_index = difficulties.index(difficulty)
        new_diff = difficulties[(current_index + 1) % len(difficulties)]
        game["difficulty"] = new_diff
        game["board"] = new_board()
        
        await message.edit_text(
            f"🎮 <b>Tic Tac Toe</b> (Difficulty: {new_diff.capitalize()})\nYou are ❌. Tap to play!",
            reply_markup=render_board(game["board"], new_diff),
            parse_mode=enums.ParseMode.HTML
        )
        return await callback_query.answer(f"Difficulty changed to {new_diff.capitalize()}")

    elif data.startswith("move_"):
        move = int(data.split("_")[1])
        
        if board[move] != " ":
            return await callback_query.answer("❌ That cell is already taken!", show_alert=True)

        # Player move
        board[move] = "❌"
        winner = check_winner(board)
        if winner:
            await update_game(message, board, winner, user.id, user.first_name, difficulty)
            # Don't remove the game state yet - allow viewing final board
            return await callback_query.answer()

        # Bot move
        bot_choice = bot_move(board, difficulty)
        if bot_choice is not None:
            board[bot_choice] = "⭕"

        winner = check_winner(board)
        if winner:
            await update_game(message, board, winner, user.id, user.first_name, difficulty)
        else:
            await message.edit_text(
                f"🎮 <b>Tic Tac Toe</b> (Difficulty: {difficulty.capitalize()})\nYou are ❌. Tap to play!",
                reply_markup=render_board(board, difficulty),
                parse_mode=enums.ParseMode.HTML
            )
        return await callback_query.answer()

# ... [keep the existing update_game function unchanged] ...

async def update_game(message: Message, board, winner, user_id, name, difficulty):
    if winner == "❌":
        text = f"🎉 <b>You Win, {name}!</b> 🏆\nDifficulty: {difficulty.capitalize()}"
        existing = collection.find_one({"user_id": user_id})
        if existing:
            collection.update_one({"user_id": user_id}, {"$inc": {"wins": 1}})
        else:
            collection.insert_one({"user_id": user_id, "name": name, "wins": 1})

    elif winner == "⭕":
        text = f"🤖 <b>Bot Wins!</b> Try Again.\nDifficulty: {difficulty.capitalize()}"
    elif winner == "draw":
        text = f"🤝 <b>It's a draw!</b>\nDifficulty: {difficulty.capitalize()}"

    await message.edit_text(
        text,
        reply_markup=render_board(board, difficulty),
        parse_mode=enums.ParseMode.HTML
    )