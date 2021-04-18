import sc2
from sc2 import Race, Difficulty
from sc2.constants import *
from sc2.player import Bot, Computer
from sc2.unit import Unit
from sc2.units import Units
from sc2.position import Point2
from sc2.ids.unit_typeid import UnitTypeId


class ProxyAgent(sc2.BotAI):
    async def on_step(self, iteration):
        await self.build_barracks()
        await self.build_bunker()
        await self.build_army()


    # Build proxy barracks
    async def build_barracks(self):
        for commandCenter in self.townhalls().ready:
            if self.structures(UnitTypeId.BARRACKS).amount < 3 or (
                self.can_afford(UnitTypeId.BARRACKS) and self.structures(UnitTypeId.BARRACKS).amount < 5
            ):
                if self.can_afford(UnitTypeId.BARRACKS):
                    p: Point2 = self.game_info.map_center.towards(self.enemy_start_locations[0], 25)
                    await self.build(UnitTypeId.BARRACKS, near=p)

    async def build_bunker(self):
        for commandCenter in self.townhalls().ready:
            if(self.can_afford(UnitTypeId.BUNKER)):
                if(self.structures.closer_than(18, commandCenter.position).filter(lambda structure: structure.type_id == UnitTypeId.BUNKER).amount < 3):
                    if(self.already_pending(UnitTypeId.BUNKER) + self.structures(UnitTypeId.BUNKER).amount < self.townhalls().ready.amount * 3):
                        p: Point2 = self.game_info.map_center.towards(self.enemy_start_locations[0], 25)
                        await self.build(UnitTypeId.BUNKER, near=p)

    # Train marines
    async def build_army(self):
        for rax in self.structures(UnitTypeId.BARRACKS).ready.idle:
            if self.can_afford(UnitTypeId.MARINE):
                rax.train(UnitTypeId.MARINE)