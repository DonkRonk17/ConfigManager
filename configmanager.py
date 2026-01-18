#!/usr/bin/env python3
"""ConfigManager v1.0 - Centralized Configuration for Team Brain"""
import json
from pathlib import Path

VERSION = "1.0.0"
CONFIG_FILE = Path("D:/BEACON_HQ/TEAM_BRAIN_CONFIG.json")

DEFAULT_CONFIG = {
    "synapse_path": "D:/BEACON_HQ/MEMORY_CORE_V2/03_INTER_AI_COMMS/THE_SYNAPSE/active",
    "memory_bridge_db": "D:/BEACON_HQ/MEMORY_CORE_V2/00_SHARED_MEMORY/memory_bridge.db",
    "task_queue_db": "D:/BEACON_HQ/TASK_QUEUE/taskqueue.db",
    "agents": {
        "ATLAS": {"model": "sonnet-4.5", "role": "builder"},
        "FORGE": {"model": "opus-4.5", "role": "orchestrator"},
        "CLIO": {"model": "sonnet-4.5", "role": "linux-specialist"},
        "BOLT": {"model": "grok", "role": "executor"}
    }
}

class ConfigManager:
    def __init__(self, config_file=CONFIG_FILE):
        self.config_file = config_file
        self.config = self._load()
    
    def _load(self):
        if self.config_file.exists():
            return json.loads(self.config_file.read_text())
        return DEFAULT_CONFIG.copy()
    
    def save(self):
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        self.config_file.write_text(json.dumps(self.config, indent=2))
    
    def get(self, key, default=None):
        return self.config.get(key, default)
    
    def set(self, key, value):
        self.config[key] = value
        self.save()

def main():
    config = ConfigManager()
    print(f"Config loaded from: {config.config_file}")
    print(f"Synapse path: {config.get('synapse_path')}")

if __name__ == "__main__":
    main()
