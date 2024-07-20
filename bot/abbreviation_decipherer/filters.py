import random
from aiogram.types import Message
from aiogram.filters import Filter


class RandomFilter(Filter):
    """
    сообщение будет обработано с вероятностью chance
    """

    def __init__(self, chance=0.08):
        self.chance = chance

    async def __call__(self, message: Message) -> bool:
        return random.random() < self.chance
