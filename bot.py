import telebot
from extensions import APIException, Convertor
from token import TOKEN

currencies = {
    'евро' : 'EUR',
    'доллар' : 'USD',
    'рубль' : 'RUB',
}

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start','help'])
def help (message: telebot.types.Message):
    bot.send_message(message.chat.id, "Привет, я - бот-конвертер")
    text = 'Введите комманду в следующем виде: \n<валюта, которую необходимо перевести> \n<валюта, в которую надо перевести> ' \
           '\n<колличество переводимой валюты>\nНапример: евро рубль 1\nСписок доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные для конвертации валюты:\n'
    for key in currencies.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    input_values = message.text.split(' ')
    if len(input_values) != 3:
        bot.send_message(message.chat.id, "Неверное количество параметров. Попробуйте снова.")
        return
    quote, base, amount = input_values
    quote_ticker = currencies.get(quote.lower())
    base_ticker = currencies.get(base.lower())

    if not quote_ticker or not base_ticker:
        bot.send_message(message.chat.id, "Неверно указаны валюты. Попробуйте снова.")
        return

    try:
        converted_amount = Convertor.get_price(quote_ticker, base_ticker, amount)
        converted_message = f"{amount} {quote_ticker} = {converted_amount} {base_ticker}"
        bot.send_message(message.chat.id, converted_message)
    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка конвертации: {str(e)}")

bot.polling(none_stop=True)




