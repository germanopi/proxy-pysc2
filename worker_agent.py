import sc2
from sc2 import units
from sc2.bot_ai import BotAI
from sc2.player import Bot, Computer
from sc2.ids.unit_typeid import UnitTypeId


class WorkerAgent():
    def __init__(self, Bot):
        self.bot = Bot

    async def doAction(self):
        await self.build_workers()
        await self.bot.distribute_workers()
        await self.build_supplyDepot()
        await self.expand()
        await self.all_in()
        if (self.bot.time > 180):
            await self.build_vespene()

    async def expand(self):
        if self.bot.townhalls().amount < 2 and self.bot.can_afford(UnitTypeId.COMMANDCENTER):
            await self.bot.expand_now()

    async def build_supplyDepot(self):
        if self.bot.supply_left < 6 and not self.bot.already_pending(UnitTypeId.SUPPLYDEPOT):
            for commandCenter in self.bot.townhalls().ready:
                if self.bot.can_afford(UnitTypeId.SUPPLYDEPOT):
                    position_towards_map_center = commandCenter.position.towards(
                        self.bot.game_info.map_center, distance=8)
                    await self.bot.build(UnitTypeId.SUPPLYDEPOT, position_towards_map_center)

    async def build_vespene(self):
        for commandCenter in self.bot.townhalls().ready:
            vespenos = self.bot.vespene_geyser.closer_than(10, commandCenter)
            for vespeno in vespenos:
                if self.bot.can_afford(UnitTypeId.REFINERY):
                    await self.bot.build(UnitTypeId.REFINERY, vespeno)


    async def build_workers(self):
        if(self.bot.can_afford(UnitTypeId.SCV) and self.bot.units(UnitTypeId.SCV).amount + self.bot.already_pending(UnitTypeId.SCV) < self.bot.townhalls().ready.amount * 22):
            for commandCenter in self.bot.townhalls().ready:
                if commandCenter.is_idle:
                    commandCenter.build(UnitTypeId.SCV)
    
     # If we don't have a townhall anymore, send all units to attack
    async def all_in(self):
        ccs: Units = self.bot.townhalls(UnitTypeId.COMMANDCENTER)
        if not ccs:
            target: Point2 = self.bot.enemy_structures.random_or(self.bot.enemy_start_locations[0]).position
            for unit in self.bot.workers | self.bot.units(UnitTypeId.MARINE):
                unit.attack(target)