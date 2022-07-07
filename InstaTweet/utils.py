import os
import requests
from pathlib import Path
from typing import Optional


AGENTS = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36']


def get_agents() -> list:
    """Scrapes a list of user agents. Returns a default list if the scrape fails."""
    if (response := requests.get('https://www.whatismybrowser.com/guides/the-latest-user-agent/chrome')).ok:
        section = response.text.split('<h2>Latest Chrome on Windows 10 User Agents</h2>')[1]
        raw_agents = section.split('code\">')[1:]
        agents = [agent.split('<')[0] for agent in raw_agents]
        for a in agents:
            if a not in AGENTS:
                AGENTS.append(a)
    # If function fails, will still return the hardcoded list
    return AGENTS


def get_agent(index: int = 0) -> str:
    """Returns a single user agent string from the specified index of the AGENTS list"""
    return get_agents()[index]  # Specify index only if you hardcode more than 1


def get_proxies(env_key) -> Optional[dict]:
    """Retrieve proxies from an environment variable"""
    if env_key:
        return {
            "http": os.environ[env_key],
            "https": os.environ[env_key]
        }
    return None


def get_root() -> Path:
    return Path(__file__).parent


def get_filepath(filename: str, filetype: str = 'txt') -> str:
    return os.path.join(get_root(), filename) + '.' + filetype
