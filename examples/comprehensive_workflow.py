#!/usr/bin/env python3
"""
Comprehensive Workflow Example: Conversation Flow Monitor in Action

This example demonstrates a complete multi-step workflow that combines
browser operations, file handling, shell commands, and error recovery
using the conversation-flow-monitor skill.
"""

import os
import sys
import json
from pathlib import Path

# Add the skill directory to Python path
skill_dir = Path(__file__).parent.parent
sys.path.insert(0, str(skill_dir / "scripts"))

from conversation_monitor import ConversationMonitor
from error_handler import ConversationErrorHandler, safe_tool_call

class ComprehensiveWorkflow:
    """Demonstrates a complete workflow with comprehensive monitoring."""
    
    def __init__(self):
        self.monitor = ConversationMonitor()
        self.error_handler = ConversationErrorHandler()
        self.results = []
        
    def run_complete_workflow(self):
        """Run a complete workflow demonstrating all monitoring features."""
        print("🚀 Starting Comprehensive Workflow Demo")
        print("=" * 60)
        
        # Step 1: Validate environment
        self._validate_environment()
        
        # Step 2: Browser operation with timeout
        browser_result = self._safe_browser_operation()
        if browser_result:
            self.results.append(("Browser Operation", browser_result))
            
        # Step 3: File operation with error handling
        file_result = self._safe_file_operation()
        if file_result:
            self.results.append(("File Operation", file_result))
            
        # Step 4: Shell command with monitoring
        shell_result = self._safe_shell_operation()
        if shell_result:
            self.results.append(("Shell Command", shell_result))
            
        # Step 5: Generate workflow report
        self._generate_report()
        
        print("\n✅ Comprehensive workflow completed successfully!")
        return True
        
    def _validate_environment(self):
        """Validate that required directories and files exist."""
        print("🔍 Validating environment...")
        
        required_dirs = [
            skill_dir / "logs",
            skill_dir / "error_logs",
            Path.home() / ".copaw" / "memory"
        ]
        
        for dir_path in required_dirs:
            if not dir_path.exists():
                print(f"   Creating missing directory: {dir_path}")
                dir_path.mkdir(parents=True, exist_ok=True)
            else:
                print(f"   ✓ Directory exists: {dir_path}")
                
        print("✅ Environment validation complete\n")
        
    def _safe_browser_operation(self):
        """Perform a browser operation with comprehensive monitoring."""
        print("🌐 Performing monitored browser operation...")
        
        # Simulate browser operation with potential timeout
        try:
            with self.monitor.track_operation("comprehensive_browser_demo", timeout=15):
                # Simulate actual browser work
                import time
                time.sleep(2)  # Simulate page loading
                
                # Simulate successful operation
                result = {
                    'url': 'https://example.com',
                    'status': 'success',
                    'load_time': 2.1,
                    'elements_found': 42
                }
                
                print(f"   ✓ Browser operation completed in {result['load_time']}s")
                return result
                
        except Exception as e:
            error_info = self.error_handler.handle_error(
                e, 
                context="comprehensive_browser_operation"
            )
            print(f"   ❌ Browser operation failed: {error_info}")
            return None
            
    def _safe_file_operation(self):
        """Perform file operations with error handling."""
        print("📁 Performing monitored file operations...")
        
        test_file = Path.home() / ".copaw" / "test_workflow_file.txt"
        
        try:
            with self.monitor.track_operation("comprehensive_file_demo", timeout=10):
                # Write test file
                test_file.write_text("Test content from comprehensive workflow demo")
                print(f"   ✓ Created test file: {test_file}")
                
                # Read test file
                content = test_file.read_text()
                print(f"   ✓ Read file content: {content[:50]}...")
                
                # Clean up
                test_file.unlink()
                print(f"   ✓ Cleaned up test file")
                
                result = {
                    'file_operations': ['create', 'read', 'delete'],
                    'content_length': len(content),
                    'status': 'success'
                }
                
                return result
                
        except Exception as e:
            error_info = self.error_handler.handle_error(
                e,
                context="comprehensive_file_operation"
            )
            print(f"   ❌ File operation failed: {error_info}")
            
            # Attempt recovery - ensure cleanup even on failure
            if test_file.exists():
                try:
                    test_file.unlink()
                    print("   ⚠️  Recovered: cleaned up test file after failure")
                except:
                    pass
                    
            return None
            
    def _safe_shell_operation(self):
        """Perform shell command with monitoring."""
        print("💻 Performing monitored shell command...")
        
        try:
            with self.monitor.track_operation("comprehensive_shell_demo", timeout=20):
                # Execute a safe shell command
                import subprocess
                
                if os.name == 'nt':  # Windows
                    cmd = ["dir", "/w"]
                    cwd = str(Path.home())
                else:  # Unix-like
                    cmd = ["ls", "-la"]
                    cwd = str(Path.home())
                    
                result = subprocess.run(
                    cmd, 
                    cwd=cwd,
                    capture_output=True, 
                    text=True, 
                    timeout=15
                )
                
                if result.returncode == 0:
                    output_lines = result.stdout.split('\n')[:5]  # First 5 lines
                    print(f"   ✓ Shell command executed successfully")
                    print(f"   📋 Output preview: {len(output_lines)} lines")
                    
                    shell_result = {
                        'command': ' '.join(cmd),
                        'return_code': result.returncode,
                        'output_preview': output_lines,
                        'status': 'success'
                    }
                    
                    return shell_result
                else:
                    raise subprocess.CalledProcessError(
                        result.returncode, 
                        cmd, 
                        result.stderr
                    )
                    
        except Exception as e:
            error_info = self.error_handler.handle_error(
                e,
                context="comprehensive_shell_operation"
            )
            print(f"   ❌ Shell command failed: {error_info}")
            return None
            
    def _generate_report(self):
        """Generate a comprehensive workflow report."""
        print("\n📊 Generating workflow report...")
        
        report = {
            'workflow_name': 'Conversation Flow Monitor - Comprehensive Demo',
            'timestamp': self._get_timestamp(),
            'operations_completed': len(self.results),
            'operations_attempted': 3,
            'success_rate': f"{len(self.results)/3*100:.1f}%",
            'results': self.results,
            'monitoring_stats': {
                'total_operations': 3,
                'errors_handled': 0,  # Would be incremented on actual errors
                'recovery_attempts': self.monitor.recovery_attempts,
                'max_recovery_attempts': self.monitor.max_recovery_attempts
            }
        }
        
        # Save report to workspace .logs directory
        workspace_logs_dir = Path.home() / ".copaw" / ".logs"
        workspace_logs_dir.mkdir(exist_ok=True)
        report_file = workspace_logs_dir / "comprehensive_workflow_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
            
        print(f"   📄 Report saved to: {report_file}")
        print(f"   ✅ Success rate: {report['success_rate']}")
        print(f"   🛡️  Recovery attempts: {report['monitoring_stats']['recovery_attempts']}")
        
    def _get_timestamp(self):
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.now().isoformat()

def main():
    """Main entry point for the comprehensive workflow example."""
    workflow = ComprehensiveWorkflow()
    
    try:
        workflow.run_complete_workflow()
        return 0
    except KeyboardInterrupt:
        print("\n⚠️  Workflow interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error in workflow: {e}")
        return 1

if __name__ == "__main__":
    exit(main())