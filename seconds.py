import telebot
from telebot import types

# Setup the bot

bot = telebot.TeleBot(TOKEN_BOT)

# Dictionaries to keep track of user states
user_states = {}

# State constants
STATE_AWAITING_BINARY_INPUT = "awaiting_binary_input"
STATE_AWAITING_TEXT_INPUT = "awaiting_text_input"

# Create a function to turn the message into a binary code
def into_binary(text):
    binary_string = ' '.join(format(ord(char), '08b') for char in text)
    return binary_string

# Create a function to turn binary code into a text message
def binary_to_string(binary_string):
    binary_values = binary_string.split()
    ascii_characters = [chr(int(bv, 2)) for bv in binary_values]
    original_string = ''.join(ascii_characters)
    return original_string

# Start command
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Text to Binary', callback_data='to_binary')
    button2 = types.InlineKeyboardButton('Binary to Text', callback_data='to_text')
    keyboard.add(button1, button2)
    bot.send_message(message.chat.id, 'Welcome to Binary Bot! Choose an option:', reply_markup=keyboard)

# Add a query handler to handle the buttons
@bot.callback_query_handler(func=lambda call: True)
def buttons(call):
    if call.data == 'to_binary':
        user_states[call.message.chat.id] = STATE_AWAITING_TEXT_INPUT
        bot.send_message(call.message.chat.id, 'Send me a string to turn it into binary code.')
    elif call.data == 'to_text':
        user_states[call.message.chat.id] = STATE_AWAITING_BINARY_INPUT
        bot.send_message(call.message.chat.id, 'Send me binary code to turn it into a text string.')

# Handle text messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    state = user_states.get(message.chat.id)

    if state == STATE_AWAITING_TEXT_INPUT:
        binary_result = into_binary(message.text)
        bot.send_message(message.chat.id, f"Binary code: {binary_result}")
    elif state == STATE_AWAITING_BINARY_INPUT:
        try:
            text_result = binary_to_string(message.text)
            bot.send_message(message.chat.id, f"Text: {text_result}")
        except ValueError:
            bot.send_message(message.chat.id, "Invalid binary code. Please make sure to enter a valid binary string.")

    # Clear the state after processing
    user_states[message.chat.id] = None

bot.polling()
