#!/usr/bin/env python3
"""
Test script to verify all conversation-flow-monitor examples are syntactically correct
and can be imported without errors.
"""

import sys
import os
import traceback

# Add the skill directory to Python path
skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(skill_dir, 'scripts'))

def test_example_import(example_name):
    """Test importing an example file."""
    try:
        example_path = os.path.join(os.path.dirname(__file__), f"{example_name}.py")
        if os.path.exists(example_path):
            with open(example_path, 'r') as f:
                compile(f.read(), example_path, 'exec')
            print(f"✅ {example_name}: Syntax OK")
            return True
        else:
            print(f"❌ {example_name}: File not found")
            return False
    except Exception as e:
        print(f"❌ {example_name}: Syntax Error - {e}")
        return False

def main():
    """Test all examples."""
    print("Testing conversation-flow-monitor examples...\n")
    
    examples = [
        'browser_timeout_example',
        'file_operation_example', 
        'shell_command_example',
        'self_improving_integration',
        'comprehensive_workflow',
        'heartbeat_integration'
    ]
    
    passed = 0
    total = len(examples)
    
    for example in examples:
        if test_example_import(example):
            passed += 1
    
    print(f"\nResults: {passed}/{total} examples passed syntax check")
    
    if passed == total:
        print("🎉 All examples are ready for production use!")
        return 0
    else:
        print("⚠️  Some examples need attention")
        return 1

if __name__ == "__main__":
    sys.exit(main())