# ConfigManager Integration Examples

**Copy-Paste Ready Code for Team Brain Tools**

This document provides ready-to-use integration examples showing how to connect ConfigManager with other Team Brain tools. Each example is complete and can be copied directly into your project.

---

## Table of Contents

1. [SynapseLink Integration](#1-synapselink-integration)
2. [SynapseWatcher Integration](#2-synapsewatcher-integration)
3. [MemoryBridge Integration](#3-memorybridge-integration)
4. [TaskQueuePro Integration](#4-taskqueuepro-integration)
5. [AgentHealth Integration](#5-agenthealth-integration)
6. [TokenTracker Integration](#6-tokentracker-integration)
7. [TimeSync Integration](#7-timesync-integration)
8. [SessionReplay Integration](#8-sessionreplay-integration)
9. [AgentRouter Integration](#9-agentrouter-integration)
10. [ToolRegistry Integration](#10-toolregistry-integration)
11. [Complete Application Example](#11-complete-application-example)

---

## 1. SynapseLink Integration

Send messages using configured Synapse path.

```python
"""
SynapseLink + ConfigManager Integration

Use centralized config for Synapse communication paths.
"""

from configmanager import ConfigManager
from synapselink import SynapseLink

def send_configured_message():
    """Send message using ConfigManager paths."""
    config = ConfigManager()
    
    # Get Synapse path from config
    synapse_path = config.get_path("synapse")
    
    # Initialize SynapseLink with config path
    synapse = SynapseLink(synapse_dir=synapse_path)
    
    # Send message
    synapse.send(
        to="FORGE",
        subject="Task Complete",
        message="Integration successful!",
        sender="ATLAS"
    )
    
    print(f"[OK] Message sent via {synapse_path}")

def quick_send_with_config():
    """Even simpler: use quick_send with config path."""
    from synapselink import quick_send
    
    config = ConfigManager()
    synapse_path = config.get_path("synapse")
    
    # quick_send uses the path internally
    quick_send(
        "FORGE",
        "Status Update",
        "All systems operational",
        sender="ATLAS"
    )

if __name__ == "__main__":
    send_configured_message()
```

---

## 2. SynapseWatcher Integration

Monitor Synapse with configured poll interval.

```python
"""
SynapseWatcher + ConfigManager Integration

Use config for paths and polling settings.
"""

from configmanager import ConfigManager
from synapsewatcher import SynapseWatcher

def start_configured_watcher():
    """Start watcher with ConfigManager settings."""
    config = ConfigManager()
    
    # Get path and settings from config
    synapse_path = config.get_path("synapse")
    poll_interval = config.get_setting("default_poll_interval")
    
    print(f"Starting watcher:")
    print(f"  Path: {synapse_path}")
    print(f"  Poll: {poll_interval}s")
    
    # Initialize with config values
    watcher = SynapseWatcher(
        synapse_path=synapse_path,
        poll_interval=poll_interval
    )
    
    # Define message handler
    def on_message(msg):
        print(f"[NEW] From {msg.sender}: {msg.subject}")
    
    watcher.on_message(on_message)
    watcher.start()

class ConfiguredSynapseWatcher:
    """Watcher class with built-in ConfigManager."""
    
    def __init__(self):
        self.config = ConfigManager()
        self.synapse_path = self.config.get_path("synapse")
        self.poll_interval = self.config.get_setting("default_poll_interval")
        self.watcher = None
    
    def start(self, handler):
        """Start watching with given handler."""
        from synapsewatcher import SynapseWatcher
        
        self.watcher = SynapseWatcher(
            synapse_path=self.synapse_path,
            poll_interval=self.poll_interval
        )
        self.watcher.on_message(handler)
        self.watcher.start()
    
    def stop(self):
        """Stop watching."""
        if self.watcher:
            self.watcher.stop()

if __name__ == "__main__":
    start_configured_watcher()
```

---

## 3. MemoryBridge Integration

Share memory with configured database paths.

```python
"""
MemoryBridge + ConfigManager Integration

Use centralized config for shared memory database.
"""

from configmanager import ConfigManager
from memorybridge import MemoryBridge

def create_configured_bridge():
    """Create MemoryBridge with ConfigManager."""
    config = ConfigManager()
    
    # Get agent info
    agent_name = "ATLAS"
    agent = config.get_agent(agent_name)
    
    # Get database path
    db_path = config.get_path("memory_bridge_db")
    
    print(f"Creating MemoryBridge:")
    print(f"  Agent: {agent_name} ({agent.role})")
    print(f"  DB: {db_path}")
    
    # Create bridge with config
    bridge = MemoryBridge(
        agent_name=agent_name,
        db_path=db_path
    )
    
    return bridge

def share_memory_example():
    """Share memory across agents."""
    bridge = create_configured_bridge()
    
    # Store some data
    bridge.store(
        namespace="session_context",
        key="current_task",
        value={"task": "tool_repair", "progress": 50}
    )
    
    # Retrieve data (any agent can access)
    data = bridge.get(
        namespace="session_context",
        key="current_task"
    )
    
    print(f"Shared data: {data}")

class ConfiguredMemoryBridge:
    """MemoryBridge with automatic ConfigManager setup."""
    
    def __init__(self, agent_name: str = "ATLAS"):
        config = ConfigManager()
        self.bridge = MemoryBridge(
            agent_name=agent_name,
            db_path=config.get_path("memory_bridge_db")
        )
    
    def store(self, namespace, key, value, ttl=None):
        return self.bridge.store(namespace, key, value, ttl)
    
    def get(self, namespace, key):
        return self.bridge.get(namespace, key)

if __name__ == "__main__":
    share_memory_example()
```

---

## 4. TaskQueuePro Integration

Manage tasks with configured queue settings.

```python
"""
TaskQueuePro + ConfigManager Integration

Use config for task queue paths and settings.
"""

from configmanager import ConfigManager
from taskqueuepro import TaskQueuePro

def create_configured_queue():
    """Create TaskQueuePro with ConfigManager."""
    config = ConfigManager()
    
    # Get database path
    db_path = config.get_path("task_queue_db")
    
    # Get settings
    max_retries = config.get_setting("max_retries")
    timeout = config.get_setting("timeout_seconds")
    
    print(f"Creating TaskQueuePro:")
    print(f"  DB: {db_path}")
    print(f"  Retries: {max_retries}")
    print(f"  Timeout: {timeout}s")
    
    queue = TaskQueuePro(db_path=db_path)
    return queue

def add_task_with_config():
    """Add task using agent config."""
    config = ConfigManager()
    queue = create_configured_queue()
    
    # Get free agents for assignment
    free_agents = []
    for agent_name in config.list_agents():
        agent = config.get_agent(agent_name)
        # Check if agent is free (Bolt is marked as free)
        if agent_name == "BOLT":
            free_agents.append(agent_name)
    
    # Add task assigned to free agent
    task_id = queue.add(
        title="Test Task",
        description="Testing ConfigManager integration",
        assigned_to=free_agents[0] if free_agents else "BOLT"
    )
    
    print(f"[OK] Task {task_id} created")

if __name__ == "__main__":
    add_task_with_config()
```

---

## 5. AgentHealth Integration

Monitor agent health using config profiles.

```python
"""
AgentHealth + ConfigManager Integration

Use config for agent profiles and health monitoring.
"""

from configmanager import ConfigManager
from agenthealth import AgentHealth

def monitor_configured_agents():
    """Monitor all configured agents."""
    config = ConfigManager()
    health = AgentHealth()
    
    # Get all configured agents
    agent_names = config.list_agents()
    
    print("Agent Health Status:")
    print("-" * 40)
    
    for agent_name in agent_names:
        agent = config.get_agent(agent_name)
        status = health.check(agent_name)
        
        print(f"{agent_name}:")
        print(f"  Model: {agent.model}")
        print(f"  Role: {agent.role}")
        print(f"  Status: {status}")
        print()

def register_agents_from_config():
    """Register all agents from config with health monitor."""
    config = ConfigManager()
    health = AgentHealth()
    
    for agent_name in config.list_agents():
        agent = config.get_agent(agent_name)
        health.register(
            agent_name=agent_name,
            model=agent.model,
            capabilities=agent.capabilities
        )
        print(f"[OK] Registered {agent_name}")

if __name__ == "__main__":
    monitor_configured_agents()
```

---

## 6. TokenTracker Integration

Track tokens with budget from config.

```python
"""
TokenTracker + ConfigManager Integration

Use config for budget settings and agent tracking.
"""

from configmanager import ConfigManager
from tokentracker import TokenTracker

def create_configured_tracker():
    """Create TokenTracker with config settings."""
    config = ConfigManager()
    
    # Get budget settings (if configured)
    monthly_budget = config.get_setting("monthly_budget_usd") or 60.0
    
    tracker = TokenTracker(monthly_budget=monthly_budget)
    return tracker

def track_agent_usage():
    """Track tokens by agent using config."""
    config = ConfigManager()
    tracker = create_configured_tracker()
    
    # Get agent being used
    agent_name = "ATLAS"
    agent = config.get_agent(agent_name)
    
    # Track usage
    tracker.track(
        agent=agent_name,
        model=agent.model,
        input_tokens=1000,
        output_tokens=500
    )
    
    # Get report
    usage = tracker.get_agent_usage(agent_name)
    print(f"{agent_name} ({agent.model}): {usage}")

if __name__ == "__main__":
    track_agent_usage()
```

---

## 7. TimeSync Integration

Synchronize time using configured paths.

```python
"""
TimeSync + ConfigManager Integration

Use config for timer paths and settings.
"""

from configmanager import ConfigManager
from timesync import TimeSync

def sync_with_config():
    """Synchronize time using ConfigManager."""
    config = ConfigManager()
    
    # TimeSync uses its own paths, but we can coordinate
    # Check if timer is stale
    from timesync import is_timer_stale, sync_timer
    
    if is_timer_stale():
        print("[!] Timer is stale, syncing...")
        sync_timer()
        print("[OK] Timer synced")
    else:
        print("[OK] Timer is fresh")

def session_timer_with_config():
    """Initialize session timer with config context."""
    config = ConfigManager()
    
    # Get agent info for session
    agent_name = "ATLAS"
    agent = config.get_agent(agent_name)
    
    from timesync import initialize_session_timer
    
    initialize_session_timer()
    print(f"[OK] Session started for {agent_name} ({agent.role})")

if __name__ == "__main__":
    sync_with_config()
```

---

## 8. SessionReplay Integration

Record sessions with configured paths.

```python
"""
SessionReplay + ConfigManager Integration

Use config for session log paths.
"""

from configmanager import ConfigManager
from sessionreplay import SessionReplay

def create_configured_recorder():
    """Create SessionReplay with config paths."""
    config = ConfigManager()
    
    # Get session logs path
    session_logs = config.get_path("session_logs")
    
    # Get agent info
    agent_name = "ATLAS"
    agent = config.get_agent(agent_name)
    
    print(f"Creating session recorder:")
    print(f"  Agent: {agent_name} ({agent.role})")
    print(f"  Logs: {session_logs}")
    
    recorder = SessionReplay(
        agent_name=agent_name,
        output_dir=session_logs
    )
    
    return recorder

def record_session():
    """Record a session with ConfigManager."""
    recorder = create_configured_recorder()
    
    # Start recording
    recorder.start()
    
    # ... session activities ...
    recorder.log_action("Checked Synapse", result="3 new messages")
    recorder.log_action("Updated tool", result="Tests passing")
    
    # End recording
    recorder.stop()
    print("[OK] Session recorded")

if __name__ == "__main__":
    record_session()
```

---

## 9. AgentRouter Integration

Route tasks using config capabilities.

```python
"""
AgentRouter + ConfigManager Integration

Use config for agent capabilities and routing.
"""

from configmanager import ConfigManager
from agentrouter import AgentRouter

def route_with_config():
    """Route tasks based on config capabilities."""
    config = ConfigManager()
    router = AgentRouter()
    
    # Build capability map from config
    for agent_name in config.list_agents():
        agent = config.get_agent(agent_name)
        for capability in agent.capabilities:
            router.register(agent_name, capability)
    
    # Route a task
    task_type = "tool_creation"
    best_agent = router.route(task_type)
    
    agent = config.get_agent(best_agent)
    print(f"Best agent for '{task_type}': {best_agent}")
    print(f"  Model: {agent.model}")
    print(f"  Role: {agent.role}")

def get_agent_for_capability(capability: str) -> str:
    """Find best agent for a capability."""
    config = ConfigManager()
    
    for agent_name in config.list_agents():
        agent = config.get_agent(agent_name)
        if capability in agent.capabilities:
            return agent_name
    
    return "BOLT"  # Default fallback

if __name__ == "__main__":
    route_with_config()
```

---

## 10. ToolRegistry Integration

Register tools with config settings.

```python
"""
ToolRegistry + ConfigManager Integration

Use config for tool registration and discovery.
"""

from configmanager import ConfigManager
from toolregistry import ToolRegistry

def register_with_config():
    """Register tools using ConfigManager."""
    config = ConfigManager()
    registry = ToolRegistry()
    
    # Register ConfigManager itself
    registry.register(
        name="ConfigManager",
        version="1.0.0",
        description="Centralized configuration for Team Brain",
        author="Atlas",
        capabilities=["configuration", "path_management", "agent_profiles"]
    )
    
    # Get registry path from config (if configured)
    # registry.set_db_path(config.get_path("tool_registry_db"))
    
    print("[OK] Tool registered")

def discover_tools():
    """Discover tools using registry."""
    registry = ToolRegistry()
    
    # Find configuration tools
    tools = registry.search(capability="configuration")
    print(f"Configuration tools: {tools}")

if __name__ == "__main__":
    register_with_config()
```

---

## 11. Complete Application Example

Full application using ConfigManager with multiple tools.

```python
"""
Complete Application Example

Demonstrates ConfigManager integration with multiple Team Brain tools.
"""

from configmanager import ConfigManager
from pathlib import Path
import json

class TeamBrainApp:
    """
    Complete Team Brain application using ConfigManager.
    
    Integrates: SynapseLink, MemoryBridge, TaskQueuePro, AgentHealth
    """
    
    def __init__(self):
        """Initialize with ConfigManager."""
        self.config = ConfigManager()
        self._validate_environment()
        self._initialize_tools()
    
    def _validate_environment(self):
        """Validate configuration before starting."""
        errors = self.config.validate()
        if errors:
            print("[X] Configuration errors:")
            for error in errors:
                print(f"  - {error}")
            raise RuntimeError("Fix configuration before continuing")
        print("[OK] Configuration validated")
    
    def _initialize_tools(self):
        """Initialize all integrated tools."""
        # Paths from config
        self.synapse_path = self.config.get_path("synapse")
        self.memory_db = self.config.get_path("memory_bridge_db")
        self.task_db = self.config.get_path("task_queue_db")
        self.session_logs = self.config.get_path("session_logs")
        
        # Settings from config
        self.poll_interval = self.config.get_setting("default_poll_interval")
        self.timeout = self.config.get_setting("timeout_seconds")
        self.max_retries = self.config.get_setting("max_retries")
        
        print(f"[OK] Tools initialized:")
        print(f"  Synapse: {self.synapse_path}")
        print(f"  Memory: {self.memory_db}")
        print(f"  Tasks: {self.task_db}")
    
    def get_available_agents(self) -> list:
        """Get list of available agents."""
        agents = []
        for agent_name in self.config.list_agents():
            agent = self.config.get_agent(agent_name)
            agents.append({
                "name": agent_name,
                "model": agent.model,
                "role": agent.role,
                "capabilities": agent.capabilities
            })
        return agents
    
    def route_task(self, capability: str) -> str:
        """Route task to agent with capability."""
        for agent_name in self.config.list_agents():
            agent = self.config.get_agent(agent_name)
            if capability in agent.capabilities:
                return agent_name
        return "BOLT"  # Default
    
    def run(self):
        """Main application loop."""
        print("\n" + "=" * 50)
        print("TEAM BRAIN APPLICATION")
        print("=" * 50)
        
        # Show available agents
        print("\nAvailable Agents:")
        for agent in self.get_available_agents():
            print(f"  {agent['name']}: {agent['model']} ({agent['role']})")
        
        # Route a sample task
        print("\nTask Routing Example:")
        task = "tool_creation"
        assigned = self.route_task(task)
        print(f"  '{task}' -> {assigned}")
        
        print("\n" + "=" * 50)
        print("[OK] Application ready")


def main():
    """Entry point."""
    app = TeamBrainApp()
    app.run()


if __name__ == "__main__":
    main()
```

---

## Integration Checklist

Use this checklist when integrating ConfigManager with any tool:

```
□ Import ConfigManager
□ Initialize config: config = ConfigManager()
□ Validate config: errors = config.validate()
□ Replace hardcoded paths with config.get_path()
□ Replace hardcoded settings with config.get_setting()
□ Use agent config for routing: config.get_agent()
□ Handle missing config gracefully
□ Test with custom config file
□ Update tool README with config instructions
□ Add config keys to documentation
```

---

## Common Patterns

### Pattern 1: Simple Path Lookup

```python
from configmanager import ConfigManager
config = ConfigManager()
path = config.get_path("synapse")
```

### Pattern 2: Validated Initialization

```python
from configmanager import ConfigManager

config = ConfigManager()
errors = config.validate()
if errors:
    raise RuntimeError(f"Config errors: {errors}")
```

### Pattern 3: Agent-Aware Operations

```python
from configmanager import ConfigManager

config = ConfigManager()
agent = config.get_agent("ATLAS")
if "tool_creation" in agent.capabilities:
    # Proceed with tool creation
    pass
```

### Pattern 4: Settings-Based Configuration

```python
from configmanager import ConfigManager

config = ConfigManager()
timeout = config.get_setting("timeout_seconds")
retries = config.get_setting("max_retries")
```

---

**ConfigManager** - One config, zero confusion! ⚙️
