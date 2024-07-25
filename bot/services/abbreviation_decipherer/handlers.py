import random
import re

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from abbreviation_decipherer.abbreviation_decipherer import get_deciphers
from abbreviation_decipherer.filters import RandomFilter

abbreviation_decipherer_router = Router()


@abbreviation_decipherer_router.message(RandomFilter(chance=0.04))
async def abbr_message_handler(msg: Message):
    """
    обрабатывает сообщение с некоторой вероятностью сообщения,
    из строки берётся одно случайное слово и ему даётся расшировка
    """
    msg_text = msg.text.lower()
    msg_text = re.sub("[^\w]", " ", msg_text).strip()
    words = set(msg_text.split())
    if not words:
        return
    variants = list()
    for w in words:
        if len(w) > 5:
            continue
        norm_word = w.strip()
        is_orig, corr_abbr, deciphers = get_deciphers(norm_word)
        if deciphers:
            variants.append((w, is_orig, corr_abbr, deciphers))
    if not variants:
        return

    random_abbr = random.choice(variants)
    random_decipher = random.choice(random_abbr[3])
    orig_abbr = random_abbr[0]
    is_orig = random_abbr[1]
    corr_abbr = random_abbr[2]

    if is_orig == 1:
        text = f'Пиши НЕ <b>"{orig_abbr}"</b>, a <b>"{random_decipher}"</b>'
    elif is_orig == 0:
        text = f'Тебе так лень написать <b>"{random_decipher}"</b> вместо <b>"{orig_abbr}"</b>?!'
    else:
        text = "Позовите Серёгу, мне плохо от ваших сокращений."
    await msg.reply(text)


@abbreviation_decipherer_router.message(Command("abbr"))
async def abbr_command_handler(msg: Message):
    """
    обрабатывает команду abbr, которая имеет аргумент строку
    из строки берётся одно случайное слово и ему даётся расшировка
    (подразумевается, что будет передаваться только одно слово)
    """
    msg_text = msg.text.lower()
    msg_text = re.sub("[^\w]", " ", msg_text).strip()
    words = set(msg_text.split())
    if not words:
        return
    variants = list()
    for w in words:
        norm_word = w.strip()
        is_orig, corr_abbr, deciphers = get_deciphers(norm_word)
        if deciphers:
            variants.append((w, is_orig, corr_abbr, deciphers))
    if not variants:
        return

    random_abbr = random.choice(variants)
    random_decipher = random.choice(random_abbr[3])
    orig_abbr = random_abbr[0]
    is_orig = random_abbr[1]
    corr_abbr = random_abbr[2]

    if is_orig == 1:
        text = f'Пиши НЕ <b>"{orig_abbr}"</b>, a <b>"{random_decipher}"</b>'
    elif is_orig == 0:
        text = f'Тебе так лень написать <b>"{random_decipher}"</b> вместо <b>"{orig_abbr}"</b>?!'
    else:
        text = "Позовите Серёгу, мне плохо от ваших сокращений."
    await msg.reply(text)
