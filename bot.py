You’re exactly where we need you to be!  
Now we’re going to add the 3 files the bot needs in under 2 minutes.

Do this right on that screen you’re seeing:

### 1. Create the first file → bot.py
- In the box that says “Name your file…” type: `bot.py`  
- Then copy-paste ALL the code below into the big white area:

```python
import telebot
from telebot import types
import sqlite3
from datetime import datetime
import os

TOKEN = os.getenv("8216496503:AAFB_-d4JJ9g9zdMy3igid6W6LjFJ461Dnw")
bot = telebot.TeleBot(TOKEN)

# Create database
def init_db():
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS bookings
                 (id INTEGER PRIMARY KEY,
                  user_id INTEGER,
                  name TEXT,
                  phone TEXT,
                  room_type TEXT,
                  check_in TEXT,
                  check_out TEXT,
                  date_booked TEXT)''')
    conn.commit()
    conn.close()

ROOMS = {
    "single": {"name": "Single Room", "price": "₦25,000/night", "emoji": "Single Bed"},
    "double": {"name": "Double Room", "price": "₦40,000/night", "emoji": "Double Bed"},
    "suite":  {"name": "Luxury Suite",   "price": "₦80,000/night", "emoji": "Crown"}
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("Make a Booking")
    markup.add(btn)
    bot.send_message(message.chat.id,
        "*Welcome to My Hotel Bot* \n\n"
        "Press the button below to book a room",
        reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "Make a Booking")
def book_room(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for key, room in ROOMS.items():
        btn = types.InlineKeyboardButton(f"{room['emoji']} {room['name']} – {room['price']}", callback_data=f"room_{key}")
    markup.add(btn)
    bot.send_message(message.chat.id, "Choose your room type:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("room_"))
def get_name(call):
    room_key = call.data.split("_")[1]
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "your full name:")
    bot.register_next_step_handler(call.message, get_phone, room_key)

def get_phone(message, room_key):
    name = message.text
    bot.send_message(message.chat.id, "your phone number (e.g. +2348012345678):")
    bot.register_next_step_handler(message, get_dates, room_key, name)

def get_dates(message, room_key, name):
    phone = message.text
    bot.send_message(message.chat.id, "Check-in date (e.g. 10 Dec 2025):")
    bot.register_next_step_handler(message, get_checkout, room_key, name, phone)

def get_checkout(message, room_key, name, phone):
    check_in = message.text
    bot.send_message(message.chat.id, "Check-out date (e.g. 15 Dec 2025):")
    bot.register_next_step_handler(message, confirm_booking, room_key, name, phone, check_in)

def confirm_booking(message, room_key, name, phone, check_in):
    check_out = message.text
    room = ROOMS[room_key]
    text = f"""*Booking Confirmation*

Name: {name}
Phone: {phone}
Room: {room['emoji']} {room['name']}
Price: {room['price']}
Check-in: {check_in}
Check-out: {check_out}

Correct?"""
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Yes, confirm", callback_data=f"confirm_{room_key}_{name}_{phone}_{check_in}_{check_out}"),
        types.InlineKeyboardButton("Cancel", callback_data="cancel")
    )
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_"))
def save_booking(call):
    data = call.data.split("_")[1:]
    room_key, name, phone, check_in, check_out = data
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("INSERT INTO bookings (user_id, name, phone, room_type, check_in, check_out, date_booked) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (call.message.chat.id, name, phone, ROOMS[room_key]['name'], check_in, check_out, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()
    bot.edit_message_text("Your booking is confirmed! \nWe will contact you soon.", call.message.chat.id, call.message.id)

@bot.callback_query_handler(func=lambda call: call.data == "cancel")
def cancel(call):
    bot.edit_message_text("Booking cancelled.", call.message.chat.id, call.message.id)
    start(call.message)

init_db()
print("Hotel booking bot started...")
bot.infinity_polling()
```

→ After pasting, scroll down and click the green button **“Commit changes”**

### 2. Create the second file → requirements.txt
Click “Add file” → “Create new file”  
Name it: `requirements.txt`  
Paste only this one line:

```
pyTelegramBotAPI
```

→ Click “Commit changes”

### 3. (Optional but good) Update README.md
Click on README.md → Edit → change the title to  
`# Hotel Booking Bot` and anything you want → Commit

That’s all the code!

Now reply with just one thing:  
the full link of your repository  
(example: https://github.com/kellyservice06-create/Hotel-booking-bot)

As soon as you send the link, I’ll give you the exact Render deploy link that finishes everything in 3 clicks.  
You’re 3 minutes away from a fully working 24/7 booking bot!
