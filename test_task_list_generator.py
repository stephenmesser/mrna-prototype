#!/usr/bin/env python3
"""
Test suite for the task list generator CLI tool.
"""

import sys
import os
import json
import tempfile
from io import StringIO
from unittest.mock import patch

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from task_list_generator import TaskListGenerator, Task


def test_task_creation():
    """Test task creation and properties."""
    print("Testing task creation...")
    
    # Test basic task creation
    task = Task("Test Task", "Test Description")
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed == False
    assert task.created_at  # Should have a timestamp
    
    # Test task with completion
    completed_task = Task("Completed Task", "", True)
    assert completed_task.completed == True
    
    print("✅ Task creation tests passed")


def test_task_list_generator_basic():
    """Test basic TaskListGenerator functionality."""
    print("Testing TaskListGenerator basic functionality...")
    
    generator = TaskListGenerator()
    
    # Test initial state
    assert len(generator.tasks) == 0
    assert generator.list_title == "Task List"
    
    # Test adding tasks
    task1 = generator.add_task("First Task", "First description")
    assert len(generator.tasks) == 1
    assert task1.title == "First Task"
    assert task1.description == "First description"
    
    task2 = generator.add_task("Second Task")
    assert len(generator.tasks) == 2
    assert task2.description == ""
    
    # Test empty title validation
    try:
        generator.add_task("")
        assert False, "Should have raised ValueError for empty title"
    except ValueError:
        pass  # Expected
    
    try:
        generator.add_task("   ")
        assert False, "Should have raised ValueError for whitespace-only title"
    except ValueError:
        pass  # Expected
    
    print("✅ TaskListGenerator basic tests passed")


def test_task_management():
    """Test task management operations."""
    print("Testing task management operations...")
    
    generator = TaskListGenerator()
    generator.add_task("Task 1")
    generator.add_task("Task 2") 
    generator.add_task("Task 3")
    
    # Test toggling completion
    assert generator.tasks[0].completed == False
    success = generator.toggle_task_completion(0)
    assert success == True
    assert generator.tasks[0].completed == True
    
    success = generator.toggle_task_completion(0)
    assert success == True
    assert generator.tasks[0].completed == False
    
    # Test invalid toggle
    success = generator.toggle_task_completion(10)
    assert success == False
    
    # Test task removal
    original_count = len(generator.tasks)
    success = generator.remove_task(1)
    assert success == True
    assert len(generator.tasks) == original_count - 1
    
    # Test invalid removal
    success = generator.remove_task(10)
    assert success == False
    
    print("✅ Task management tests passed")


def test_markdown_export():
    """Test Markdown export functionality."""
    print("Testing Markdown export...")
    
    generator = TaskListGenerator()
    generator.set_list_title("Test Project")
    
    # Test empty list export
    markdown = generator.export_to_markdown()
    assert "# Test Project" in markdown
    assert "No tasks defined" in markdown
    
    # Test with tasks
    generator.add_task("Task 1", "Description 1")
    generator.add_task("Task 2", "Description 2")
    generator.toggle_task_completion(0)  # Complete first task
    
    markdown = generator.export_to_markdown()
    assert "# Test Project" in markdown
    assert "- [x] **Task 1**" in markdown
    assert "- [ ] **Task 2**" in markdown
    assert "Description 1" in markdown
    assert "Description 2" in markdown
    
    print("✅ Markdown export tests passed")


def test_plain_text_export():
    """Test plain text export functionality."""
    print("Testing plain text export...")
    
    generator = TaskListGenerator()
    generator.set_list_title("Test Project")
    
    # Test empty list export
    text = generator.export_to_plain_text()
    assert "Test Project" in text
    assert "=" in text  # Title underline
    assert "No tasks defined" in text
    
    # Test with tasks
    generator.add_task("Task 1", "Description 1")
    generator.add_task("Task 2", "Description 2")
    generator.toggle_task_completion(0)  # Complete first task
    
    text = generator.export_to_plain_text()
    assert "Test Project" in text
    assert "[DONE] Task 1" in text
    assert "[TODO] Task 2" in text
    assert "Description 1" in text
    assert "Description 2" in text
    
    print("✅ Plain text export tests passed")


def test_json_export_import():
    """Test JSON export and import functionality."""
    print("Testing JSON export and import...")
    
    generator = TaskListGenerator()
    generator.set_list_title("JSON Test")
    generator.add_task("Task 1", "Description 1")
    generator.add_task("Task 2", "Description 2")
    generator.toggle_task_completion(0)
    
    # Test export
    json_data = generator.export_to_json()
    data = json.loads(json_data)
    
    assert data["title"] == "JSON Test"
    assert len(data["tasks"]) == 2
    assert data["tasks"][0]["title"] == "Task 1"
    assert data["tasks"][0]["completed"] == True
    assert data["tasks"][1]["completed"] == False
    
    # Test import
    new_generator = TaskListGenerator()
    new_generator.load_from_json(json_data)
    
    assert new_generator.list_title == "JSON Test"
    assert len(new_generator.tasks) == 2
    assert new_generator.tasks[0].title == "Task 1"
    assert new_generator.tasks[0].completed == True
    assert new_generator.tasks[1].completed == False
    
    # Test invalid JSON
    try:
        new_generator.load_from_json("invalid json")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass  # Expected
    
    print("✅ JSON export/import tests passed")


