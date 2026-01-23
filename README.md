# ConfigManager v1.1.0

**Centralized Configuration System for Team Brain**

One config file to rule them all! ConfigManager provides a unified, validated configuration system for all Team Brain tools and agents. No more scattered config files, hardcoded paths, or configuration chaos.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-success.svg)](requirements.txt)

---

## 🎯 **What It Does**

**Problem:** Every tool has its own config file. Paths are hardcoded. Agent settings are scattered. Changing one path requires updating 10+ files. Configuration management is a nightmare.

**Solution:** ConfigManager provides centralized, validated configuration:
- ⚙️ **Single Source of Truth** - One config file for everything
- 📁 **Path Management** - Centralized directory paths
- 🤖 **Agent Profiles** - Model, role, capabilities per agent
- 🔧 **Settings Management** - Tool-specific and global settings
- ✅ **Automatic Validation** - Ensure paths exist and values are valid
- 🔑 **Dot-Notation Access** - `config.get("agents.ATLAS.model")`
- 💾 **Reset to Defaults** - Restore clean configuration
- 🛠️ **CLI + Python API** - Use from command line or code

**Real Impact:**
```python
# BEFORE: Hardcoded paths in every tool
SYNAPSE_PATH = "D:/BEACON_HQ/MEMORY_CORE_V2/03_INTER_AI_COMMS/THE_SYNAPSE/active"
DB_PATH = "D:/BEACON_HQ/TASK_QUEUE/taskqueue.db"
# Change a path? Update 15 files manually!

# AFTER: Centralized configuration
from configmanager import ConfigManager
config = ConfigManager()

synapse = config.get_path("synapse")
db = config.get_path("task_queue_db")
# Change once, updates everywhere!
```

---

## 🚀 **Quick Start**

### Installation

```bash
# Clone or copy the script
cd /path/to/configmanager
python configmanager.py --help
```

**No dependencies required!** Pure Python standard library.

### Basic Usage

```python
from configmanager import ConfigManager

# Initialize (loads from D:/BEACON_HQ/TEAM_BRAIN_CONFIG.json)
config = ConfigManager()

# Get paths
synapse_path = config.get_path("synapse")
memory_core = config.get_path("memory_core")

# Get agent configuration
atlas = config.get_agent("ATLAS")
print(f"{atlas.name}: {atlas.model} ({atlas.role})")

# Get/set settings
poll_interval = config.get_setting("default_poll_interval")  # 300
config.set_setting("custom_setting", "value")

# Save changes
config.save()
```

---

## 📖 **Usage**

### Path Management

```python
# Get standard paths
synapse = config.get_path("synapse")
memory_core = config.get_path("memory_core")
task_queue = config.get_path("task_queue")
session_logs = config.get_path("session_logs")

# Set custom path
config.set_path("custom_dir", "/my/custom/path")
config.save()

# Validate all paths exist
valid, errors = config.validate()
if not valid:
    print(f"Errors: {errors}")
```

### Agent Configuration

```python
# Get agent profile
atlas = config.get_agent("ATLAS")
print(f"Model: {atlas.model}")           # "Claude Sonnet 4.5"
print(f"Role: {atlas.role}")             # "Builder/Orchestrator"
print(f"Free: {atlas.free}")             # True
print(f"Capabilities: {atlas.capabilities}")  # ["tool_calling", ...]

# List all agents
agents = config.list_agents()
for agent in agents:
    print(f"{agent.name}: {agent.model}")

# Update agent
config.set("agents.BOLT.model", "Grok-beta (Free)")
config.save()
```

### Settings Management

```python
# Get setting
poll_interval = config.get_setting("default_poll_interval")
log_level = config.get_setting("log_level")

# Set setting
config.set_setting("log_level", "DEBUG")
config.set_setting("max_retries", 3)

# Get all settings
all_settings = config.get("settings")
print(all_settings)
```

### Dot-Notation Access

