import sc2
from sc2 import units
from sc2.bot_ai import BotAI
from sc2.player import Bot, Computer
from sc2.ids.unit_typeid import UnitTypeId
from worker_agent import WorkerAgent
from proxy_agent import ProxyAgent
from fighter_agent import FighterAgent

class MasterAgent(sc2.BotAI):
    
    async def on_step(self, iteration):
        WorkerAgent.on_step()
        if self.can_afford(UnitTypeId.BARRACKS):
            ProxyAgent()
            FighterAgent()

sc2.run_game(
    sc2.maps.get("AcropolisLE"),
    [Bot(sc2.Race.Terran, MasterAgent()), Computer(
        sc2.Race.Zerg, sc2.Difficulty.Easy)],
    realtime=False,
)
