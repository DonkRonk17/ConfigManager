# ConfigManager v1.0

**Centralized Configuration for Team Brain**

One config file to rule them all! Manage paths, agent settings, and tool configurations in one centralized location.

## Features
- Centralized config (`D:/BEACON_HQ/TEAM_BRAIN_CONFIG.json`)
- Path management (Synapse, databases, core directories)
- Agent profiles (model, role, capabilities)
- Settings management
- Dot-notation access (`config.get("agents.ATLAS.model")`)
- Validation
- CLI + Python API

## Quick Start
```python
from configmanager import ConfigManager

config = ConfigManager()

# Get paths
synapse = config.get_path("synapse")

# Get agent config
atlas = config.get_agent("ATLAS")
print(f"{atlas.model} - {atlas.role}")

# Get/set settings
poll = config.get_setting("default_poll_interval")
config.set_setting("custom", "value")
config.save()
```

## CLI Usage
```bash
# Show all config
python configmanager.py show

# Get value
python configmanager.py get --key "paths.synapse"

# Set value
python configmanager.py set --key "settings.log_level" --value "DEBUG"

# List section
python configmanager.py list --section agents

# Validate
python configmanager.py validate

# Reset to defaults
python configmanager.py reset
```

## Credits
**Built by:** Atlas (Team Brain)  
**Requested by:** Forge  
**Date:** January 18, 2026  
**Tests:** 29/29 passed

**ConfigManager** - One config, zero confusion! ⚙️
