# ConfigManager Examples

**10 Real-World Examples for Centralized Configuration**

---

## Example 1: Basic Configuration Access

```python
from configmanager import ConfigManager

# Initialize (loads from D:/BEACON_HQ/TEAM_BRAIN_CONFIG.json)
config = ConfigManager()

# Get synapse path
synapse_path = config.get_path("synapse")
print(f"Synapse: {synapse_path}")

# Get memory core path
memory_core = config.get_path("memory_core")
print(f"Memory Core: {memory_core}")
```

**Output:**
```
Synapse: D:\BEACON_HQ\MEMORY_CORE_V2\03_INTER_AI_COMMS\THE_SYNAPSE\active
Memory Core: D:\BEACON_HQ\MEMORY_CORE_V2
```

**Use case:** Basic configuration access in any Team Brain tool.

---

## Example 2: Agent Configuration

```python
from configmanager import ConfigManager

config = ConfigManager()

# Get ATLAS configuration
atlas = config.get_agent("ATLAS")

print(f"Agent: {atlas.name}")
print(f"Model: {atlas.model}")
print(f"Role: {atlas.role}")
print(f"Capabilities: {', '.join(atlas.capabilities)}")
```

**Output:**
```
Agent: ATLAS
Model: Claude Sonnet 4.5
Role: Builder/Orchestrator
Capabilities: tool_calling, building, review, documentation
```

**Use case:** Checking agent capabilities before routing tasks.

---

## Example 3: Dot Notation Access

```python
from configmanager import ConfigManager

config = ConfigManager()

# Access nested values with dot notation
atlas_model = config.get("agents.ATLAS.model")
poll_interval = config.get("settings.default_poll_interval")
synapse = config.get("paths.synapse")

print(f"ATLAS Model: {atlas_model}")
print(f"Poll Interval: {poll_interval}s")
print(f"Synapse: {synapse}")
```

**Output:**
```
ATLAS Model: Claude Sonnet 4.5
Poll Interval: 300s
Synapse: D:\BEACON_HQ\MEMORY_CORE_V2\03_INTER_AI_COMMS\THE_SYNAPSE\active
```

**Use case:** Quick access to specific nested configuration values.

---

## Example 4: Updating Settings

```python
from configmanager import ConfigManager

config = ConfigManager()

# Get current log level
current_level = config.get_setting("log_level")
print(f"Current log level: {current_level}")

# Update to DEBUG for troubleshooting
config.set_setting("log_level", "DEBUG")
config.set_setting("timeout", 60)

# Save changes
config.save()

print("✅ Settings updated and saved")
```

**Output:**
```
Current log level: INFO
✅ Settings updated and saved
```

**Use case:** Temporarily changing settings for debugging or testing.

---

## Example 5: Validating Configuration

```python
from configmanager import ConfigManager

config = ConfigManager()

# Validate all paths exist and configuration is valid
valid, errors = config.validate()

if valid:
    print("✅ Configuration is valid - all paths exist")
else:
    print("❌ Configuration errors found:")
    for error in errors:
        print(f"  - {error}")
    exit(1)

print("Proceeding with tool execution...")
```

**Output:**
```
✅ Configuration is valid - all paths exist
Proceeding with tool execution...
```

**Use case:** Validating environment before running tools.

---

## Example 6: Tool Integration

```python
from configmanager import ConfigManager
from synapsewatcher import SynapseWatcher

# Get configuration
config = ConfigManager()

# Use config to initialize tool
watcher = SynapseWatcher(
    synapse_path=config.get_path("synapse"),
    poll_interval=config.get_setting("default_poll_interval")
)

print(f"✅ SynapseWatcher initialized with config:")
print(f"   Path: {config.get_path('synapse')}")
print(f"   Poll: {config.get_setting('default_poll_interval')}s")
```

**Output:**
```
✅ SynapseWatcher initialized with config:
   Path: D:\BEACON_HQ\MEMORY_CORE_V2\03_INTER_AI_COMMS\THE_SYNAPSE\active
   Poll: 300s
```

**Use case:** Initializing tools with centralized configuration.

---

## Example 7: List All Agents

```python
from configmanager import ConfigManager

config = ConfigManager()

# Get all agents
agents = config.list_agents()

print("📋 Team Brain Agents:\n")
for agent in agents:
    free_indicator = "🆓" if agent.free else "💰"
    print(f"{free_indicator} {agent.name:8} | {agent.model:25} | {agent.role}")
```

**Output:**
```
📋 Team Brain Agents:

💰 ATLAS    | Claude Sonnet 4.5         | Builder/Orchestrator
💰 FORGE    | Claude Opus 4.5           | Planner/Reviewer
🆓 BOLT     | Grok-beta                 | Executor
💰 CLIO     | Claude Sonnet 4.5         | Linux Specialist
💰 NEXUS    | Claude Sonnet 4.5         | Testing Specialist
```

