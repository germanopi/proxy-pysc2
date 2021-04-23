import sc2
from sc2 import units
from sc2.bot_ai import BotAI
from sc2.player import Bot, Computer
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.ids.upgrade_id import UpgradeId
from sc2.unit import Unit
from sc2.units import Units



class MilitarWorker():
    def __init__(self, Bot):
        self.bot = Bot
        self.barracktech = []

    async def doAction(self):
        if self.bot.time >60 and self.bot.minerals>250:
            await self.build_barracks()
            await self.upgrade_techlab()
            await self.build_engineering_bay()
            await self.build_factory()
            await self.build_starport()
            #await self.build_armory()
            await self.build_army()
        
    # Remover for de townhalls onde reelevante
    async def build_engineering_bay(self):
        for commandCenter in self.bot.townhalls().ready:
            if self.bot.can_afford(UnitTypeId.ENGINEERINGBAY) and self.bot.structures(UnitTypeId.ENGINEERINGBAY).amount <1  :
                if(self.bot.already_pending(UnitTypeId.ENGINEERINGBAY) + self.bot.structures(UnitTypeId.ENGINEERINGBAY).amount < 1):
                    position_towards_map_center=commandCenter.position.towards(
                        self.bot.game_info.map_center, distance=8)
                    await self.bot.build(UnitTypeId.ENGINEERINGBAY, position_towards_map_center)

        if self.bot.already_pending_upgrade(UpgradeId.TERRANINFANTRYWEAPONSLEVEL1) == 0 and self.bot.can_afford(UpgradeId.TERRANINFANTRYWEAPONSLEVEL1):
            bay_ready = self.bot.structures(UnitTypeId.ENGINEERINGBAY).ready
            if bay_ready:
                self.bot.research(UpgradeId.TERRANINFANTRYWEAPONSLEVEL1)
    
    async def build_factory(self):
        for commandCenter in self.bot.townhalls().ready:
            if self.bot.can_afford(UnitTypeId.FACTORY) and self.bot.structures(UnitTypeId.FACTORY).amount <1:
                if(self.bot.structures.closer_than(25, commandCenter.position).filter(lambda structure: structure.type_id == UnitTypeId.FACTORY).amount < 1):
                    position_towards_map_center=commandCenter.position.towards(
                        self.bot.game_info.map_center, distance=12)
                    await self.bot.build(UnitTypeId.FACTORY, position_towards_map_center)

    async def build_armory(self):
        for commandCenter in self.bot.townhalls().ready:
            if self.bot.can_afford(UnitTypeId.ARMORY):
                if(self.bot.already_pending(UnitTypeId.ARMORY) + self.bot.structures(UnitTypeId.ARMORY).amount < 1):
                    position_towards_map_center=commandCenter.position.towards(
                        self.bot.game_info.map_center, distance=8)
                    await self.bot.build(UnitTypeId.ARMORY, position_towards_map_center)

    async def build_starport(self):
        for commandCenter in self.bot.townhalls().ready:
            if self.bot.can_afford(UnitTypeId.STARPORT):
                if(self.bot.already_pending(UnitTypeId.STARPORT) + self.bot.structures(UnitTypeId.STARPORT).amount < 1):
                    position_towards_map_center=commandCenter.position.towards(
                        self.bot.game_info.map_center, distance=8)
                    await self.bot.build(UnitTypeId.STARPORT, position_towards_map_center)

    async def build_barracks(self):
        for commandCenter in self.bot.townhalls().ready:
            if(self.bot.can_afford(UnitTypeId.BARRACKS)):
                if not self.bot.already_pending(UnitTypeId.BARRACKS):
                    if(self.bot.structures.closer_than(25, commandCenter.position).filter(lambda structure: structure.type_id == UnitTypeId.BARRACKS).amount < 2):
                        position_towards_map_center=commandCenter.position.towards(
                            self.bot.game_info.map_center, distance=14)
                        await self.bot.build(UnitTypeId.BARRACKS, position_towards_map_center)
                        #SELECIONAR AS BARRACA PERTO E DAR O UPGRADE QUE FAZ MARAUDER

    async def upgrade_techlab(self):
        if(self.bot.already_pending(UnitTypeId.BARRACKSTECHLAB) + self.bot.structures(UnitTypeId.BARRACKSTECHLAB).amount < 1) and self.bot.can_afford(UnitTypeId.BARRACKSTECHLAB): 
            for commandCenter in self.bot.townhalls().ready:
                for barracas in self.bot.structures.closer_than(25, commandCenter.position).filter(lambda structure: structure.type_id == UnitTypeId.BARRACKS):
                    self.bot.do(barracas.build(UnitTypeId.BARRACKSTECHLAB))
        if self.bot.already_pending_upgrade(UpgradeId.STIMPACK) == 0 and self.bot.can_afford(UpgradeId.STIMPACK):
            techlab_ready = self.bot.structures(UnitTypeId.BARRACKSTECHLAB).ready
            if techlab_ready:
                self.bot.research(UpgradeId.STIMPACK)

# SELECIONAR BARRACAS DA BASE APENAS
    async def build_army(self):
        unit = None
        if self.bot.can_afford(UnitTypeId.MARAUDER)  and self.bot.units(UnitTypeId.MARAUDER).amount < 4:
            unit = UnitTypeId.MARAUDER
        elif self.bot.can_afford(UnitTypeId.MEDIVAC) and self.bot.units(UnitTypeId.MEDIVAC).amount < 3:
            unit = UnitTypeId.MEDIVAC
        elif self.bot.can_afford(UnitTypeId.MARINE) and self.bot.units(UnitTypeId.MARINE).amount < 8:
            unit = UnitTypeId.MARINE
        elif self.bot.can_afford(UnitTypeId.MARAUDER):
            unit = UnitTypeId.MARAUDER
        elif self.bot.can_afford(UnitTypeId.MARINE):
            unit = UnitTypeId.MARINE
        if not unit:
            return
        for rax in self.bot.structures.of_type({UnitTypeId.BARRACKS, UnitTypeId.STARPORT}).ready.idle:
            if(unit == UnitTypeId.MARAUDER and rax.type_id == UnitTypeId.BARRACKS and rax.has_techlab):
                rax.train(unit)
            elif(unit == UnitTypeId.MARINE and rax.type_id == UnitTypeId.BARRACKS):
                rax.train(unit)
            elif(unit == UnitTypeId.MEDIVAC and rax.type_id == UnitTypeId.STARPORT):
                rax.train(unit)
            else:
                return
           