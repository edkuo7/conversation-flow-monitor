#!/usr/bin/env python3
"""
Shell Command Monitoring Example
Demonstrates safe execution of shell commands with timeout protection and error recovery.

This example shows how to:
1. Execute shell commands safely with automatic timeout enforcement
2. Handle command failures gracefully with structured error information  
3. Implement retry logic for transient failures
4. Log command execution details for debugging and analysis
5. Integrate with self-improving-agent for continuous learning

Use Case: Running system commands that might hang, fail, or take too long.
"""

import os
import sys
import json
from pathlib import Path

# Add the skill's scripts directory to Python path
skill_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(skill_dir))

from conversation_monitor import ConversationMonitor, create_safe_tool_wrapper
from error_handler import ConversationErrorHandler, safe_tool_call

def demonstrate_shell_command_monitoring():
    """Demonstrate comprehensive shell command monitoring."""
    
    print("🚀 Shell Command Monitoring Example")
    print("=" * 50)
    
    # Initialize monitoring components
    monitor = ConversationMonitor()
    error_handler = ConversationErrorHandler(max_retries=2, default_timeout=20)
    
    # Create a safe wrapper for shell command execution
    @safe_tool_call(timeout=15, max_retries=2)
    async def safe_execute_shell(command: str, cwd: str = None):
        """Safely execute a shell command with monitoring."""
        import subprocess
        
        # Start monitoring this operation
        monitor.start_operation(f"shell:{command[:30]}...", timeout=15)
        
        try:
            # Execute the command
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                cwd=cwd,
                timeout=15  # Enforce timeout at subprocess level too
            )
            
            # Log successful execution
            monitor.end_operation(success=True)
            
            return {
                'success': True,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'command': command
            }
            
        except subprocess.TimeoutExpired as e:
            monitor.end_operation(success=False)
            raise TimeoutError(f"Command timed out after 15 seconds: {command}")
            
        except Exception as e:
            monitor.end_operation(success=False)
            raise e
    
    # Example 1: Safe command that should succeed
    print("\n✅ Example 1: Safe directory listing")
    try:
        import asyncio
        result = asyncio.run(safe_execute_shell("dir", cwd=os.getcwd()))
        if result.get('success'):
            print(f"   Command completed successfully (exit code: {result['returncode']})")
            print(f"   Output lines: {len(result['stdout'].splitlines())}")
        else:
            print(f"   Command failed: {result}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Example 2: Command that might hang (simulated with sleep)
    print("\n⏳ Example 2: Long-running command with timeout protection")
    try:
        import asyncio
        # This command would normally take 30 seconds, but we have 15s timeout
        result = asyncio.run(safe_execute_shell("timeout /t 30 /nobreak >nul", cwd=os.getcwd()))
        if result.get('success'):
            print("   Command completed within timeout")
        else:
            print("   Command was terminated due to timeout")
    except TimeoutError as e:
        print(f"   ⏱️  Command properly timed out: {e}")
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
    
    # Example 3: Command that fails (non-existent command)
    print("\n❌ Example 3: Non-existent command error handling")
    try:
        import asyncio
        result = asyncio.run(safe_execute_shell("nonexistent_command_12345", cwd=os.getcwd()))
        if not result.get('success'):
            print(f"   Command failed as expected (exit code: {result['returncode']})")
            print(f"   Error: {result['stderr'][:100]}...")
    except Exception as e:
        print(f"   ❌ Error handled gracefully: {e}")
    
    # Example 4: Integration with self-improving-agent logging
    print("\n📝 Example 4: Integration with self-improving-agent")
    try:
        # Simulate logging an error pattern for future learning
        error_pattern = {
            'timestamp': '2026-03-12T11:30:00Z',
            'error_type': 'shell_command_timeout',
            'context': 'system_information_gathering',
            'command': 'systeminfo',
            'resolution': 'Use shorter timeout or alternative lightweight command'
        }
        
        # In real usage, this would be logged to .learnings/ERRORS.md
        learning_entry = f"""
## [ERR-20260312-001] shell_command_timeout
**Logged**: 2026-03-12T11:30:00Z
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
System information gathering command timed out on Windows systems

### Error
Command 'systeminfo' exceeded 15-second timeout threshold

### Context
- Command attempted: systeminfo
- Environment: Windows with limited system resources
- Input parameters: none

### Suggested Fix
Use alternative lightweight commands like 'ver' or 'wmic os get caption'

### Metadata
- Reproducible: yes
- Related Files: examples/shell_command_example.py
- See Also: ERR-20260310-005
---
"""
        print("   ✅ Learning entry structure ready for self-improving-agent")
        print("   📁 Would be logged to: .learnings/ERRORS.md")
        
    except Exception as e:
        print(f"   ⚠️  Learning integration note: {e}")
    
    # Final health check
    print("\n" + "=" * 50)
    health = monitor.get_conversation_health()
    print(f"📊 Final Conversation Health: {'✅ HEALTHY' if health['is_healthy'] else '⚠️  NEEDS ATTENTION'}")
    print(f"   Recovery attempts used: {health['recovery_attempts']}/{health['max_recovery_attempts']}")
    
    if health['current_operation']:
        print(f"   Current operation: {health['current_operation']} ({health['operation_elapsed']:.1f}s elapsed)")
    
    print("\n🎯 Shell Command Monitoring Example Complete!")
    print("💡 Key Takeaways:")
    print("   • All shell commands now have automatic timeout protection")
    print("   • Errors are handled gracefully with structured information")  
    print("   • Recovery strategies prevent conversation flow interruption")
    print("   • Integration with learning systems enables continuous improvement")

if __name__ == "__main__":
    demonstrate_shell_command_monitoring()