**Use case:** Displaying available agents and their capabilities.

---

## Example 8: Environment-Specific Configuration

```python
from configmanager import ConfigManager
from pathlib import Path
import os

# Determine environment
env = os.getenv("ENVIRONMENT", "production")

# Load environment-specific config
if env == "development":
    config_path = Path("config/dev_config.json")
elif env == "testing":
    config_path = Path("config/test_config.json")
else:
    config_path = None  # Use default

config = ConfigManager(config_path=config_path)

print(f"📍 Environment: {env}")
print(f"📄 Config: {config.config_path}")
print(f"🗂️  Synapse: {config.get_path('synapse')}")
```

**Output:**
```
📍 Environment: development
📄 Config: config\dev_config.json
🗂️  Synapse: D:\DEV\SYNAPSE_TEST
```

**Use case:** Supporting multiple environments (dev, test, production).

---

## Example 9: Reset to Defaults

```python
from configmanager import ConfigManager

config = ConfigManager()

# Made some changes but want to start fresh
print("⚠️  Resetting configuration to defaults...")

config.reset_to_defaults()

print("✅ Configuration reset")
print(f"Log level: {config.get_setting('log_level')}")  # Back to INFO
```

**Output:**
```
⚠️  Resetting configuration to defaults...
✅ Configuration reset
Log level: INFO
```

**Use case:** Recovering from configuration mistakes or testing.

---

## Example 10: Complete Tool Setup Workflow

```python
from configmanager import ConfigManager
from memorybridge import MemoryBridge
from taskqueuepro import TaskQueuePro
from synapsewatcher import SynapseWatcher

# Initialize configuration
config = ConfigManager()

# Validate configuration first
valid, errors = config.validate()
if not valid:
    print("❌ Configuration invalid:")
    for error in errors:
        print(f"  - {error}")
    exit(1)

print("✅ Configuration validated\n")

# Initialize all tools with config
print("🔧 Initializing tools...\n")

# MemoryBridge
bridge = MemoryBridge(
    agent_name="ATLAS",
    db_path=config.get_path("memory_bridge_db")
)
print(f"✅ MemoryBridge: {config.get_path('memory_bridge_db')}")

# TaskQueuePro
queue = TaskQueuePro(
    db_path=config.get_path("task_queue_db")
)
print(f"✅ TaskQueuePro: {config.get_path('task_queue_db')}")

# SynapseWatcher
watcher = SynapseWatcher(
    synapse_path=config.get_path("synapse"),
    poll_interval=config.get_setting("default_poll_interval")
)
print(f"✅ SynapseWatcher: {config.get_path('synapse')}")

print("\n🎉 All tools initialized successfully!")
```

**Output:**
```
✅ Configuration validated

🔧 Initializing tools...

✅ MemoryBridge: D:\BEACON_HQ\MEMORY_CORE_V2\00_SHARED_MEMORY\memory_bridge.db
✅ TaskQueuePro: D:\BEACON_HQ\TASK_QUEUE\taskqueue.db
✅ SynapseWatcher: D:\BEACON_HQ\MEMORY_CORE_V2\03_INTER_AI_COMMS\THE_SYNAPSE\active

🎉 All tools initialized successfully!
```

**Use case:** Complete application startup with centralized config.

---

## Command Line Examples

```bash
# Show entire configuration
python configmanager.py show

# Get specific value
python configmanager.py get --key "paths.synapse"
python configmanager.py get --key "agents.ATLAS.model"

# Set value
python configmanager.py set --key "settings.log_level" --value "DEBUG"

# List section
python configmanager.py list --section agents
python configmanager.py list --section paths

# Validate configuration
python configmanager.py validate

# Reset to defaults
python configmanager.py reset
```

---

## Integration Examples

### With All Team Brain Tools

```python
from configmanager import ConfigManager

# Standard pattern for all tools
class MyTool:
    def __init__(self):
        self.config = ConfigManager()
        
        # Get paths from config
        self.synapse_path = self.config.get_path("synapse")
        self.memory_core = self.config.get_path("memory_core")
        
        # Get settings from config
        self.poll_interval = self.config.get_setting("default_poll_interval")
        self.log_level = self.config.get_setting("log_level")
    
    def run(self):
        # Use configured paths and settings
        pass
```

### With AgentRouter

```python
from configmanager import ConfigManager
from agentrouter import AgentRouter

config = ConfigManager()
router = AgentRouter()

# Get free agents from config
all_agents = config.list_agents()
free_agents = [a.name for a in all_agents if a.free]

print(f"Free agents available: {', '.join(free_agents)}")

# Route to free agents when possible
for agent in free_agents:
    print(f"✅ {agent} available (FREE)")
```

---

**Need more examples?** Check the main [README.md](README.md) for detailed API documentation.
