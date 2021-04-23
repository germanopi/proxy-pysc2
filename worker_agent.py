import sc2
from sc2 import units
from sc2.bot_ai import BotAI
from sc2.player import Bot, Computer
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.unit import Unit
from sc2.units import Units


class WorkerAgent():
    def __init__(self, Bot):
        self.bot = Bot
        self.baseBarracks = []
        self.rampbool = False

    async def doAction(self):
        await self.build_workers()
        await self.check_ramp()
        if not self.rampbool:
            await self.supply_ramp()
            #await self.barracks_ramp()
        else:
            await self.build_supplyDepot()
        await self.bot.distribute_workers()
        await self.expand()
        await self.all_in()
        if (self.bot.time > 180):
            await self.build_vespene()

    async def check_ramp(self):
        for depo in self.bot.structures(UnitTypeId.SUPPLYDEPOT).ready:
            for unit in self.bot.enemy_units:
                if unit.distance_to(depo) < 15:
                    break
            else:
                depo(AbilityId.MORPH_SUPPLYDEPOT_LOWER)

        # Lower depos when no enemies are nearby
        for depo in self.bot.structures(UnitTypeId.SUPPLYDEPOTLOWERED).ready:
            for unit in self.bot.enemy_units:
                if unit.distance_to(depo) < 10:
                    depo(AbilityId.MORPH_SUPPLYDEPOT_RAISE)
                    break

    async def supply_ramp(self):
        depot_placement_positions = self.bot.main_base_ramp.corner_depots | {self.bot.main_base_ramp.depot_in_middle}
        depots: Units = self.bot.structures.of_type({UnitTypeId.SUPPLYDEPOT, UnitTypeId.SUPPLYDEPOTLOWERED})
        if depots:
            depot_placement_positions: Set[Point2] = {
                d for d in depot_placement_positions if depots.closest_distance_to(d) > 1
            }
        if self.bot.can_afford(UnitTypeId.SUPPLYDEPOT) and self.bot.already_pending(UnitTypeId.SUPPLYDEPOT) == 0:
            if len(depot_placement_positions) == 0:
                self.rampbool = True
                return
            # Choose any depot location
            target_depot_location: Point2 = depot_placement_positions.pop()
            workers: Units = self.bot.workers.gathering
            if workers:  # if workers were found
                worker: Unit = workers.random
                self.bot.do(worker.build(UnitTypeId.SUPPLYDEPOT, target_depot_location))

    async def barracks_ramp(self):
        barracks_placement_position: Point2 = self.bot.main_base_ramp.barracks_correct_placement
        depots: Units = self.bot.structures.of_type({UnitTypeId.SUPPLYDEPOT, UnitTypeId.SUPPLYDEPOTLOWERED})
        if depots.ready and self.bot.can_afford(UnitTypeId.BARRACKS) and self.bot.already_pending(UnitTypeId.BARRACKS) == 0:
            workers = self.bot.workers.gathering
            if workers and barracks_placement_position:  # if workers were found
                worker: Unit = workers.random
                worker.build(UnitTypeId.BARRACKS, barracks_placement_position)
                self.rampbool = True

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