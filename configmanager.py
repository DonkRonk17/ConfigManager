#!/usr/bin/env python3
"""
ConfigManager v1.0 - Centralized Configuration for Team Brain

One config file to rule them all! Centralized configuration management for
all Team Brain tools. Change paths, settings, and agent configs in one place.

Author: Atlas (Team Brain)
Requested by: Forge
Date: January 18, 2026
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional, List
from dataclasses import dataclass, asdict

VERSION = "1.0.0"

# Default config file location
DEFAULT_CONFIG_FILE = Path("D:/BEACON_HQ/TEAM_BRAIN_CONFIG.json")

# Default configuration
DEFAULT_CONFIG = {
    "version": "1.0.0",
    "paths": {
        "synapse": "D:/BEACON_HQ/MEMORY_CORE_V2/03_INTER_AI_COMMS/THE_SYNAPSE/active",
        "memory_bridge_db": "D:/BEACON_HQ/MEMORY_CORE_V2/00_SHARED_MEMORY/memory_bridge.db",
        "task_queue_db": "D:/BEACON_HQ/TASK_QUEUE/taskqueue.db",
        "memory_core": "D:/BEACON_HQ/MEMORY_CORE_V2",
        "beacon_hq": "D:/BEACON_HQ"
    },
    "agents": {
        "ATLAS": {
            "model": "sonnet-4.5",
            "role": "builder",
            "capabilities": ["tool_creation", "testing", "documentation"]
        },
        "FORGE": {
            "model": "opus-4.5",
            "role": "orchestrator",
            "capabilities": ["planning", "architecture", "review"]
        },
        "CLIO": {
            "model": "sonnet-4.5",
            "role": "linux-specialist",
            "capabilities": ["system_admin", "deployment", "automation"]
        },
        "BOLT": {
            "model": "grok",
            "role": "executor",
            "capabilities": ["code_execution", "testing", "quick_tasks"]
        },
        "NEXUS": {
            "model": "sonnet-4.5",
            "role": "tester",
            "capabilities": ["comprehensive_testing", "qa", "validation"]
        }
    },
    "settings": {
        "default_poll_interval": 1.0,
        "max_retries": 3,
        "timeout_seconds": 30,
        "log_level": "INFO"
    }
}


@dataclass
class AgentConfig:
    """Configuration for an agent."""
    model: str
    role: str
    capabilities: List[str]


class ConfigManager:
    """
    Centralized configuration manager for Team Brain tools.
    
    Usage:
        config = ConfigManager()
        
        # Get path
        synapse_path = config.get_path("synapse")
        
        # Get agent config
        atlas = config.get_agent("ATLAS")
        
        # Get setting
        poll_interval = config.get_setting("default_poll_interval")
        
        # Update config
        config.set_path("synapse", "/new/path")
        config.save()
    """
    
    def __init__(self, config_file: Optional[Path] = None):
        """
        Initialize ConfigManager.
        
        Args:
            config_file: Path to config file (uses default if not provided)
        """
        self.config_file = config_file or DEFAULT_CONFIG_FILE
        self.config = self._load()
    
    def _load(self) -> Dict[str, Any]:
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                return json.loads(self.config_file.read_text(encoding='utf-8'))
            except json.JSONDecodeError as e:
                print(f"Warning: Config file corrupted, using defaults: {e}")
                return DEFAULT_CONFIG.copy()
        
        # First time - create with defaults
        config = DEFAULT_CONFIG.copy()
        # Write defaults to file
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        self.config_file.write_text(json.dumps(config, indent=2), encoding='utf-8')
        return config
    
    def save(self):
        """Save configuration to file."""
        # Ensure directory exists
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Write with nice formatting
        self.config_file.write_text(json.dumps(self.config, indent=2), encoding='utf-8')
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get any config value by dot-notation key.
        
        Args:
            key: Dot-notation key (e.g., "paths.synapse" or "agents.ATLAS.model")
            default: Default value if key not found
        
        Returns:
            Config value or default
        """
        parts = key.split('.')
        value = self.config
        
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """
        Set config value by dot-notation key.
        
        Args:
            key: Dot-notation key (e.g., "settings.log_level")
            value: Value to set
        """
        parts = key.split('.')
        target = self.config
        
        # Navigate to parent
        for part in parts[:-1]:
            if part not in target:
                target[part] = {}
            target = target[part]
        
        # Set final value
        target[parts[-1]] = value
    
    def get_path(self, path_name: str) -> Path:
        """
        Get a path from config.
        
        Args:
            path_name: Name of path (synapse, memory_bridge_db, etc.)
        
        Returns:
            Path object
        """
        path_str = self.get(f"paths.{path_name}")
        if path_str:
            return Path(path_str)
        raise KeyError(f"Path '{path_name}' not found in config")
    
    def set_path(self, path_name: str, path_value: str):
        """Set a path in config."""
        self.set(f"paths.{path_name}", path_value)
    
    def get_agent(self, agent_name: str) -> Optional[AgentConfig]:
        """
        Get agent configuration.
        
        Args:
            agent_name: Agent name (ATLAS, FORGE, etc.)
        
        Returns:
            AgentConfig object or None
        """
        agent_data = self.get(f"agents.{agent_name}")
        if agent_data:
            return AgentConfig(
                model=agent_data.get('model', 'unknown'),
                role=agent_data.get('role', 'unknown'),
                capabilities=agent_data.get('capabilities', [])
            )
        return None
    
    def get_setting(self, setting_name: str, default: Any = None) -> Any:
        """Get a setting value."""
        return self.get(f"settings.{setting_name}", default)
    
    def set_setting(self, setting_name: str, value: Any):
        """Set a setting value."""
        self.set(f"settings.{setting_name}", value)
    
    def list_agents(self) -> List[str]:
        """Get list of configured agents."""
        agents = self.get("agents", {})
        return list(agents.keys())
    
    def list_paths(self) -> Dict[str, str]:
        """Get all configured paths."""
        return self.get("paths", {})
    
    def list_settings(self) -> Dict[str, Any]:
        """Get all settings."""
        return self.get("settings", {})
    
    def validate(self) -> List[str]:
        """
        Validate configuration.
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Check required sections
        for section in ['paths', 'agents', 'settings']:
            if section not in self.config:
                errors.append(f"Missing required section: {section}")
        
        # Validate agents have required fields
        for agent_name in self.list_agents():
            agent = self.get_agent(agent_name)
            if not agent:
                errors.append(f"Invalid agent config: {agent_name}")
            elif not agent.model:
                errors.append(f"Agent {agent_name} missing model")
            elif not agent.role:
                errors.append(f"Agent {agent_name} missing role")
        
        return errors
    
    def reset_to_defaults(self):
        """Reset configuration to defaults."""
        self.config = DEFAULT_CONFIG.copy()
        self.save()


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="ConfigManager - Centralized configuration for Team Brain",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('command', choices=['show', 'get', 'set', 'list', 'validate', 'reset'],
                        help='Command to execute')
    parser.add_argument('--key', help='Config key (dot notation)')
    parser.add_argument('--value', help='Value to set')
    parser.add_argument('--section', choices=['paths', 'agents', 'settings'],
                        help='Section to list')
    parser.add_argument('--version', action='version', version=f'ConfigManager {VERSION}')
    
    args = parser.parse_args()
    
    config = ConfigManager()
    
    if args.command == 'show':
        print("\n" + "="*60)
        print("TEAM BRAIN CONFIGURATION")
        print("="*60)
        print(f"Config file: {config.config_file}")
        print(f"Version: {config.get('version')}")
        print("\nPaths:")
        for name, path in config.list_paths().items():
            print(f"  {name}: {path}")
        print("\nAgents:")
        for agent_name in config.list_agents():
            agent = config.get_agent(agent_name)
            print(f"  {agent_name}: {agent.model} ({agent.role})")
        print("\nSettings:")
        for name, value in config.list_settings().items():
            print(f"  {name}: {value}")
        print("="*60 + "\n")
    
    elif args.command == 'get':
        if not args.key:
            print("ERROR: --key required")
            return 1
        
        value = config.get(args.key)
        if value is not None:
            print(json.dumps(value, indent=2))
        else:
            print(f"Key not found: {args.key}")
            return 1
    
    elif args.command == 'set':
        if not args.key or not args.value:
            print("ERROR: --key and --value required")
            return 1
        
        # Try to parse value as JSON
        try:
            value = json.loads(args.value)
        except:
            value = args.value
        
        config.set(args.key, value)
        config.save()
        print(f"[OK] Set {args.key} = {value}")
    
    elif args.command == 'list':
        if not args.section:
            print("ERROR: --section required (paths, agents, or settings)")
            return 1
        
        if args.section == 'paths':
            print("\n=== PATHS ===")
            for name, path in config.list_paths().items():
                print(f"  {name}: {path}")
        elif args.section == 'agents':
            print("\n=== AGENTS ===")
            for agent_name in config.list_agents():
                agent = config.get_agent(agent_name)
                print(f"  {agent_name}:")
                print(f"    Model: {agent.model}")
                print(f"    Role: {agent.role}")
                print(f"    Capabilities: {', '.join(agent.capabilities)}")
        elif args.section == 'settings':
            print("\n=== SETTINGS ===")
            for name, value in config.list_settings().items():
                print(f"  {name}: {value}")
        print()
    
    elif args.command == 'validate':
        errors = config.validate()
        if errors:
            print("\n[VALIDATION FAILED]")
            for error in errors:
                print(f"  - {error}")
            print()
            return 1
        else:
            print("\n[OK] Configuration valid!\n")
    
    elif args.command == 'reset':
        confirm = input("Reset to defaults? This will overwrite current config! (yes/no): ")
        if confirm.lower() == 'yes':
            config.reset_to_defaults()
            print("[OK] Configuration reset to defaults")
        else:
            print("Cancelled")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