def test_cli_basic_functionality():
    """Test CLI basic functionality."""
    print("Testing CLI basic functionality...")
    
    # Test help message
    with patch('sys.argv', ['task_list_generator.py', '--help']):
        try:
            from task_list_generator import main
            main()
            assert False, "Should have exited with help"
        except SystemExit as e:
            assert e.code == 0  # Help should exit with code 0
    
    # Test version
    with patch('sys.argv', ['task_list_generator.py', '--version']):
        try:
            from task_list_generator import main
            main()
            assert False, "Should have exited with version"
        except SystemExit as e:
            assert e.code == 0  # Version should exit with code 0
    
    print("✅ CLI basic functionality tests passed")


def test_cli_export_functionality():
    """Test CLI export functionality."""
    print("Testing CLI export functionality...")
    
    # Redirect stdout to capture output
    original_stdout = sys.stdout
    
    try:
        # Test markdown export
        sys.stdout = StringIO()
        with patch('sys.argv', ['task_list_generator.py', '--title', 'CLI Test', '--add', 'Test Task', '--export', 'markdown']):
            from task_list_generator import main
            main()
        
        output = sys.stdout.getvalue()
        assert "# CLI Test" in output
        assert "Test Task" in output
        
        # Test text export
        sys.stdout = StringIO()
        with patch('sys.argv', ['task_list_generator.py', '--title', 'CLI Test', '--add', 'Test Task', '--export', 'text']):
            main()
        
        output = sys.stdout.getvalue()
        assert "CLI Test" in output
        assert "[TODO] Test Task" in output
        
        # Test JSON export
        sys.stdout = StringIO()
        with patch('sys.argv', ['task_list_generator.py', '--title', 'CLI Test', '--add', 'Test Task', '--export', 'json']):
            main()
        
        output = sys.stdout.getvalue()
        data = json.loads(output)
        assert data["title"] == "CLI Test"
        assert len(data["tasks"]) == 1
        
    finally:
        sys.stdout = original_stdout
    
    print("✅ CLI export functionality tests passed")


def test_cli_file_operations():
    """Test CLI file operations."""
    print("Testing CLI file operations...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Test saving to file
        output_file = os.path.join(temp_dir, "test_output.md")
        
        with patch('sys.argv', ['task_list_generator.py', '--title', 'File Test', '--add', 'Test Task', '--export', 'markdown', '--output', output_file]):
            from task_list_generator import main
            main()
        
        # Verify file was created and contains expected content
        assert os.path.exists(output_file)
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "# File Test" in content
            assert "Test Task" in content
        
        # Test loading from JSON file
        json_file = os.path.join(temp_dir, "test_tasks.json")
        
        # First create a JSON file
        with patch('sys.argv', ['task_list_generator.py', '--title', 'JSON Test', '--add', 'Task 1', '--add', 'Task 2', '--export', 'json', '--output', json_file]):
            main()
        
        # Then load and export as markdown
        output_file2 = os.path.join(temp_dir, "loaded_output.md")
        original_stdout = sys.stdout
        
        try:
            sys.stdout = StringIO()
            with patch('sys.argv', ['task_list_generator.py', '--load', json_file, '--export', 'markdown', '--output', output_file2]):
                main()
        finally:
            sys.stdout = original_stdout
        
        # Verify loaded content
        assert os.path.exists(output_file2)
        with open(output_file2, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "# JSON Test" in content
            assert "Task 1" in content
            assert "Task 2" in content
    
    print("✅ CLI file operations tests passed")


def test_task_with_descriptions():
    """Test tasks with multiline descriptions."""
    print("Testing tasks with descriptions...")
    
    generator = TaskListGenerator()
    multiline_desc = "This is a task\nwith multiple lines\nof description"
    generator.add_task("Complex Task", multiline_desc)
    
    # Test markdown export handles multiline descriptions
    markdown = generator.export_to_markdown()
    assert "Complex Task" in markdown
    assert "This is a task" in markdown
    assert "with multiple lines" in markdown
    assert "of description" in markdown
    
    # Test text export handles multiline descriptions
    text = generator.export_to_plain_text()
    assert "Complex Task" in text
    assert "This is a task" in text
    assert "with multiple lines" in text
    assert "of description" in text
    
    print("✅ Task description tests passed")


def run_all_tests():
    """Run all tests."""
    print("Starting task list generator tests...\n")
    
    tests = [
        test_task_creation,
        test_task_list_generator_basic,
        test_task_management,
        test_markdown_export,
        test_plain_text_export,
        test_json_export_import,
        test_cli_basic_functionality,
        test_cli_export_functionality,
        test_cli_file_operations,
        test_task_with_descriptions
    ]
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"❌ Test failed: {test.__name__}")
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    print("\n🎉 All task list generator tests passed!")
    return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)