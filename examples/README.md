# Conversation Flow Monitor - Usage Examples

This directory contains comprehensive examples demonstrating how to use the conversation-flow-monitor skill in real-world scenarios.

## Example Overview

| Example | Scenario | Key Features Demonstrated |
|---------|----------|---------------------------|
| [`browser_timeout_example.py`](browser_timeout_example.py) | Web scraping with timeout protection | Browser operation monitoring, timeout handling, recovery strategies |
| [`file_operation_example.py`](file_operation_example.py) | File system operations with error handling | Path validation, file existence checks, graceful error recovery |
| [`shell_command_example.py`](shell_command_example.py) | System command execution with monitoring | Command timeout enforcement, output validation, error pattern recognition |
| [`self_improving_integration.py`](self_improving_integration.py) | Integration with self-improving-agent | Error logging to learnings, pattern promotion, continuous improvement |
| [`comprehensive_workflow.py`](comprehensive_workflow.py) | Multi-step complex workflow | Sequential operation monitoring, cascading failure prevention, health checks |
| [`heartbeat_integration.py`](heartbeat_integration.py) | Periodic health monitoring | Automated conversation health checks, stuck conversation detection, maintenance |

## Getting Started

### Basic Usage Pattern

```python
from conversation_monitor import ConversationMonitor
from error_handler import ConversationErrorHandler

# Initialize monitor and error handler
monitor = ConversationMonitor()
error_handler = ConversationErrorHandler()

# Monitor any operation
monitor.start_operation("your_operation_name", timeout=30)
try:
    # Your actual operation here
    result = your_function()
    monitor.end_operation(success=True)
except Exception as e:
    error_info = monitor.handle_error(e, "context_description")
    # Handle recovery or provide user feedback
```

### Safe Tool Wrapper (Recommended)

For maximum safety, use the built-in safe tool wrapper:

```python
from conversation_monitor import create_safe_tool_wrapper

# Create safe wrapper for any tool function
safe_browser_use = create_safe_tool_wrapper(browser_use, "browser_use", default_timeout=45)

# Use safely
result = safe_browser_use(action="open", url="https://example.com")
if isinstance(result, dict) and result.get('error'):
    print(f"Operation failed: {result['error_details']['error_message']}")
    print(f"Suggested action: {result['suggested_action']}")
else:
    print("Operation succeeded!")
```

## Best Practices

### 1. Always Set Reasonable Timeouts
- Browser operations: 30-60 seconds
- File operations: 10-30 seconds  
- Shell commands: 20-45 seconds
- Network requests: 15-30 seconds

### 2. Provide Meaningful Context
Always include descriptive context for error handling:
```python
# Good
monitor.handle_error(e, "web_scraping_product_data")

# Avoid
monitor.handle_error(e, "error")
```

### 3. Implement Recovery Strategies
For critical operations, always have fallback plans:
```python
if operation_failed:
    if recovery_attempt < max_attempts:
        # Try alternative approach
        use_fallback_method()
    else:
        # Provide clear user guidance
        suggest_user_intervention()
```

### 4. Integrate with Learning Systems
When using with self-improving-agent, promote recurring patterns:
```python
# Log to .learnings/ERRORS.md
# If pattern repeats 3+ times, promote to AGENTS.md or TOOLS.md
```

## Advanced Patterns

### Health Monitoring During Long Conversations
```python
# Check conversation health periodically
health = monitor.get_conversation_health()
if not health['is_healthy']:
    initiate_recovery_protocol()
    log_conversation_issue_for_analysis()
```

### Custom Recovery Strategies
```python
# Register custom recovery for specific error patterns
error_handler.register_recovery_strategy(
    'browser_timeout', 
    lambda: "Switch to headless browser mode or reduce page complexity"
)
```

## Testing Your Implementation

Run the integration test to verify everything works:
```bash
cd scripts
python test_integration.py
```

## Troubleshooting

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| Timeout too short | Increase timeout threshold in config.json |
| False positives | Adjust sensitivity in ConversationMonitor class |
| Missing error logs | Check logs directory permissions |
| Integration failures | Verify YAML front matter in SKILL.md |

## Support

If you encounter issues not covered in these examples:
1. Check the main [README.md](../README.md)
2. Review error logs in the `logs/` directory  
3. Examine conversation health with `get_conversation_health()`
4. Consider opening an issue on the GitHub repository

---

**Remember**: The goal of conversation-flow-monitor is to **prevent conversations from getting stuck**, not just handle errors after they occur. Proactive monitoring and reasonable timeouts are key to reliable AI assistant operation.