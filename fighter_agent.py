import sc2
from sc2 import Race, Difficulty
from sc2.constants import *
from sc2.player import Bot, Computer
from sc2.unit import Unit
from sc2.units import Units
from sc2.position import Point2
from sc2.ids.unit_typeid import UnitTypeId


class FighterAgent():
    def __init__(self, Bot):
        self.bot = Bot

    async def doAction(self):
        await self.attack()

    #SAVING FOR NEXT

    # Send marines in waves of 15, each time 15 are idle, send them to their death
    async def attack(self):
        marines: Units = self.bot.units(UnitTypeId.MARINE).idle
        if marines.amount > 8:
            target: Point2 = self.bot.enemy_structures.random_or(self.bot.enemy_start_locations[0]).position
            for marine in marines:
                marine.attack(target)
    
    