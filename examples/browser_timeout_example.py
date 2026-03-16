#!/usr/bin/env python3
"""
Example 1: Browser Operation with Timeout Protection

Demonstrates how to use conversation-flow-monitor to prevent browser operations
from hanging indefinitely due to slow page loads, network issues, or JavaScript errors.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from conversation_monitor import ConversationMonitor, create_safe_tool_wrapper
from error_handler import error_handler

# Simulate a browser tool function that might hang
def simulate_browser_operation(url, timeout_seconds=10):
    """
    Simulates a browser operation that could potentially hang.
    In real usage, this would be your actual browser_use function.
    """
    import time
    import random
    
    # Simulate different scenarios
    scenario = random.choice(['fast', 'slow', 'error'])
    
    if scenario == 'fast':
        time.sleep(2)  # Quick operation
        return {'success': True, 'url': url, 'load_time': 2}
    elif scenario == 'slow':
        time.sleep(timeout_seconds + 5)  # This will exceed timeout
        return {'success': True, 'url': url, 'load_time': timeout_seconds + 5}
    else:
        raise Exception(f"Browser crashed while loading {url}")

# Create a safe wrapper for the browser operation
safe_browser_operation = create_safe_tool_wrapper(
    simulate_browser_operation, 
    "browser_navigation", 
    default_timeout=15
)

def main():
    print("🚀 Example 1: Browser Operation with Timeout Protection")
    print("=" * 60)
    
    # Test the safe browser operation
    urls_to_test = [
        "https://example.com",
        "https://slow-website.com", 
        "https://error-prone-site.com"
    ]
    
    for i, url in enumerate(urls_to_test, 1):
        print(f"\n📋 Test {i}: Navigating to {url}")
        print("-" * 40)
        
        result = safe_browser_operation(url, timeout_seconds=10)
        
        if isinstance(result, dict) and result.get('error'):
            print(f"❌ Operation failed:")
            print(f"   Tool: {result['tool_name']}")
            print(f"   Error: {result['error_details']['error_message']}")
            print(f"   Recovery: {result['suggested_action']}")
        else:
            print(f"✅ Operation succeeded:")
            print(f"   Result: {result}")
    
    print("\n🎯 Key Benefits Demonstrated:")
    print("• Automatic timeout enforcement (15 seconds max)")
    print("• Graceful error handling instead of hanging")
    print("• Structured error information for debugging")
    print("• Recovery suggestions for next steps")

if __name__ == "__main__":
    main()