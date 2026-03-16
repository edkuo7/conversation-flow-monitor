#!/usr/bin/env python3
"""
File Operation Error Handling Example

Demonstrates how the conversation-flow-monitor skill handles file operations
that might fail due to missing files, permission issues, or path problems.
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from conversation_monitor import ConversationMonitor
from error_handler import ConversationErrorHandler

def demonstrate_file_operations():
    """Demonstrate safe file operations with error handling."""
    print("📁 File Operation Error Handling Example")
    print("=" * 50)
    
    # Initialize monitoring components
    monitor = ConversationMonitor()
    error_handler = ConversationErrorHandler()
    
    # Example 1: Reading a non-existent file
    print("\n1. Attempting to read non-existent file...")
    monitor.start_operation("read_nonexistent_file", timeout=10)
    
    try:
        # This would normally cause FileNotFoundError
        with open("/path/that/does/not/exist.txt", "r") as f:
            content = f.read()
        monitor.end_operation(success=True)
        print("✅ File read successful")
    except FileNotFoundError as e:
        monitor.end_operation(success=False)
        error_info = error_handler.handle_error(e, context="file_read_nonexistent")
        print(f"❌ Expected error handled gracefully:")
        print(f"   Error type: {error_info['error_type']}")
        print(f"   Recovery attempt: {error_info['recovery_attempt']}")
        print(f"   Suggested action: Create directory and retry with valid path")
    
    # Example 2: Writing to protected directory
    print("\n2. Attempting to write to protected directory...")
    monitor.start_operation("write_protected_directory", timeout=10)
    
    try:
        # This might cause PermissionError on some systems
        with open("/system/protected/file.txt", "w") as f:
            f.write("test content")
        monitor.end_operation(success=True)
        print("✅ File write successful")
    except (PermissionError, OSError) as e:
        monitor.end_operation(success=False)
        error_info = error_handler.handle_error(e, context="file_write_protected")
        print(f"❌ Permission error handled gracefully:")
        print(f"   Error type: {error_info['error_type']}")
        print(f"   Recovery attempt: {error_info['recovery_attempt']}")
        print(f"   Suggested action: Use user-writable directory like ~/.copaw/")
    
    # Example 3: Safe file operation with validation
    print("\n3. Safe file operation with pre-validation...")
    
    # Validate path before attempting operation
    safe_path = os.path.expanduser("~/.copaw/test_safe_file.txt")
    safe_dir = os.path.dirname(safe_path)
    
    # Ensure directory exists
    os.makedirs(safe_dir, exist_ok=True)
    
    monitor.start_operation("safe_file_write", timeout=10)
    try:
        with open(safe_path, "w") as f:
            f.write("This is a safely written file!")
        monitor.end_operation(success=True)
        print(f"✅ Safe file write successful: {safe_path}")
        
        # Clean up
        os.remove(safe_path)
        print("🧹 Cleanup completed")
        
    except Exception as e:
        monitor.end_operation(success=False)
        error_info = error_handler.handle_error(e, context="safe_file_write")
        print(f"❌ Unexpected error: {error_info}")
    
    print("\n" + "=" * 50)
    print("✅ File operation examples completed!")
    print("Key takeaways:")
    print("- Always validate file paths before operations")
    print("- Handle specific exceptions (FileNotFoundError, PermissionError)")
    print("- Use safe directories (user home, working directory)")
    print("- Monitor operations with appropriate timeouts")

if __name__ == "__main__":
    demonstrate_file_operations()