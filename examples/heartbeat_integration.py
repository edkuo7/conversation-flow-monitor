#!/usr/bin/env python3
"""
Example: Heartbeat Integration with Conversation Flow Monitor

This example demonstrates how to integrate the conversation flow monitor
with OpenClaw's heartbeat system for proactive conversation health monitoring.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

import sys
import os
from pathlib import Path

# Add the skill directory to Python path
skill_dir = Path(__file__).parent.parent
sys.path.insert(0, str(skill_dir / "scripts"))

# Import conversation flow monitor components
from conversation_monitor import ConversationMonitor
from error_handler import ConversationErrorHandler

class HeartbeatConversationMonitor:
    """Enhanced monitor that integrates with heartbeat system."""
    
    def __init__(self, config_path=None):
        self.monitor = ConversationMonitor()
        self.error_handler = ConversationErrorHandler()
        self.config = self.load_config(config_path)
        self.log_dir = Path(self.config.get('log_dir', '~/.copaw/logs')).expanduser()
        self.log_dir.mkdir(exist_ok=True)
        
    def load_config(self, config_path):
        """Load configuration from file or use defaults."""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            # Default configuration
            return {
                'stuck_conversation_threshold_minutes': 30,
                'log_retention_days': 7,
                'max_recovery_attempts': 3,
                'default_timeout': 30,
                'log_dir': '~/.copaw/logs'
            }
    
    def run_heartbeat_check(self):
        """Run comprehensive heartbeat health check."""
        print("🔍 Running Conversation Flow Heartbeat Check...")
        
        # Check 1: Recent error patterns
        self.check_recent_errors()
        
        # Check 2: Stuck conversation detection
        self.check_stuck_conversations()
        
        # Check 3: System resource validation
        self.validate_system_resources()
        
        # Check 4: Skill integrity verification
        self.verify_skill_integrity()
        
        # Check 5: Recovery strategy validation
        self.validate_recovery_strategies()
        
        print("✅ Heartbeat check completed successfully!")
    
    def check_recent_errors(self):
        """Check for recent error patterns that indicate conversation issues."""
        error_log_path = self.log_dir / "conversation_monitor.log"
        
        if not error_log_path.exists():
            print("📝 No error log found - system appears clean")
            return
            
        # Read last 100 lines of error log
        with open(error_log_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()[-100:]
            
        # Look for timeout patterns
        timeout_count = sum(1 for line in lines if 'exceeded timeout' in line)
        error_count = sum(1 for line in lines if 'ERROR' in line)
        
        if timeout_count > 0:
            print(f"⚠️  Detected {timeout_count} timeout errors in recent logs")
            print("   Recommendation: Review operation timeouts and network connectivity")
            
        if error_count > 5:
            print(f"🚨 High error rate detected ({error_count} errors)")
            print("   Recommendation: Check system stability and skill configurations")
            
        if timeout_count == 0 and error_count == 0:
            print("✅ No recent errors detected - conversation flow appears healthy")
    
    def check_stuck_conversations(self):
        """Detect potentially stuck conversations."""
        threshold_minutes = self.config.get('stuck_conversation_threshold_minutes', 30)
        threshold_time = datetime.now() - timedelta(minutes=threshold_minutes)
        
        # In a real implementation, this would check active session states
        # For this example, we'll simulate the check
        print(f"⏳ Checking for conversations stuck longer than {threshold_minutes} minutes...")
        
        # Simulate: Check if any operations are currently running too long
        health = self.monitor.get_conversation_health()
        
        if health['current_operation'] and health['operation_elapsed'] > 60:
            print(f"⚠️  Potential stuck conversation detected!")
            print(f"   Operation: {health['current_operation']}")
            print(f"   Duration: {health['operation_elapsed']:.1f} seconds")
            print("   Recommendation: Consider intervention or timeout adjustment")
        else:
            print("✅ No stuck conversations detected")
    
    def validate_system_resources(self):
        """Validate system resources for conversation flow."""
        print("📊 Validating system resources...")
        
        # Check available disk space (simplified)
        total, used, free = self.get_disk_usage()
        free_gb = free / (1024**3)
        
        if free_gb < 1:
            print(f"⚠️  Low disk space: {free_gb:.1f} GB available")
            print("   Recommendation: Clean up temporary files")
        else:
            print(f"✅ Sufficient disk space: {free_gb:.1f} GB available")
            
        # Check memory usage would go here in a real implementation
    
    def get_disk_usage(self):
        """Get disk usage statistics."""
        import shutil
        total, used, free = shutil.disk_usage("/")
        return total, used, free
    
    def verify_skill_integrity(self):
        """Verify that all required skill files are present and valid."""
        print("🔍 Verifying skill integrity...")
        
        skill_dir = Path(__file__).parent.parent
        required_files = [
            "SKILL.md",
            "scripts/conversation_monitor.py", 
            "scripts/error_handler.py",
            "hooks/heartbeat.py",
            "config.json"
        ]
        
        missing_files = []
        for file in required_files:
            if not (skill_dir / file).exists():
                missing_files.append(file)
        
        if missing_files:
            print(f"❌ Missing required files: {missing_files}")
            print("   Recommendation: Reinstall the conversation-flow-monitor skill")
        else:
            # Verify SKILL.md has proper YAML front matter
            skill_md_path = skill_dir / "SKILL.md"
            with open(skill_md_path, 'r') as f:
                content = f.read()
                
            if content.startswith('---\nname:') and 'description:' in content:
                print("✅ SKILL.md has proper YAML front matter")
            else:
                print("⚠️  SKILL.md may be missing proper YAML front matter")
                print("   Recommendation: Ensure SKILL.md starts with YAML front matter")
    
    def validate_recovery_strategies(self):
        """Validate that recovery strategies are properly configured."""
        print("🔄 Validating recovery strategies...")
        
        # Check if error handler has recovery strategies registered
        if hasattr(self.error_handler, 'recovery_strategies'):
            strategy_count = len(self.error_handler.recovery_strategies)
            if strategy_count > 0:
                print(f"✅ {strategy_count} recovery strategies available")
            else:
                print("ℹ️  No custom recovery strategies registered")
                print("   Recommendation: Register recovery strategies for common error patterns")
        else:
            print("⚠️  Error handler may not have recovery strategy support")

def main():
    """Main function to demonstrate heartbeat integration."""
    print("🚀 Starting Conversation Flow Monitor Heartbeat Integration Demo")
    print("=" * 60)
    
    # Initialize the heartbeat monitor
    heartbeat_monitor = HeartbeatConversationMonitor()
    
    # Run the heartbeat check
    heartbeat_monitor.run_heartbeat_check()
    
    print("\n💡 Usage Tips:")
    print("- Schedule this script to run every 30 minutes via cron")
    print("- Integrate with OpenClaw's HEARTBEAT.md for automatic execution")
    print("- Customize config.json for your specific environment")
    print("- Monitor logs in ~/.copaw/logs for detailed diagnostics")
    
    print("\n🎯 This example shows how conversation-flow-monitor can be")
    print("   integrated into your regular maintenance workflow to")
    print("   proactively prevent conversation flow issues before they occur!")

if __name__ == "__main__":
    main()