import sc2
from sc2 import units
from sc2.bot_ai import BotAI
from sc2.player import Bot, Computer
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId



class MilitarWorker():
    def __init__(self, Bot):
        self.bot = Bot

    async def doAction(self):
        if self.bot.time >180:
            await self.build_engineering_bay()
            await self.build_factory()
            await self.build_armory()
            await self.build_barracks()
            await self.build_army()
            await self.upgrade_techlab()
        
    # Remover for de townhalls onde reelevante
    async def build_engineering_bay(self):
        for commandCenter in self.bot.townhalls().ready:
            if self.bot.can_afford(UnitTypeId.ENGINEERINGBAY) and self.bot.structures(UnitTypeId.ENGINEERINGBAY).amount <1  :
                if(self.bot.already_pending(UnitTypeId.ENGINEERINGBAY) + self.bot.structures(UnitTypeId.ENGINEERINGBAY).amount < 1):
                    position_towards_map_center=commandCenter.position.towards(
                        self.bot.game_info.map_center, distance=8)
                    await self.bot.build(UnitTypeId.ENGINEERINGBAY, position_towards_map_center)
    
    async def build_factory(self):
        for commandCenter in self.bot.townhalls().ready:
            if self.bot.can_afford(UnitTypeId.FACTORY) and self.bot.structures(UnitTypeId.FACTORY).amount <2 :
                if(self.bot.structures.closer_than(12, commandCenter.position).filter(lambda structure: structure.type_id == UnitTypeId.FACTORY).amount < 1):
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

    async def build_barracks(self):
        for commandCenter in self.bot.townhalls().ready:
            if(self.bot.can_afford(UnitTypeId.BARRACKS)):
                if not self.bot.already_pending(UnitTypeId.BARRACKS):
                    if(self.bot.structures.closer_than(15, commandCenter.position).filter(lambda structure: structure.type_id == UnitTypeId.BARRACKS).amount < 2):
                        position_towards_map_center=commandCenter.position.towards(
                            self.bot.game_info.map_center, distance=12)
                        await self.bot.build(UnitTypeId.BARRACKS, position_towards_map_center)
                        #SELECIONAR AS BARRACA PERTO E DAR O UPGRADE QUE FAZ MARAUDER

    async def upgrade_techlab(self):
        for rax in self.bot.structures(UnitTypeId.BARRACKS).ready.idle:
            rax(AbilityId.BUILD_TECHLAB_BARRACKS)

# SELECIONAR BARRACAS DA BASE APENAS
    async def build_army(self):
        unit = None
        if self.bot.can_afford(UnitTypeId.MARAUDER)  and self.bot.units(UnitTypeId.MARAUDER).amount < 8:
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
        for rax in self.bot.structures(UnitTypeId.BARRACKS).ready.idle:
            if(unit == UnitTypeId.MARAUDER and rax.has_techlab):
                rax.train(unit)
            elif(unit == UnitTypeId.MARINE):
                rax.train(unit)
            else:
                return
           