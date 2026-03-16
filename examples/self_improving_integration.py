#!/usr/bin/env python3
"""
Example 4: Integration with self-improving-agent skill

This example demonstrates how conversation-flow-monitor works seamlessly with
the self-improving-agent skill to provide comprehensive error handling and
continuous improvement capabilities.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Add the conversation-flow-monitor scripts to path
SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from conversation_monitor import ConversationMonitor, create_safe_tool_wrapper
from error_handler import ConversationErrorHandler, error_handler

def demonstrate_self_improving_integration():
    """
    Demonstrates integration between conversation-flow-monitor and self-improving-agent.
    
    The conversation-flow-monitor handles immediate error recovery and timeout protection,
    while self-improving-agent captures the learning for long-term improvement.
    """
    print("🔄 Example 4: Integration with self-improving-agent")
    print("=" * 60)
    
    # Initialize both systems
    monitor = ConversationMonitor()
    error_handler_instance = ConversationErrorHandler()
    
    # Simulate a complex operation that might fail
    def risky_skill_operation(skill_name, operation_params):
        """Simulate a skill operation that could fail."""
        print(f"   🧠 Attempting operation: {skill_name}")
        
        # Simulate different failure scenarios based on skill name
        if skill_name == "browser_navigation":
            if operation_params.get("url") == "https://slow-website.com":
                raise TimeoutError("Page took too long to load")
            elif operation_params.get("url") == "https://broken-website.com":
                raise ConnectionError("Failed to connect to website")
                
        elif skill_name == "file_processing":
            if not os.path.exists(operation_params.get("file_path", "")):
                raise FileNotFoundError(f"File not found: {operation_params.get('file_path')}")
                
        elif skill_name == "skill_registration":
            if "missing_yaml" in operation_params.get("skill_path", ""):
                raise ValueError("SKILL.md missing required YAML front matter")
                
        # Success case
        return {"status": "success", "result": f"Completed {skill_name} operation"}
    
    # Create safe wrapper that integrates with self-improving-agent
    def safe_skill_operation_with_learning(skill_name, operation_params):
        """
        Safe skill operation that logs errors to self-improving-agent format.
        """
        monitor.start_operation(f"skill_{skill_name}", timeout=30)
        
        try:
            result = risky_skill_operation(skill_name, operation_params)
            monitor.end_operation(success=True)
            return result
            
        except Exception as e:
            # Handle error with conversation-flow-monitor
            error_info = monitor.handle_error(e, context=f"skill:{skill_name}")
            
            # Format error for self-improving-agent logging
            self_improving_entry = format_for_self_improving_agent(
                error_info, 
                skill_name, 
                operation_params
            )
            
            # Log to self-improving-agent format (simulated)
            log_to_self_improving_agent(self_improving_entry)
            
            # Return structured error response
            return {
                'error': True,
                'tool_name': skill_name,
                'error_details': error_info,
                'self_improving_log': self_improving_entry,
                'suggested_action': 'Check self-improving-agent logs for detailed analysis and recovery suggestions'
            }
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Successful browser navigation",
            "skill": "browser_navigation", 
            "params": {"url": "https://working-website.com"},
            "expected": "success"
        },
        {
            "name": "Timeout error - slow website",
            "skill": "browser_navigation",
            "params": {"url": "https://slow-website.com"},
            "expected": "timeout_error"
        },
        {
            "name": "File not found error",
            "skill": "file_processing", 
            "params": {"file_path": "/nonexistent/file.txt"},
            "expected": "file_error"
        },
        {
            "name": "Skill registration error (missing YAML)",
            "skill": "skill_registration",
            "params": {"skill_path": "my_skill_missing_yaml"},
            "expected": "yaml_error"
        }
    ]
    
    results = []
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n📝 Test {i}: {scenario['name']}")
        print("-" * 40)
        
        result = safe_skill_operation_with_learning(
            scenario['skill'], 
            scenario['params']
        )
        
        if result.get('error'):
            print(f"   ❌ Error handled gracefully!")
            print(f"   📊 Error type: {result['error_details']['error_type']}")
            print(f"   💡 Recovery attempt: {result['error_details']['recovery_attempt']}")
            print(f"   📝 Logged to self-improving-agent: YES")
        else:
            print(f"   ✅ Operation completed successfully!")
            print(f"   🎯 Result: {result.get('result', 'Success')}")
            
        results.append(result)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 INTEGRATION SUMMARY")
    print("=" * 60)
    successful_ops = len([r for r in results if not r.get('error')])
    failed_ops = len([r for r in results if r.get('error')])
    
    print(f"✅ Successful operations: {successful_ops}")
    print(f"❌ Handled errors: {failed_ops}")
    print(f"📈 All errors logged to self-improving-agent format")
    print(f"🔄 Continuous improvement enabled")
    
    return results

def format_for_self_improving_agent(error_info, skill_name, operation_params):
    """
    Format error information in self-improving-agent compatible format.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Generate unique ID
    error_type_short = error_info['error_type'][:3].upper()
    date_str = datetime.now().strftime("%Y%m%d")
    import random
    random_suffix = f"{random.randint(100, 999)}"
    entry_id = f"ERR-{date_str}-{random_suffix}"
    
    return {
        "entry_id": entry_id,
        "summary": f"Conversation flow error in {skill_name}",
        "logged": timestamp,
        "priority": "high",
        "status": "pending",
        "area": "conversation_flow",
        "error_details": {
            "error_type": error_info['error_type'],
            "error_message": error_info['error_message'],
            "context": error_info['context'],
            "operation": error_info['operation'],
            "recovery_attempt": error_info['recovery_attempt']
        },
        "operation_context": operation_params,
        "suggested_fix": "Implement proper validation and timeout handling using conversation-flow-monitor skill",
        "metadata": {
            "source": "conversation-flow-monitor",
            "related_files": ["SKILL.md", "scripts/conversation_monitor.py"],
            "tags": ["timeout", "error_handling", "conversation_flow"],
            "see_also": []
        }
    }

def log_to_self_improving_agent(entry):
    """
    Simulate logging to self-improving-agent .learnings/ERRORS.md format.
    In real usage, this would append to the actual file.
    """
    # This would normally write to ~/.copaw/.learnings/ERRORS.md
    # For this example, we just simulate the logging
    print(f"   📁 Would log to .learnings/ERRORS.md:")
    print(f"      Entry ID: {entry['entry_id']}")
    print(f"      Summary: {entry['summary']}")

if __name__ == "__main__":
    # Run the demonstration
    results = demonstrate_self_improving_integration()
    
    print("\n🚀 This integration enables:")
    print("   • Real-time error handling with timeout protection")
    print("   • Automatic logging to self-improving-agent format") 
    print("   • Continuous learning from conversation flow issues")
    print("   • Proactive prevention of future similar issues")
    print("   • Seamless workflow between monitoring and improvement")
    
    print("\n💡 Usage in your OpenClaw workspace:")
    print("   1. Install both conversation-flow-monitor and self-improving-agent")
    print("   2. Use safe_tool_call decorator for critical operations")  
    print("   3. Errors automatically appear in .learnings/ERRORS.md")
    print("   4. Promote valuable patterns to AGENTS.md/SOUL.md")