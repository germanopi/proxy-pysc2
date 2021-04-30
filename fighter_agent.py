import sc2
from sc2 import Race, Difficulty
from sc2.constants import *
from sc2.player import Bot, Computer
from sc2.unit import Unit
from sc2.units import Units
from sc2.position import Point2
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId


class FighterAgent():
    def __init__(self, Bot):
        self.bot = Bot
        self.defesa = None
        self.ataque = None
        self.ataqueutil = False
        self.defesautil = None

    async def doAction(self):
        if self.bot.time < 420: 
            await self.proxyattack()
        
        if self.bot.time > 420:
            army: Units = self.bot.units(UnitTypeId.MARAUDER).idle | self.bot.units(UnitTypeId.MEDIVAC).idle | self.bot.units(UnitTypeId.MARINE).idle
            if self.ataqueutil:
                self.ataqueutil = True
                await self.offensive_stance()
            else:
                await self.defensive_stance()
    #SAVING FOR NEXT

    # Send marines in waves of 8, each time 8 are idle, send them to their death
    async def proxyattack(self):
        marines: Units = self.bot.units(UnitTypeId.MARINE).idle
        if marines.amount > 2:
            target: Point2 = self.bot.enemy_structures.random_or(self.bot.enemy_start_locations[0]).position
            for marine in marines:
                marine.attack(target)
    
    async def defensive_stance(self):
        army: Units = self.bot.units(UnitTypeId.MARAUDER).idle | self.bot.units(UnitTypeId.MEDIVAC).idle | self.bot.units(UnitTypeId.MARINE).idle
        if len(army) > 15:
            self.ataqueutil = True
        # padrao
        self.defesa = self.bot.main_base_ramp.top_center
        for commandCenter in self.bot.townhalls().ready:
            new_pos = commandCenter.position.towards(self.bot.game_info.map_center, 7)
            if new_pos.distance_to(self.bot.game_info.map_center) < self.defesa.distance_to(self.bot.game_info.map_center):
                self.defesa = new_pos
        # por perigo
        self.defesautil = 0
        for commandCenter in self.bot.townhalls().ready:
            enemy_group = self.bot.enemy_units.closer_than(20, commandCenter)
            if self.defesautil < enemy_group.amount:
                self.defesautil = enemy_group.amount
                self.defesa = enemy_group.center
        for unit in army:
            exists_close = self.bot.enemy_units.closer_than(unit.sight_range, unit).exists
            if exists_close:
                self.bot.do(unit.attack(self.bot.enemy_units.center))
            else:
                self.bot.do(unit.attack(self.defesa)) #.random_on_distance(15)

    async def offensive_stance(self):
        army: Units = self.bot.units(UnitTypeId.MARAUDER) | self.bot.units(UnitTypeId.MEDIVAC) | self.bot.units(UnitTypeId.MARINE)
        bio: Units = self.bot.units(UnitTypeId.MARAUDER) | self.bot.units(UnitTypeId.MARINE)
        medivac = self.bot.units(UnitTypeId.MEDIVAC)

        self.ataqueutil = True
        #atacar base mais proxima da minha base
        #special = self.ataque == None
        # self.ataque = None
        # best_dist = 129381
        # for structure in self.bot.enemy_structures:
        #     if best_dist > structure.position.distance_to(self.__bot.start_location):
        #         best_dist = structure.position.distance_to(self.__bot.start_location)
        #         self.ataque = structure.position
        # if self.ataque == None:
        #     self.ataque = self.bot.enemy_start_locations[0]
        # #self.ataqueutil = self.ataqueutil.towards(self.ataque, min(self.ataque.distance_to(self.ataqueutil), 20))

        target: Point2 = self.bot.enemy_structures.random_or(self.bot.enemy_start_locations[0]).position
        for unit in bio:
            in_range = False
            exists_close = self.bot.enemy_units.closer_than(unit.sight_range, unit).exists
            in_range = self.bot.enemy_units.closer_than(unit.ground_range, unit).exists
            if exists_close:
                if in_range and unit.health > 40 and len(unit.buffs)<1:
                    #print("stimpack")
                    self.bot.do(unit(AbilityId.EFFECT_STIM))
                self.bot.do(unit.attack(self.bot.enemy_units.center))
            else:
                self.bot.do(unit.attack(target)) #.random_on_distance(15)
            if len(unit.buffs)>0:
                print(unit.buffs)
        for unit in medivac:
            self.bot.do(unit.attack(bio.closest_to(self.bot.enemy_start_locations[0])))
        if len(army)<5:
            self.ataqueutil = False
            self.bot.do(unit.move(self.defesa))

            

    