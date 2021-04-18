import sc2
from sc2 import units
from sc2.bot_ai import BotAI
from sc2.player import Bot, Computer
from sc2.ids.unit_typeid import UnitTypeId


class WorkerAgent(sc2.BotAI):
    async def on_step(self, iteration: int):
        await self.build_workers()
        await self.distribute_workers()
        await self.build_vespene()
        await self.build_supplyDepot()
        await self.expand()
        await self.all_in()

    async def expand(self):
        if self.townhalls().amount < 2 and self.can_afford(UnitTypeId.COMMANDCENTER):
            await self.expand_now()

    async def build_supplyDepot(self):
        if self.supply_left < 6 and not self.already_pending(UnitTypeId.SUPPLYDEPOT):
            for commandCenter in self.townhalls().ready:
                if self.can_afford(UnitTypeId.SUPPLYDEPOT):
                    position_towards_map_center = commandCenter.position.towards(
                        self.game_info.map_center, distance=8)
                    await self.build(UnitTypeId.SUPPLYDEPOT, position_towards_map_center)

    async def build_vespene(self):
        for commandCenter in self.townhalls().ready:
            vespenos = self.vespene_geyser.closer_than(10, commandCenter)
            for vespeno in vespenos:
                if self.can_afford(UnitTypeId.REFINERY):
                    await self.build(UnitTypeId.REFINERY, vespeno)

    async def build_engineering_bay(self):
        for commandCenter in self.townhalls().ready:
            if(self.can_afford(UnitTypeId.ENGINEERINGBAY)):
                if(self.already_pending(UnitTypeId.ENGINEERINGBAY) + self.structures(UnitTypeId.ENGINEERINGBAY).amount < 1):
                    position_towards_map_center=commandCenter.position.towards(
                        self.game_info.map_center, distance=8)
                    await self.build(UnitTypeId.ENGINEERINGBAY, position_towards_map_center)

    async def build_workers(self):
        if(self.can_afford(UnitTypeId.SCV) and self.units(UnitTypeId.SCV).amount + self.already_pending(UnitTypeId.SCV) < self.townhalls().ready.amount * 22):
            for commandCenter in self.townhalls().ready:
                if commandCenter.is_idle:
                    commandCenter.build(UnitTypeId.SCV)
    
     # If we don't have a townhall anymore, send all units to attack
    async def all_in(self):
        ccs: Units = self.townhalls(UnitTypeId.COMMANDCENTER)
        if not ccs:
            target: Point2 = self.enemy_structures.random_or(self.enemy_start_locations[0]).position
            for unit in self.workers | self.units(UnitTypeId.MARINE):
                unit.attack(target)