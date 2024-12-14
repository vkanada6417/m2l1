import telebot 
from config import token
from random import randint
from logic import Pokemon, Wizard, Fighter

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['go'])
def start(message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        chance = randint(1,5)
        if chance == 1:
            pokemon = Pokemon(message.from_user.username)
        elif chance == 2:
            pokemon = Wizard(message.from_user.username)
        elif chance == 3:
            pokemon = Fighter(message.from_user.username)
        else:
            pokemon = Pokemon(message.from_user.username)
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")

@bot.message_handler(commands=['rename'])
def rename(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "Укажите новое имя для покемона: /rename <новое_имя>")
        return

    if message.from_user.username in Pokemon.pokemons:
        new_name = args[1]
        Pokemon.pokemons[message.from_user.username].name = new_name
        bot.send_message(message.chat.id, f"Имя покемона изменено на {new_name}")
    else:
        bot.reply_to(message, "Сначала создайте покемона с помощью команды /go")

@bot.message_handler(commands=['info'])
def info(message):
    if message.from_user.username in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[message.from_user.username]
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_message(message.chat.id, f"Здоровье: {pokemon.hp}")
        bot.send_message(message.chat.id, f"Сила: {pokemon.power}")
    else:
        bot.reply_to(message, "Сначала создайте покемона с помощью команды /go")

@bot.message_handler(commands=['feed'])
def feed(message):
    if message.from_user.username in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[message.from_user.username]
        result = pokemon.feed()
        bot.send_message(message.chat.id, result)
    else:
        bot.reply_to(message, "Сначала создайте покемона с помощью команды /go")

@bot.message_handler(commands=['attack'])
def attack_pok(message):
    if message.reply_to_message:
        if message.reply_to_message.from_user.username in Pokemon.pokemons.keys() and message.from_user.username in Pokemon.pokemons.keys():
            enemy = Pokemon.pokemons[message.reply_to_message.from_user.username]
            pok = Pokemon.pokemons[message.from_user.username]
            res = pok.attack(enemy)
            bot.send_message(message.chat.id, res)
        else:
            bot.send_message(message.chat.id, "Сражаться можно только с покемонами")
    else:
        bot.send_message(message.chat.id, "Чтобы атаковать, нужно ответить на сообщения того, кого хочешь атаковать")

@bot.message_handler(commands=['help'])
def help(message):
    try:
        help_text = (
            "Доступные команды:\n"
            "/go - Создать нового покемона.\n"
            "/info - Показать информацию о вашем покемоне.\n"
            "/rename <новое_имя> - Изменить имя вашего покемона.\n"
            "/feed - Покормить покемона.\n"
            "/heal - Восстановить здоровье покемона.\n"
            "/attack - Атаковать другого покемона.\n" 
            "/help - Показать список команд и их описание."
        )
        bot.send_message(message.chat.id, help_text)
    except Exception as e:
        bot.reply_to(message, "Ошибка при выполнении команды /help")

@bot.message_handler(commands=['heal'])
def heal_pok(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pok = Pokemon.pokemons[message.from_user.username]
        pok.heal(10)
        bot.send_message(message.chat.id, f"Здоровье покемона восстановлено на 10 единиц. Текущее здоровье: {pok.hp}")
    else:
        bot.send_message(message.chat.id, "Сначала создайте покемона")

bot.infinity_polling(none_stop=True)