```python
# Access nested values with dot notation
atlas_model = config.get("agents.ATLAS.model")
synapse_path = config.get("paths.synapse")

# Set nested values
config.set("agents.BOLT.capabilities", ["execution", "testing"])
config.set("settings.timeout", 30)

# Works for any depth
deep_value = config.get("section.subsection.key")
```

### Validation

```python
# Validate configuration
valid, errors = config.validate()

if valid:
    print("✅ Configuration is valid")
else:
    print("❌ Configuration errors:")
    for error in errors:
        print(f"  - {error}")

# Validate automatically checks:
# - All paths exist
# - Required fields present
# - Agent models specified
# - Settings have valid values
```

### Reset to Defaults

```python
# Reset entire configuration
config.reset_to_defaults()

# Restores:
# - Default paths
# - Default agent profiles
# - Default settings
# - Removes custom values
```

---

## 🧪 **Real-World Results**

### Test: Centralizing Tool Paths

```python
# Before ConfigManager: 7 tools with hardcoded paths

# SynapseWatcher.py
SYNAPSE_PATH = "D:/BEACON_HQ/MEMORY_CORE_V2/03_INTER_AI_COMMS/THE_SYNAPSE/active"

# TaskQueuePro.py
DB_PATH = "D:/BEACON_HQ/TASK_QUEUE/taskqueue.db"

# MemoryBridge.py
DB_PATH = "D:/BEACON_HQ/MEMORY_CORE_V2/00_SHARED_MEMORY/memory_bridge.db"

# ... 4 more tools ...

# PROBLEM: Need to change BEACON_HQ location?
# Update 7+ files manually. Miss one? Tool breaks.

# ===============================================

# After ConfigManager: One config, all tools updated

from configmanager import ConfigManager
config = ConfigManager()

# All tools use centralized paths
synapse = config.get_path("synapse")
task_db = config.get_path("task_queue_db")
memory_db = config.get_path("memory_bridge_db")

# Change BEACON_HQ location?
# Edit one line in TEAM_BRAIN_CONFIG.json
# All tools automatically use new paths!
```

**Before ConfigManager:**
- ❌ 7 files with hardcoded paths
- ❌ 15+ minutes to change one path
- ❌ Easy to miss files and break tools
- ❌ No validation

**After ConfigManager:**
- ✅ One config file
- ✅ 30 seconds to change any path
- ✅ All tools auto-updated
- ✅ Automatic validation

---

## 📦 **Dependencies**

ConfigManager uses only Python's standard library:
- `json` - Configuration serialization
- `pathlib` - Path handling
- `dataclasses` - Configuration objects
- `typing` - Type hints

**No `pip install` required!**

---

## 🎓 **How It Works**

### Configuration File Structure

**Location:** `D:/BEACON_HQ/TEAM_BRAIN_CONFIG.json`

```json
{
  "paths": {
    "beacon_hq": "D:/BEACON_HQ",
    "memory_core": "D:/BEACON_HQ/MEMORY_CORE_V2",
    "synapse": "D:/BEACON_HQ/MEMORY_CORE_V2/03_INTER_AI_COMMS/THE_SYNAPSE/active",
    "task_queue": "D:/BEACON_HQ/TASK_QUEUE",
    "session_logs": "D:/BEACON_HQ/MEMORY_CORE_V2/02_SESSION_LOGS"
  },
  "agents": {
    "ATLAS": {
      "name": "ATLAS",
      "model": "Claude Sonnet 4.5",
      "role": "Builder/Orchestrator",
      "free": true,
      "capabilities": ["tool_calling", "file_operations", "code_generation"]
    },
    "FORGE": {
      "name": "FORGE",
      "model": "Claude Opus 4.5",
      "role": "Planner/Reviewer",
      "free": true,
      "capabilities": ["planning", "review", "architecture"]
    }
  },
  "settings": {
    "default_poll_interval": 300,
    "log_level": "INFO",
    "max_retries": 3,
    "timeout": 30
  }
}
```

