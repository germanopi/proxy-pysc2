import sc2
from sc2 import units
from sc2.bot_ai import BotAI
from sc2.player import Bot, Computer
from sc2.ids.unit_typeid import UnitTypeId
from worker_agent import WorkerAgent
from proxy_agent import ProxyAgent
from fighter_agent import FighterAgent

class MasterAgent(sc2.BotAI):
    workerAgent = None
    proxyAgent = None
    fighterAgent = None

    async def on_step(self, iteration):
        init = True
        if init:
            self.workerAgent = WorkerAgent(self)
            self.proxyAgent = ProxyAgent(self)
            self.fighterAgent = FighterAgent(self)
            init = False
        else:
            self.workerAgent.doAction()
            if self.can_afford(UnitTypeId.BARRACKS):
                self.proxyAgent.doAction()
                self.fighterAgent.doAction()


sc2.run_game(
    sc2.maps.get("AcropolisLE"),
    [Bot(sc2.Race.Terran, MasterAgent()), Computer(
        sc2.Race.Zerg, sc2.Difficulty.Easy)],
    realtime=False,
)
