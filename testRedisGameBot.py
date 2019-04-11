import telebot
from telebot import types
import logging
from telegram_game.redis_game import RedisGame, RedisField
import json

token_file = open('token')
TOKEN = token_file.read()
bot = telebot.TeleBot(TOKEN)
logger = logging.getLogger(__name__)


with open('testJSON.json') as json_file:
    script = json.load(json_file)


class Game(RedisGame):
    currentPoint = RedisField(0)
    last_point = RedisField(0)

    async def start(self):
        print(self.currentPoint)
        await self.send('Let`s play the Game!')


        while True:
            msg = await self.recv()
            chat_id = msg['message']['chat']['id']
            print(self.currentPoint)
            msg_text = msg['message']['text']
            self.currentPoint = self.point_definition(msg_text)
            self.send_message(chat_id)



    def point_definition(self, msg_text):
        self.last_point = self.currentPoint
        ans_one = script[self.last_point]['textBtnOne']
        callback_one = script[self.last_point]['CallbackDataBtnOne']
        ans_two = script[self.last_point]['textBtnTwo']
        callback_two = script[self.last_point]['CallbackDataBtnTwo']
        if msg_text == ans_one:
            return int(callback_one)
        elif msg_text == ans_two:
            return int(callback_two)
        else:
            return 0

    def send_message(self, chat_id):
        key = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btnOne = types.KeyboardButton(text=script[self.currentPoint]['textBtnOne'])
        btnTwo = types.KeyboardButton(text=script[self.currentPoint]['textBtnTwo'])
        key.add(btnOne, btnTwo)
        bot.send_message(chat_id, text=script[self.currentPoint]['textMsg'], reply_markup=key)