### Validation Rules

ConfigManager validates:
1. **Paths exist** - All directories in `paths` section must exist
2. **Agent models** - All agents must have a `model` specified
3. **Required sections** - `paths`, `agents`, `settings` must be present
4. **Path format** - Paths must be absolute and valid

### Default Configuration

If config file doesn't exist, ConfigManager creates it with defaults:
- Standard BEACON_HQ paths
- All Team Brain agents (ATLAS, FORGE, BOLT, CLIO, NEXUS)
- Sensible default settings

---

## 🎯 **Use Cases**

### For Tool Development

```python
# Every tool imports ConfigManager
from configmanager import ConfigManager

config = ConfigManager()

# Use centralized paths
synapse_path = config.get_path("synapse")
watcher = SynapseWatcher(synapse_path=synapse_path)

# No hardcoded paths!
# Tool works for everyone with same config
```

### For Agent Coordination

```python
# Check which agents are available
config = ConfigManager()
free_agents = [a for a in config.list_agents() if a.free]

print("Free agents available:")
for agent in free_agents:
    print(f"  {agent.name}: {agent.model} ({agent.role})")
```

### For Environment Setup

```python
# Validate environment before running tools
config = ConfigManager()

valid, errors = config.validate()
if not valid:
    print("⚠️ Configuration issues found:")
    for error in errors:
        print(f"  - {error}")
    print("\nPlease fix configuration before continuing.")
    exit(1)

print("✅ Environment validated - ready to run!")
```

### For Multi-Environment Support

```python
# Development config
dev_config = ConfigManager(
    config_path=Path("config/dev_config.json")
)

# Production config
prod_config = ConfigManager(
    config_path=Path("config/prod_config.json")
)

# Use appropriate config based on environment
import os
env = os.getenv("ENVIRONMENT", "dev")
config = dev_config if env == "dev" else prod_config
```

---

## 🧰 **Advanced Features**

### Custom Config Path

```python
from pathlib import Path
config = ConfigManager(config_path=Path("/custom/config.json"))
```

### Nested Access

```python
# Get deeply nested values
atlas_capabilities = config.get("agents.ATLAS.capabilities")

# Set deeply nested values
config.set("agents.BOLT.metadata.last_updated", "2026-01-18")
```

### Batch Updates

```python
# Update multiple settings at once
config.set("settings.log_level", "DEBUG")
config.set("settings.timeout", 60)
config.set("settings.max_retries", 5)
config.save()  # Save once after all updates
```

### Configuration Export

```python
# Export current config
all_config = config.get_all()
import json
with open("config_backup.json", "w") as f:
    json.dump(all_config, f, indent=2)

# Import config
with open("config_backup.json") as f:
    backup = json.load(f)
for key, value in backup.items():
    config.set(key, value)
config.save()
```

---

## 🔗 **Integration with Team Brain**

### With All Tools

```python
# Standard pattern for all Team Brain tools
from configmanager import ConfigManager

class MyTool:
    def __init__(self):
        config = ConfigManager()
        self.synapse_path = config.get_path("synapse")
        self.poll_interval = config.get_setting("default_poll_interval")
        
    def run(self):
        # Use configured paths/settings
        ...
```

### With SynapseWatcher

```python
from configmanager import ConfigManager
from synapsewatcher import SynapseWatcher

config = ConfigManager()

watcher = SynapseWatcher(
    synapse_path=config.get_path("synapse"),
    poll_interval=config.get_setting("default_poll_interval")
)
```

### With MemoryBridge

```python
from configmanager import ConfigManager
from memorybridge import MemoryBridge

config = ConfigManager()

bridge = MemoryBridge(
    agent_name="ATLAS",
    db_path=config.get_path("memory_bridge_db")
)
```

---

## 📊 **Statistics & Monitoring**

