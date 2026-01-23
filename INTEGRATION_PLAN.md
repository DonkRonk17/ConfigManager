# ConfigManager Integration Plan

**Version:** 1.1.0  
**Created:** January 18, 2026  
**Updated:** January 23, 2026 (Phase 7 Integration Docs)  
**Author:** Atlas (Team Brain)  
**Status:** Active - Ready for Team Brain Integration

---

## Executive Summary

ConfigManager provides the centralized configuration backbone for all Team Brain operations. This integration plan details how ConfigManager connects with every other tool, enabling single-source-of-truth configuration management across the entire ecosystem.

**Key Value Proposition:**
- **One config, zero confusion** - All paths, settings, and agent profiles in one place
- **Change once, update everywhere** - Modify a path in one file, all tools use the new location
- **Validation built-in** - Catch configuration errors before they cause runtime failures
- **Agent-aware** - Native support for Team Brain agent profiles and capabilities

---

## Table of Contents

1. [Integration Goals](#integration-goals)
2. [BCH Integration](#bch-integration)
3. [AI Agent Integration](#ai-agent-integration)
4. [Tool Integration Matrix](#tool-integration-matrix)
5. [Adoption Roadmap](#adoption-roadmap)
6. [Success Metrics](#success-metrics)
7. [Technical Integration Details](#technical-integration-details)
8. [Migration Guide](#migration-guide)
9. [Maintenance & Support](#maintenance--support)

---

## Integration Goals

### Primary Objectives

1. **Eliminate Hardcoded Paths**
   - Replace all hardcoded `D:/BEACON_HQ/...` paths with config lookups
   - Reduce path maintenance from 15+ files to 1
   - Enable environment-specific configurations (dev, test, prod)

2. **Centralize Agent Profiles**
   - Single source for agent capabilities and models
   - Enable dynamic agent routing based on capabilities
   - Support agent status tracking (active, inactive, maintenance)

3. **Standardize Settings**
   - Unified poll intervals, timeouts, and retry counts
   - Consistent logging levels across all tools
   - Environment-aware settings (debug in dev, info in prod)

4. **Enable Configuration Validation**
   - Validate paths exist before tool execution
   - Check agent profiles are complete
   - Ensure required settings have values

### Integration Principles

| Principle | Description |
|-----------|-------------|
| **Non-Invasive** | Tools can adopt ConfigManager incrementally |
| **Backward Compatible** | Existing tools work during transition |
| **Fail-Safe** | Graceful fallbacks if config unavailable |
| **Zero Dependencies** | ConfigManager uses only Python stdlib |

---

## BCH Integration

### Beacon Command Hub Connection

ConfigManager serves as the configuration layer for BCH (Beacon Command Hub), providing:

```
┌────────────────────────────────────────────────────────────┐
│                    BCH Desktop/Mobile                       │
├────────────────────────────────────────────────────────────┤
│                         │                                   │
│         ┌───────────────┼───────────────┐                  │
│         │               ▼               │                  │
│         │       ConfigManager           │                  │
│         │    (TEAM_BRAIN_CONFIG.json)   │                  │
│         │               │               │                  │
│         └───────────────┼───────────────┘                  │
│                         │                                   │
│    ┌────────────────────┼────────────────────┐             │
│    ▼                    ▼                    ▼             │
│ SynapseLink        TaskQueuePro         AgentRouter        │
│ MemoryBridge       SessionReplay        TokenTracker       │
│ AgentHealth        TimeSync             ToolRegistry       │
└────────────────────────────────────────────────────────────┘
```

### BCH Integration Points

#### 1. Path Configuration

```python
# BCH reads all paths from ConfigManager
from configmanager import ConfigManager

config = ConfigManager()

# BCH uses these paths for all file operations
bch_config = {
    "synapse_path": str(config.get_path("synapse")),
    "memory_core": str(config.get_path("memory_core")),
    "task_queue": str(config.get_path("task_queue")),
    "session_logs": str(config.get_path("session_logs")),
}
```

#### 2. Agent Discovery

```python
# BCH discovers available agents from config
agents = config.list_agents()

for agent_name in agents:
    agent = config.get_agent(agent_name)
    bch_register_agent(
        name=agent_name,
        model=agent.model,
        role=agent.role,
        capabilities=agent.capabilities
    )
```

#### 3. Settings Propagation

```python
# BCH applies global settings
settings = {
    "poll_interval": config.get_setting("default_poll_interval"),
    "log_level": config.get_setting("log_level"),
    "max_retries": config.get_setting("max_retries"),
    "timeout": config.get_setting("timeout_seconds"),
}
```

### BCH Mobile Considerations

For BCH Mobile (iOS/Android), ConfigManager provides:

1. **Remote Config Sync** - Config changes sync to mobile devices
2. **Reduced Paths** - Mobile uses subset of paths (synapse, session_logs)
3. **Offline Defaults** - Default config works without network

---

## AI Agent Integration

### Per-Agent Integration Patterns

#### FORGE (Orchestrator #1)

```python
# Forge uses ConfigManager for planning and orchestration
from configmanager import ConfigManager

config = ConfigManager()

# Check available agents for task assignment
def assign_task(task_type: str) -> str:
    """Assign task to best available agent."""
    agents = config.list_agents()
    
    for agent_name in agents:
        agent = config.get_agent(agent_name)
        if task_type in agent.capabilities:
            return agent_name
    
    return "BOLT"  # Default executor

# Get paths for session management
synapse = config.get_path("synapse")
session_logs = config.get_path("session_logs")
```

**Forge Integration Checklist:**
- [x] Use ConfigManager for path lookups
- [x] Check agent capabilities before assignment
- [x] Validate config at session start
- [x] Log config version for debugging

#### ATLAS (Tool Creator)

```python
# Atlas uses ConfigManager when creating/testing tools
from configmanager import ConfigManager

config = ConfigManager()

# Standard tool initialization pattern
class NewTool:
    def __init__(self):
        self.config = ConfigManager()
        self._validate_environment()
    
    def _validate_environment(self):
        """Ensure required paths exist."""
        errors = self.config.validate()
        if errors:
            raise RuntimeError(f"Config errors: {errors}")
```

**Atlas Integration Checklist:**
- [x] Use ConfigManager template for all new tools
- [x] Include ConfigManager in tool dependencies
- [x] Test with custom config paths
- [x] Document config keys used

#### CLIO (Linux Specialist)

```python
# Clio handles cross-platform path differences
from configmanager import ConfigManager

config = ConfigManager()

# Handle WSL paths
synapse = config.get_path("synapse")
if str(synapse).startswith("D:/"):
    # Convert for WSL
    wsl_path = str(synapse).replace("D:/", "/mnt/d/")
else:
    wsl_path = str(synapse)
```

**Clio Integration Checklist:**
- [x] Convert Windows paths for Linux operations
- [x] Validate paths exist on target system
- [x] Handle path format differences gracefully

#### BOLT (Executor)

```python
# Bolt executes tasks using config paths
from configmanager import ConfigManager

config = ConfigManager()

# Get execution environment
def get_execution_context():
    return {
        "synapse": config.get_path("synapse"),
        "timeout": config.get_setting("timeout_seconds"),
        "retries": config.get_setting("max_retries"),
    }
```

#### NEXUS (VS Code Agent)

```python
# Nexus uses config for testing workflows
from configmanager import ConfigManager

config = ConfigManager()

# Test environment setup
test_paths = {
    "task_queue": config.get_path("task_queue"),
    "memory_bridge": config.get_path("memory_bridge_db"),
}
```

---

## Tool Integration Matrix

### Current Integration Status

| Tool | ConfigManager | Path Lookup | Agent Config | Settings |
|------|---------------|-------------|--------------|----------|
| SynapseLink | ✅ | ✅ | ❌ | ⏳ |
| SynapseWatcher | ✅ | ✅ | ❌ | ✅ |
| MemoryBridge | ✅ | ✅ | ❌ | ⏳ |
| TaskQueuePro | ✅ | ✅ | ⏳ | ⏳ |
| AgentHealth | ⏳ | ⏳ | ✅ | ⏳ |
| SessionReplay | ⏳ | ✅ | ❌ | ⏳ |
| TokenTracker | ⏳ | ⏳ | ✅ | ✅ |
| TimeSync | ✅ | ✅ | ❌ | ✅ |
| AgentRouter | ✅ | ⏳ | ✅ | ⏳ |
| ToolRegistry | ⏳ | ✅ | ❌ | ⏳ |

**Legend:** ✅ Complete | ⏳ In Progress | ❌ Not Started

### Integration Pattern for Each Tool

#### Pattern 1: Path-Only Integration

For tools that only need centralized paths:

```python
from configmanager import ConfigManager

config = ConfigManager()
synapse_path = config.get_path("synapse")
```

#### Pattern 2: Full Integration

For tools using paths, agents, and settings:

```python
from configmanager import ConfigManager

class FullyIntegratedTool:
    def __init__(self):
        self.config = ConfigManager()
        
        # Paths
        self.synapse = self.config.get_path("synapse")
        self.memory_core = self.config.get_path("memory_core")
        
        # Agent info
        self.agent = self.config.get_agent("ATLAS")
        
        # Settings
        self.poll_interval = self.config.get_setting("default_poll_interval")
        self.timeout = self.config.get_setting("timeout_seconds")
```

---

## Adoption Roadmap

### Phase 1: Foundation (Complete)
**Timeline:** January 18-20, 2026

- [x] Create ConfigManager core functionality
- [x] Define default configuration structure
- [x] Implement validation system
- [x] Create CLI interface
- [x] Write comprehensive tests

### Phase 2: Critical Tool Integration (In Progress)
**Timeline:** January 20-25, 2026

- [x] SynapseLink integration
- [x] SynapseWatcher integration
- [x] MemoryBridge integration
- [x] TaskQueuePro integration
- [x] TimeSync integration
- [ ] TokenTracker integration
- [ ] ContextCompressor integration

### Phase 3: Full Ecosystem Integration
**Timeline:** January 25-31, 2026

- [ ] Migrate all remaining tools
- [ ] Update all tool READMEs with config instructions
- [ ] Create environment-specific configs (dev, test, prod)
- [ ] Implement config versioning

### Phase 4: BCH Integration
**Timeline:** February 1-15, 2026

- [ ] BCH Desktop config integration
- [ ] BCH Mobile config sync
- [ ] Remote config management API
- [ ] Config change notifications

---

## Success Metrics

### Quantitative Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Tools using ConfigManager | 100% | 45% |
| Hardcoded paths eliminated | 100% | 60% |
| Config validation coverage | 100% | 80% |
| Path change time | < 1 min | 30 sec |

### Qualitative Metrics

- **Developer Experience:** Easy to understand and use
- **Error Prevention:** Catch config issues before runtime
- **Consistency:** Same configuration access pattern everywhere
- **Maintainability:** Single point of configuration truth

---

## Technical Integration Details

### Configuration File Location

```
Default: D:/BEACON_HQ/TEAM_BRAIN_CONFIG.json

Structure:
BEACON_HQ/
├── TEAM_BRAIN_CONFIG.json    ← Main config file
├── MEMORY_CORE_V2/           ← Memory Core root
│   ├── 03_INTER_AI_COMMS/
│   │   └── THE_SYNAPSE/
│   │       └── active/       ← Synapse path
│   └── 02_SESSION_LOGS/      ← Session logs path
└── TASK_QUEUE/               ← Task queue path
```

### Configuration Schema

```json
{
  "version": "1.0.0",
  "paths": {
    "beacon_hq": "D:/BEACON_HQ",
    "memory_core": "D:/BEACON_HQ/MEMORY_CORE_V2",
    "synapse": "D:/BEACON_HQ/MEMORY_CORE_V2/03_INTER_AI_COMMS/THE_SYNAPSE/active",
    "task_queue": "D:/BEACON_HQ/TASK_QUEUE",
    "session_logs": "D:/BEACON_HQ/MEMORY_CORE_V2/02_SESSION_LOGS",
    "memory_bridge_db": "D:/BEACON_HQ/MEMORY_CORE_V2/00_SHARED_MEMORY/memory_bridge.db",
    "task_queue_db": "D:/BEACON_HQ/TASK_QUEUE/taskqueue.db"
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
    }
  },
  "settings": {
    "default_poll_interval": 1.0,
    "max_retries": 3,
    "timeout_seconds": 30,
    "log_level": "INFO"
  }
}
```

### API Reference Summary

| Method | Purpose | Example |
|--------|---------|---------|
| `get_path(name)` | Get path by name | `config.get_path("synapse")` |
| `set_path(name, path)` | Set custom path | `config.set_path("custom", "/path")` |
| `get_agent(name)` | Get agent config | `config.get_agent("ATLAS")` |
| `list_agents()` | List all agents | `config.list_agents()` |
| `get_setting(name)` | Get setting value | `config.get_setting("timeout")` |
| `set_setting(name, value)` | Set setting | `config.set_setting("timeout", 60)` |
| `get(key)` | Dot notation access | `config.get("agents.ATLAS.model")` |
| `set(key, value)` | Dot notation set | `config.set("settings.timeout", 60)` |
| `validate()` | Validate config | `errors = config.validate()` |
| `save()` | Persist changes | `config.save()` |
| `reset_to_defaults()` | Reset config | `config.reset_to_defaults()` |

---

## Migration Guide

### For Existing Tools

#### Step 1: Add ConfigManager Import

```python
# Before
SYNAPSE_PATH = "D:/BEACON_HQ/MEMORY_CORE_V2/03_INTER_AI_COMMS/THE_SYNAPSE/active"

# After
from configmanager import ConfigManager
config = ConfigManager()
synapse_path = config.get_path("synapse")
```

#### Step 2: Replace All Hardcoded Paths

```python
# Find and replace pattern:
# "D:/BEACON_HQ/..." → config.get_path("...")
```

#### Step 3: Add Validation

```python
def __init__(self):
    self.config = ConfigManager()
    errors = self.config.validate()
    if errors:
        print(f"Configuration errors: {errors}")
```

#### Step 4: Test Thoroughly

```bash
python -m pytest test_tool.py
python configmanager.py validate
```

### Migration Checklist

- [ ] Import ConfigManager
- [ ] Replace hardcoded paths
- [ ] Add validation step
- [ ] Update tests
- [ ] Update README
- [ ] Verify all tests pass

---

## Maintenance & Support

### Updating Configuration

1. **Edit Config File:**
   ```bash
   code D:/BEACON_HQ/TEAM_BRAIN_CONFIG.json
   ```

2. **Validate Changes:**
   ```bash
   python configmanager.py validate
   ```

3. **Restart Affected Tools:**
   - Tools reload config on next initialization
   - Some tools may need explicit restart

### Common Maintenance Tasks

| Task | Command |
|------|---------|
| View config | `python configmanager.py show` |
| Get value | `python configmanager.py get --key "paths.synapse"` |
| Set value | `python configmanager.py set --key "settings.timeout" --value 60` |
| Validate | `python configmanager.py validate` |
| Reset | `python configmanager.py reset` |

### Support Resources

- **Documentation:** README.md, EXAMPLES.md, CHEAT_SHEET.txt
- **GitHub Issues:** https://github.com/DonkRonk17/ConfigManager/issues
- **Team Synapse:** Post questions to THE_SYNAPSE

---

## Appendix: Configuration Best Practices

### Do's

- ✅ Always call `config.validate()` at startup
- ✅ Use `config.save()` after making changes
- ✅ Use dot notation for nested access
- ✅ Handle KeyError for missing paths
- ✅ Keep agent capabilities up to date

### Don'ts

- ❌ Don't hardcode paths in tool code
- ❌ Don't modify config file manually while tools are running
- ❌ Don't forget to save after setting values
- ❌ Don't assume paths exist without validation

---

**Document Version:** 1.1.0  
**Last Updated:** January 23, 2026  
**Next Review:** February 1, 2026

---

*ConfigManager - One config, zero confusion!* ⚙️
