import sc2
from sc2 import units
from sc2.bot_ai import BotAI
from sc2.player import Bot, Computer
from sc2.ids.unit_typeid import UnitTypeId
from worker_agent import WorkerAgent
from proxy_agent import ProxyAgent
from fighter_agent import FighterAgent
from militar_worker import MilitarWorker

class MasterAgent(sc2.BotAI):
    def __init__(self):
        self.workerAgent = WorkerAgent(self)
        self.proxyAgent = ProxyAgent(self)
        self.fighterAgent = FighterAgent(self)
        self.militarWorker = MilitarWorker(self)

    async def on_step(self, iteration):
        if self.can_afford(UnitTypeId.BARRACKS):
            if self.time < 420:
                await self.proxyAgent.doAction()
            await self.fighterAgent.doAction()
        await self.militarWorker.doAction()
        await self.workerAgent.doAction()

sc2.run_game(
    sc2.maps.get("AcropolisLE"),
    [Bot(sc2.Race.Terran, MasterAgent()), Computer(
        sc2.Race.Protoss, sc2.Difficulty.Hard)],
    realtime=False,
)
