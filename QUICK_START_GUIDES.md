# ConfigManager Quick Start Guides

**Agent-Specific Guides for Rapid Adoption**

Each Team Brain agent has different needs and workflows. These quick start guides provide tailored instructions for each agent to begin using ConfigManager immediately.

---

## Table of Contents

1. [FORGE Quick Start](#forge-quick-start-orchestrator)
2. [ATLAS Quick Start](#atlas-quick-start-builder)
3. [CLIO Quick Start](#clio-quick-start-linux-specialist)
4. [NEXUS Quick Start](#nexus-quick-start-tester)
5. [BOLT Quick Start](#bolt-quick-start-executor)
6. [Logan Quick Start](#logan-quick-start-human-operator)
7. [Common Operations](#common-operations)
8. [Troubleshooting](#troubleshooting)

---

## FORGE Quick Start (Orchestrator)

### Your Role
As Orchestrator #1, you coordinate Team Brain operations. ConfigManager helps you:
- Route tasks to appropriate agents
- Manage session configurations
- Validate environment before delegating work

### 30-Second Start

```python
from configmanager import ConfigManager

config = ConfigManager()

# Check which agents are available
agents = config.list_agents()
print(f"Available agents: {agents}")

# Get agent capabilities for task routing
atlas = config.get_agent("ATLAS")
print(f"ATLAS can: {atlas.capabilities}")

# Validate environment before starting work
errors = config.validate()
if errors:
    print(f"Fix these first: {errors}")
```

### Key Operations for Forge

```python
# 1. Check agent capabilities
def can_agent_handle(agent_name: str, required_cap: str) -> bool:
    agent = config.get_agent(agent_name)
    return required_cap in agent.capabilities

# 2. Get Synapse path for coordination
synapse = config.get_path("synapse")

# 3. Get session logs for context
session_logs = config.get_path("session_logs")

# 4. Check agent model
forge_model = config.get("agents.FORGE.model")
```

### Forge Checklist

- [ ] Validate config at session start
- [ ] Use agent capabilities for routing
- [ ] Check paths before file operations
- [ ] Log config version for debugging

---

## ATLAS Quick Start (Builder)

### Your Role
As Tool Creator and QA Specialist, you build tools for Team Brain. ConfigManager helps you:
- Use consistent paths across all tools you create
- Access standard settings (timeouts, retries)
- Validate tool environments

### 30-Second Start

```python
from configmanager import ConfigManager

config = ConfigManager()

# Standard tool initialization pattern
synapse = config.get_path("synapse")
memory_core = config.get_path("memory_core")
timeout = config.get_setting("timeout_seconds")

print(f"Tool configured with {timeout}s timeout")
```

### Tool Creation Template

```python
"""
[ToolName] - [Description]

Uses ConfigManager for centralized configuration.
"""

from configmanager import ConfigManager
from pathlib import Path

class NewTool:
    """Standard Team Brain tool template."""
    
    def __init__(self, config_path: Path = None):
        """Initialize with ConfigManager."""
        self.config = ConfigManager(config_file=config_path)
        
        # Validate environment
        errors = self.config.validate()
        if errors:
            raise RuntimeError(f"Config errors: {errors}")
        
        # Load paths
        self.synapse_path = self.config.get_path("synapse")
        self.memory_core = self.config.get_path("memory_core")
        
        # Load settings
        self.timeout = self.config.get_setting("timeout_seconds")
        self.max_retries = self.config.get_setting("max_retries")
    
    def run(self):
        """Main tool logic."""
        # Use configured paths and settings
        pass
```

### Atlas Checklist

- [ ] Import ConfigManager in all new tools
- [ ] Use config paths instead of hardcoded paths
- [ ] Validate config at tool startup
- [ ] Test with custom config paths
- [ ] Document which config keys your tool uses

---

## CLIO Quick Start (Linux Specialist)

### Your Role
As Linux Specialist, you handle cross-platform operations. ConfigManager helps you:
- Convert Windows paths for WSL/Linux
- Access consistent paths across environments
- Maintain configuration for both platforms

### 30-Second Start

```python
from configmanager import ConfigManager
import sys

config = ConfigManager()

# Get path (Windows format by default)
synapse = config.get_path("synapse")

# Convert for Linux/WSL if needed
if sys.platform != "win32":
    synapse_linux = str(synapse).replace("D:/", "/mnt/d/").replace("\\", "/")
else:
    synapse_linux = str(synapse)

print(f"Synapse path: {synapse_linux}")
```

### Cross-Platform Helper

```python
def get_cross_platform_path(config: ConfigManager, path_name: str) -> str:
    """Get path in correct format for current OS."""
    import sys
    
    path = config.get_path(path_name)
    path_str = str(path)
    
    if sys.platform == "win32":
        return path_str
    else:
        # Convert Windows path to WSL format
        if path_str.startswith("D:/"):
            return path_str.replace("D:/", "/mnt/d/").replace("\\", "/")
        elif path_str.startswith("C:/"):
            return path_str.replace("C:/", "/mnt/c/").replace("\\", "/")
        return path_str

# Usage
synapse = get_cross_platform_path(config, "synapse")
```

### Clio Checklist

- [ ] Check `sys.platform` before path operations
- [ ] Convert paths for target environment
- [ ] Validate paths exist on target system
- [ ] Test scripts on both Windows and WSL

---

## NEXUS Quick Start (Tester)

### Your Role
As Testing Specialist, you validate Team Brain tools. ConfigManager helps you:
- Set up test environments consistently
- Access paths for test data
- Configure test settings

### 30-Second Start

```python
from configmanager import ConfigManager
import tempfile
from pathlib import Path

# For testing, use a temporary config file
with tempfile.TemporaryDirectory() as temp_dir:
    test_config_path = Path(temp_dir) / "test_config.json"
    config = ConfigManager(config_file=test_config_path)
    
    # Config will be created with defaults
    errors = config.validate()
    print(f"Test config validation: {len(errors)} errors")
```

### Test Environment Setup

```python
import unittest
import tempfile
from pathlib import Path
from configmanager import ConfigManager

class TestWithConfig(unittest.TestCase):
    """Base test class with ConfigManager setup."""
    
    def setUp(self):
        """Create isolated test config."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "test_config.json"
        self.config = ConfigManager(config_file=self.config_path)
    
    def tearDown(self):
        """Clean up test config."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_config_loads(self):
        """Config should load with defaults."""
        self.assertIsNotNone(self.config.get("version"))
    
    def test_config_validates(self):
        """Default config should be valid."""
        errors = self.config.validate()
        self.assertEqual(len(errors), 0)
```

### Nexus Checklist

- [ ] Use temporary config files for isolated tests
- [ ] Test with both default and custom configs
- [ ] Validate config as part of test setup
- [ ] Clean up test configs in tearDown

---

## BOLT Quick Start (Executor)

### Your Role
As Executor, you run tasks assigned by Forge. ConfigManager helps you:
- Get paths for file operations
- Access settings for execution parameters
- Check your own capabilities

### 30-Second Start

```python
from configmanager import ConfigManager

config = ConfigManager()

# Get execution settings
timeout = config.get_setting("timeout_seconds")
retries = config.get_setting("max_retries")

# Get paths for file operations
synapse = config.get_path("synapse")
task_queue = config.get_path("task_queue")

# Check your own config
bolt = config.get_agent("BOLT")
print(f"BOLT model: {bolt.model}")
print(f"BOLT capabilities: {bolt.capabilities}")
```

### Execution Context

```python
def get_execution_context() -> dict:
    """Get all settings needed for task execution."""
    config = ConfigManager()
    
    return {
        "synapse_path": config.get_path("synapse"),
        "task_queue_path": config.get_path("task_queue"),
        "timeout": config.get_setting("timeout_seconds"),
        "max_retries": config.get_setting("max_retries"),
        "log_level": config.get_setting("log_level"),
    }

# Use in task execution
context = get_execution_context()
print(f"Executing with {context['timeout']}s timeout")
```

### Bolt Checklist

- [ ] Load config at task start
- [ ] Use configured timeout values
- [ ] Respect max_retries setting
- [ ] Report path issues to Forge

---

## Logan Quick Start (Human Operator)

### Your Role
As the human operator, you manage Team Brain configuration. ConfigManager helps you:
- View and modify configuration
- Validate environment setup
- Reset configuration if needed

### 30-Second Start (CLI)

```bash
# View entire configuration
python configmanager.py show

# Get specific value
python configmanager.py get --key "paths.synapse"

# Set a value
python configmanager.py set --key "settings.log_level" --value "DEBUG"

# Validate configuration
python configmanager.py validate

# Reset to defaults
python configmanager.py reset
```

### Common Tasks

```bash
# Check if all paths exist
python configmanager.py validate

# Change log level for debugging
python configmanager.py set --key "settings.log_level" --value "DEBUG"

# View all agents
python configmanager.py list --section agents

# View all paths
python configmanager.py list --section paths

# View all settings
python configmanager.py list --section settings
```

### Logan Checklist

- [ ] Run `validate` after environment changes
- [ ] Use CLI for quick config changes
- [ ] Keep backup of working config
- [ ] Share config changes with team via Synapse

---

## Common Operations

### Getting Paths

```python
config = ConfigManager()

# Standard paths
beacon_hq = config.get_path("beacon_hq")
memory_core = config.get_path("memory_core")
synapse = config.get_path("synapse")
task_queue = config.get_path("task_queue")
session_logs = config.get_path("session_logs")

# Database paths
memory_bridge_db = config.get_path("memory_bridge_db")
task_queue_db = config.get_path("task_queue_db")
```

### Getting Agent Info

```python
# Get single agent
atlas = config.get_agent("ATLAS")
print(f"Model: {atlas.model}")
print(f"Role: {atlas.role}")
print(f"Capabilities: {atlas.capabilities}")

# List all agents
for agent_name in config.list_agents():
    agent = config.get_agent(agent_name)
    print(f"{agent_name}: {agent.model}")
```

### Getting Settings

```python
# Individual settings
poll_interval = config.get_setting("default_poll_interval")
timeout = config.get_setting("timeout_seconds")
retries = config.get_setting("max_retries")
log_level = config.get_setting("log_level")

# All settings
all_settings = config.list_settings()
```

### Modifying Configuration

```python
# Set values
config.set_setting("log_level", "DEBUG")
config.set_path("custom_path", "/my/custom/path")
config.set("agents.ATLAS.model", "opus-4.5")

# Always save after changes
config.save()
```

### Validation

```python
# Validate configuration
errors = config.validate()

if errors:
    print("Configuration errors:")
    for error in errors:
        print(f"  - {error}")
else:
    print("Configuration valid!")
```

---

## Troubleshooting

### Config File Not Found

**Symptom:** `FileNotFoundError` or config uses defaults  
**Cause:** Config file doesn't exist yet  
**Solution:** ConfigManager creates default config automatically

```python
config = ConfigManager()
# First run creates D:/BEACON_HQ/TEAM_BRAIN_CONFIG.json
```

### Path Doesn't Exist

**Symptom:** `validate()` returns path errors  
**Cause:** Directory hasn't been created  
**Solution:** Create the directory

```python
errors = config.validate()
# Output: ["Path 'synapse' does not exist: D:/BEACON_HQ/..."]

# Fix: Create the directory
synapse_path = config.get_path("synapse")
synapse_path.mkdir(parents=True, exist_ok=True)
```

### Changes Not Persisting

**Symptom:** Settings reset on next run  
**Cause:** Forgot to call `save()`  
**Solution:** Always save after changes

```python
config.set_setting("log_level", "DEBUG")
config.save()  # Don't forget this!
```

### Wrong Path Format

**Symptom:** Path operations fail  
**Cause:** Windows vs Unix path format  
**Solution:** Use Path objects, convert for target OS

```python
# Get as Path object
path = config.get_path("synapse")

# Convert to string for target OS
if sys.platform != "win32":
    path_str = str(path).replace("D:/", "/mnt/d/")
```

### Agent Not Found

**Symptom:** `get_agent()` returns None  
**Cause:** Agent name not in config  
**Solution:** Check agent names (case-sensitive)

```python
# Correct
atlas = config.get_agent("ATLAS")

# Wrong
atlas = config.get_agent("atlas")  # Case-sensitive!
atlas = config.get_agent("Atlas")  # Wrong case!
```

### Import Error

**Symptom:** `ModuleNotFoundError: No module named 'configmanager'`  
**Cause:** Script not in Python path  
**Solution:** Add to path or install

```python
import sys
sys.path.insert(0, "/path/to/ConfigManager")
from configmanager import ConfigManager
```

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│                 ConfigManager Quick Reference                │
├─────────────────────────────────────────────────────────────┤
│ INITIALIZE                                                   │
│   config = ConfigManager()                                   │
│   config = ConfigManager(config_file=Path("/custom.json"))   │
├─────────────────────────────────────────────────────────────┤
│ PATHS                                                        │
│   path = config.get_path("synapse")                         │
│   config.set_path("custom", "/path")                        │
│   all_paths = config.list_paths()                           │
├─────────────────────────────────────────────────────────────┤
│ AGENTS                                                       │
│   agent = config.get_agent("ATLAS")                         │
│   agent.model / agent.role / agent.capabilities             │
│   all_agents = config.list_agents()                         │
├─────────────────────────────────────────────────────────────┤
│ SETTINGS                                                     │
│   value = config.get_setting("timeout_seconds")             │
│   config.set_setting("timeout_seconds", 60)                 │
│   all_settings = config.list_settings()                     │
├─────────────────────────────────────────────────────────────┤
│ DOT NOTATION                                                 │
│   value = config.get("agents.ATLAS.model")                  │
│   config.set("settings.timeout", 60)                        │
├─────────────────────────────────────────────────────────────┤
│ SAVE & VALIDATE                                              │
│   config.save()                                              │
│   errors = config.validate()                                 │
│   config.reset_to_defaults()                                 │
├─────────────────────────────────────────────────────────────┤
│ CLI COMMANDS                                                 │
│   python configmanager.py show                               │
│   python configmanager.py get --key "paths.synapse"         │
│   python configmanager.py set --key "..." --value "..."     │
│   python configmanager.py validate                           │
│   python configmanager.py list --section agents              │
└─────────────────────────────────────────────────────────────┘
```

---

**ConfigManager** - One config, zero confusion! ⚙️
