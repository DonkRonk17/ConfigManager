"""
ConfigManager v1.0 - Test Suite

Comprehensive tests for centralized configuration management.
"""

import sys
import json
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from configmanager import ConfigManager, AgentConfig


class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def assert_true(self, condition, message):
        if condition:
            self.passed += 1
            print(f"  [OK] {message}")
        else:
            self.failed += 1
            self.errors.append(message)
            print(f"  [FAIL] {message}")
    
    def assert_equal(self, actual, expected, message):
        if actual == expected:
            self.passed += 1
            print(f"  [OK] {message}")
        else:
            self.failed += 1
            error = f"{message} (expected: {expected}, got: {actual})"
            self.errors.append(error)
            print(f"  [FAIL] {error}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"TEST RESULTS: {self.passed}/{total} passed")
        if self.failed > 0:
            print(f"\nFailed tests:")
            for error in self.errors:
                print(f"  - {error}")
        print(f"{'='*60}\n")
        return self.failed == 0


def test_load_defaults():
    """Test loading default configuration."""
    print("\n[TEST] Load Defaults")
    results = TestResults()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        config_file = Path(temp_dir) / "config.json"
        config = ConfigManager(config_file=config_file)
        
        results.assert_true(config_file.exists(), "Config file created")
        results.assert_equal(config.get('version'), '1.0.0', "Version loaded")
        results.assert_true('paths' in config.config, "Paths section exists")
        results.assert_true('agents' in config.config, "Agents section exists")
        results.assert_true('settings' in config.config, "Settings section exists")
    
    return results.summary()


def test_get_set():
    """Test get/set operations."""
    print("\n[TEST] Get and Set")
    results = TestResults()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        config_file = Path(temp_dir) / "config.json"
        config = ConfigManager(config_file=config_file)
        
        # Get existing value
        synapse_path = config.get('paths.synapse')
        results.assert_true(synapse_path is not None, "Get existing value")
        
        # Set new value
        config.set('paths.custom', '/custom/path')
        results.assert_equal(config.get('paths.custom'), '/custom/path', "Set new value")
        
        # Get with default
        missing = config.get('nonexistent.key', 'default')
        results.assert_equal(missing, 'default', "Default value works")
    
    return results.summary()


def test_paths():
    """Test path operations."""
    print("\n[TEST] Path Operations")
    results = TestResults()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        config_file = Path(temp_dir) / "config.json"
        config = ConfigManager(config_file=config_file)
        
        # Get path
        synapse = config.get_path('synapse')
        results.assert_true(isinstance(synapse, Path), "get_path returns Path object")
        
        # Set path
        config.set_path('custom', '/new/path')
        custom = config.get_path('custom')
        results.assert_true(str(custom).replace('\\', '/') == '/new/path', "set_path works")
        
        # List paths
        all_paths = config.list_paths()
        results.assert_true('synapse' in all_paths, "list_paths includes synapse")
    
    return results.summary()


def test_agents():
    """Test agent configuration."""
    print("\n[TEST] Agent Configuration")
    results = TestResults()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        config_file = Path(temp_dir) / "config.json"
        config = ConfigManager(config_file=config_file)
        
        # Get agent
        atlas = config.get_agent('ATLAS')
        results.assert_true(isinstance(atlas, AgentConfig), "get_agent returns AgentConfig")
        results.assert_equal(atlas.model, 'sonnet-4.5', "ATLAS model correct")
        results.assert_equal(atlas.role, 'builder', "ATLAS role correct")
        
        # List agents
        agents = config.list_agents()
        results.assert_true('ATLAS' in agents, "ATLAS in agent list")
        results.assert_true('FORGE' in agents, "FORGE in agent list")
        results.assert_true(len(agents) >= 4, "Multiple agents configured")
    
    return results.summary()


def test_settings():
    """Test settings operations."""
    print("\n[TEST] Settings")
    results = TestResults()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        config_file = Path(temp_dir) / "config.json"
        config = ConfigManager(config_file=config_file)
        
        # Get setting
        poll = config.get_setting('default_poll_interval')
        results.assert_equal(poll, 1.0, "Get setting value")
        
        # Set setting
        config.set_setting('custom_setting', 'value')
        results.assert_equal(config.get_setting('custom_setting'), 'value', "Set custom setting")
        
        # List settings
        all_settings = config.list_settings()
        results.assert_true('default_poll_interval' in all_settings, "Settings listed")
    
    return results.summary()


def test_save_load():
    """Test save and load persistence."""
    print("\n[TEST] Save and Load")
    results = TestResults()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        config_file = Path(temp_dir) / "config.json"
        
        # Create and modify config
        config1 = ConfigManager(config_file=config_file)
        config1.set('paths.test', '/test/path')
        config1.save()
        
        # Load in new instance
        config2 = ConfigManager(config_file=config_file)
        value = config2.get('paths.test')
        
        results.assert_equal(value, '/test/path', "Value persisted across instances")
    
    return results.summary()


def test_validation():
    """Test configuration validation."""
    print("\n[TEST] Validation")
    results = TestResults()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        config_file = Path(temp_dir) / "config.json"
        config = ConfigManager(config_file=config_file)
        
        # Validate default config (should be valid)
        errors = config.validate()
        results.assert_true(isinstance(errors, list), "Validation returns list")
        results.assert_equal(len(errors), 0, "Default config is valid")
    
    return results.summary()


def test_reset():
    """Test reset to defaults."""
    print("\n[TEST] Reset to Defaults")
    results = TestResults()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        config_file = Path(temp_dir) / "config.json"
        config = ConfigManager(config_file=config_file)
        
        # Modify config
        config.set('test_setting', 'custom_value')
        config.save()
        results.assert_equal(config.get('test_setting'), 'custom_value', "Custom setting set")
        
        # Reset
        config.reset_to_defaults()
        results.assert_true('test_setting' not in config.config, "Custom setting removed after reset")
    
    return results.summary()


def test_dot_notation():
    """Test dot notation access."""
    print("\n[TEST] Dot Notation")
    results = TestResults()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        config_file = Path(temp_dir) / "config.json"
        config = ConfigManager(config_file=config_file)
        
        # Deep get
        atlas_model = config.get('agents.ATLAS.model')
        results.assert_equal(atlas_model, 'sonnet-4.5', "Deep get works")
        
        # Deep set
        config.set('agents.ATLAS.model', 'opus-4.5')
        new_model = config.get('agents.ATLAS.model')
        results.assert_equal(new_model, 'opus-4.5', "Deep set works")
        
        # Create new deep path
        config.set('custom.nested.value', 'test')
        nested = config.get('custom.nested.value')
        results.assert_equal(nested, 'test', "Create nested path works")
    
    return results.summary()


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*60)
    print("CONFIGMANAGER v1.0 - TEST SUITE")
    print("="*60)
    
    all_passed = True
    
    all_passed &= test_load_defaults()
    all_passed &= test_get_set()
    all_passed &= test_paths()
    all_passed &= test_agents()
    all_passed &= test_settings()
    all_passed &= test_save_load()
    all_passed &= test_validation()
    all_passed &= test_reset()
    all_passed &= test_dot_notation()
    
    print("\n" + "="*60)
    if all_passed:
        print("[SUCCESS] ALL TESTS PASSED!")
    else:
        print("[FAILED] SOME TESTS FAILED")
    print("="*60 + "\n")
    
    return all_passed


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
