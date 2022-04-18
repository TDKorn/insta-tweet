import os
import json
import random
import pkgutil
from pathlib import Path


class UserAgent(object):
    default_agents = json.loads(pkgutil.get_data(__name__, "default_agents.txt"))

    def __init__(self, agents=None):
        self.agents = agents

        if self.agents is None:
            self.agents = UserAgent.default_agents

    @classmethod
    def common(cls, amount=20):
        return cls(agents=UserAgent.default_agents[:amount])

    @property
    def default(self):
        return self.default_agents[0]['useragent']

    def random(self):
        agent = random.choice(self.agents)
        if isinstance(agent, dict) and agent.get('useragent'):
            return agent['useragent']
        # Continue error check if needed
        return agent


def get_root():
    return Path(__file__).parent.parent


def get_filepath(filename, filetype='.txt'):
    return os.path.join(get_root(), filename) + filetype
