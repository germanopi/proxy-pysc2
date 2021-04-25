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
        self.defesa = None
        self.ataque = None
        self.defesautil = None

    async def doAction(self):
        if self.bot.time < 420: 
            await self.proxyattack()
        if self.bot.time > 420: 
            await self.defensive_stance()
    #SAVING FOR NEXT

    # Send marines in waves of 8, each time 8 are idle, send them to their death
    async def proxyattack(self):
        marines: Units = self.bot.units(UnitTypeId.MARINE).idle
        if marines.amount > 8:
            target: Point2 = self.bot.enemy_structures.random_or(self.bot.enemy_start_locations[0]).position
            for marine in marines:
                marine.attack(target)
    
    async def defensive_stance(self):
        army: Units = self.bot.units(UnitTypeId.MARAUDERS).idle | self.bot.units(UnitTypeId.MEDIVAC).idle | self.bot.units(UnitTypeId.MARINE).idle
        # padrao
        self.defesa = self.bot.main_base_ramp.top_center
        for commandCenter in self.bot.townhalls().ready:
            new_pos = commandCenter.position.towards(self.bot.game_info.map_center, 7)
            if new_pos.distance_to(self.bot.game_info.map_center) < self.defesa.distance_to(self.bot.game_info.map_center):
                self.defesa = new_pos
        # por perigo
        self.defesautil = 0
        for commandCenter in self.bot.townhalls().ready:
            enemy_group = self.bot.state.enemy_units.closer_than(20, commandCenter)
            if self.defesautil < enemy_group.amount:
                self.defesautil = enemy_group.amount
                self.defesa = enemy_group.center
        for unit in army:
            exists_close = bot.state.enemy_units.closer_than(unit.sight_range, unit).exists
            #if exists_close:
            #    await self.attack_pattern(iteration, unit, bot, exists_close)
            #else:
            await bot.do(unit.attack(self.defesa.random_on_distance(15)))
    