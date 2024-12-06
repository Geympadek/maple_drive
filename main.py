import loader
from loader import dp, bot, app

from aiogram import types
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter

from flask import request, redirect, render_template

import api
import auth

@dp.message(Command("start"))
async def on_start(msg: types.Message, state: FSMContext):
    await msg.answer(text="Maple drive - это облачный диск, встроенный в телеграм.")

@app.route("/")
def index():
    return render_template("index.html")

async def main():
    app.run(host="192.168.0.109", debug=True, ssl_context=("ssl/triangle.run.place.cer", "ssl/triangle.run.place.key"))
    pass

import asyncio

if __name__ == "__main__":
    asyncio.run(main())