```python
# Get configuration summary
config = ConfigManager()

print(f"Paths configured: {len(config.get('paths'))}")
print(f"Agents configured: {len(config.list_agents())}")
print(f"Settings configured: {len(config.get('settings'))}")

# Validate health
valid, errors = config.validate()
print(f"Configuration valid: {valid}")
if not valid:
    print(f"Errors: {len(errors)}")
```

---

## 🐛 **Troubleshooting**

### Issue: Config file not found
**Cause:** First run or file deleted  
**Fix:** ConfigManager automatically creates default config on first run

### Issue: Path doesn't exist
**Cause:** Directory not created yet  
**Fix:** Run `config.validate()` to see which paths are missing, then create them

### Issue: Changes not persisting
**Cause:** Forgot to call `config.save()`  
**Fix:** Always call `config.save()` after making changes

### Issue: Can't access nested value
**Cause:** Incorrect dot notation syntax  
**Fix:** Use exact key path (e.g., `agents.ATLAS.model`, not `agent.atlas.model`)

### Still Having Issues?

1. Check [EXAMPLES.md](EXAMPLES.md) for working examples
2. Review [CHEAT_SHEET.txt](CHEAT_SHEET.txt) for quick reference
3. Ask in Team Brain Synapse
4. Open an issue on GitHub

---

## 📖 **Documentation**

- **[EXAMPLES.md](EXAMPLES.md)** - 10+ working examples
- **[CHEAT_SHEET.txt](CHEAT_SHEET.txt)** - Quick reference
- **[INTEGRATION_PLAN.md](INTEGRATION_PLAN.md)** - Full integration roadmap for Team Brain
- **[QUICK_START_GUIDES.md](QUICK_START_GUIDES.md)** - Agent-specific quick start guides
- **[INTEGRATION_EXAMPLES.md](INTEGRATION_EXAMPLES.md)** - Copy-paste integration code
- **[API Documentation](#usage)** - Full API reference above

---

## 🛠️ **Setup Script**

```python
from setuptools import setup

setup(
    name="configmanager",
    version="1.0.0",
    py_modules=["configmanager"],
    python_requires=">=3.8",
    author="Team Brain",
    description="Centralized configuration management for AI agents",
    license="MIT",
)
```

Install globally:
```bash
pip install .
```

---

## 🤝 **Contributing**

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📜 **License**

MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 **Credits**

**Built by:** Atlas (Team Brain)  
**Requested by:** Forge (needed centralized configuration system to eliminate hardcoded paths and scattered config files)  
**For:** Randell Logan Smith / [Metaphy LLC](https://metaphysicsandcomputing.com)  
**Part of:** Beacon HQ / Team Brain Ecosystem  
**Date:** January 18, 2026  
**Updated:** January 23, 2026 (Phase 7 Integration Docs by Atlas)  
**Methodology:** Test-Break-Optimize (29/29 tests passed)

Built with ❤️ as part of the Team Brain ecosystem - where AI agents collaborate to solve real problems.

---

## 🔗 **Links**

- **GitHub:** https://github.com/DonkRonk17/ConfigManager
- **Issues:** https://github.com/DonkRonk17/ConfigManager/issues
- **Author:** https://github.com/DonkRonk17
- **Company:** [Metaphy LLC](https://metaphysicsandcomputing.com)
- **Ecosystem:** Part of HMSS (Heavenly Morning Star System)

---

## 📝 **Quick Reference**

```python
# Initialize
config = ConfigManager()

# Get path
path = config.get_path("synapse")

# Get agent
agent = config.get_agent("ATLAS")

# Get/set setting
value = config.get_setting("key")
config.set_setting("key", "value")

# Dot notation
value = config.get("agents.ATLAS.model")
config.set("settings.timeout", 30)

# Validate
valid, errors = config.validate()

# Save changes
config.save()

# Reset to defaults
config.reset_to_defaults()
```

---

**ConfigManager** - One config, zero confusion! ⚙️
