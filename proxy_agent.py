import sc2
from sc2 import Race, Difficulty
from sc2.constants import *
from sc2.player import Bot, Computer
from sc2.unit import Unit
from sc2.units import Units
from sc2.position import Point2
from sc2.ids.unit_typeid import UnitTypeId


class ProxyAgent():
    def __init__(self, Bot):
        self.bot = Bot
    
    async def doAction(self):
        await self.build_barracks()
     #   await self.build_bunker()
        await self.build_army()


    # Build proxy barracks
    async def build_barracks(self):
            if self.bot.structures(UnitTypeId.BARRACKS).amount < 2 and self.bot.already_pending(UnitTypeId.BARRACKS) < 2 :
                if self.bot.can_afford(UnitTypeId.BARRACKS):
                    p: Point2 = self.bot.game_info.map_center.towards(self.bot.enemy_start_locations[0], 25)
                    await self.bot.build(UnitTypeId.BARRACKS, near=p)

   #  async def build_bunker(self):
    #        if(self.bot.can_afford(UnitTypeId.BUNKER)):
     #           if(self.bot.already_pending(UnitTypeId.BUNKER) + self.bot.structures(UnitTypeId.BUNKER).amount < self.bot.townhalls().ready.amount * 3):
      #              p: Point2 = self.bot.game_info.map_center.towards(self.bot.enemy_start_locations[0], 25)
       #             await self.bot.build(UnitTypeId.BUNKER, near=p) 

    # Train marines
    async def build_army(self):
        for rax in self.bot.structures(UnitTypeId.BARRACKS).ready.idle:
            if self.bot.can_afford(UnitTypeId.MARINE):
                rax.train(UnitTypeId.MARINE)