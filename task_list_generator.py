#!/usr/bin/env python3
"""
Task List Generator CLI Tool

A command-line interface tool for generating structured task lists.
Supports both interactive and batch modes with export to Markdown and plain text formats.

Author: AI Assistant
Date: 2024
"""

import argparse
import json
import sys
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Task:
    """Represents a single task with title, description, and completion status."""
    title: str
    description: str = ""
    completed: bool = False
    created_at: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


class TaskListGenerator:
    """Main class for generating and managing task lists."""
    
    def __init__(self):
        self.tasks: List[Task] = []
        self.list_title: str = "Task List"
    
    def set_list_title(self, title: str):
        """Set the title for the task list."""
        self.list_title = title
    
    def add_task(self, title: str, description: str = "", completed: bool = False) -> Task:
        """Add a new task to the list."""
        if not title.strip():
            raise ValueError("Task title cannot be empty")
        
        task = Task(
            title=title.strip(),
            description=description.strip(),
            completed=completed
        )
        self.tasks.append(task)
        return task
    
    def remove_task(self, index: int) -> bool:
        """Remove a task by index."""
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            return True
        return False
    
    def toggle_task_completion(self, index: int) -> bool:
        """Toggle the completion status of a task."""
        if 0 <= index < len(self.tasks):
            self.tasks[index].completed = not self.tasks[index].completed
            return True
        return False
    
    def export_to_markdown(self) -> str:
        """Export the task list to Markdown format."""
        if not self.tasks:
            return f"# {self.list_title}\n\nNo tasks defined.\n"
        
        markdown = f"# {self.list_title}\n\n"
        markdown += f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
        
        for i, task in enumerate(self.tasks, 1):
            checkbox = "- [x]" if task.completed else "- [ ]"
            markdown += f"{checkbox} **{task.title}**\n"
            
            if task.description:
                # Indent description
                description_lines = task.description.split('\n')
                for line in description_lines:
                    if line.strip():
                        markdown += f"  {line.strip()}\n"
                markdown += "\n"
            else:
                markdown += "\n"
        
        return markdown
    
    def export_to_plain_text(self) -> str:
        """Export the task list to plain text format."""
        if not self.tasks:
            return f"{self.list_title}\n{'=' * len(self.list_title)}\n\nNo tasks defined.\n"
        
        text = f"{self.list_title}\n"
        text += "=" * len(self.list_title) + "\n\n"
        text += f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for i, task in enumerate(self.tasks, 1):
            status = "[DONE]" if task.completed else "[TODO]"
            text += f"{i:2d}. {status} {task.title}\n"
            
            if task.description:
                # Indent description
                description_lines = task.description.split('\n')
                for line in description_lines:
                    if line.strip():
                        text += f"    {line.strip()}\n"
                text += "\n"
            else:
                text += "\n"
        
        return text
    
    def export_to_json(self) -> str:
        """Export the task list to JSON format."""
        data = {
            "title": self.list_title,
            "generated_at": datetime.now().isoformat(),
            "tasks": [asdict(task) for task in self.tasks]
        }
        return json.dumps(data, indent=2)
    
    def load_from_json(self, json_data: str):
        """Load tasks from JSON data."""
        try:
            data = json.loads(json_data)
            self.list_title = data.get("title", "Task List")
            self.tasks = []
            
            for task_data in data.get("tasks", []):
                task = Task(**task_data)
                self.tasks.append(task)
        except (json.JSONDecodeError, TypeError, KeyError) as e:
            raise ValueError(f"Invalid JSON format: {e}")


def interactive_mode():
    """Run the tool in interactive mode."""
    generator = TaskListGenerator()
    
    print("Task List Generator - Interactive Mode")
    print("=" * 40)
    
    # Get list title
    title = input("Enter task list title (default: 'Task List'): ").strip()
    if title:
        generator.set_list_title(title)
    
    print(f"\nCreating task list: {generator.list_title}")
    print("Enter tasks (type 'done' when finished, 'help' for commands)\n")
    
    while True:
        try:
            command = input("Command> ").strip().lower()
            
            if command == 'done':
                break
            elif command == 'help':
                print("\nAvailable commands:")
                print("  add - Add a new task")
                print("  list - Show current tasks")
                print("  toggle <number> - Toggle task completion")
                print("  remove <number> - Remove a task")
                print("  export <format> - Export to markdown/text/json")
                print("  done - Finish and export")
                print("  help - Show this help")
                print()
                continue
            elif command == 'add':
                task_title = input("Task title: ").strip()
                if not task_title:
                    print("Task title cannot be empty!")
                    continue
                
                task_desc = input("Task description (optional): ").strip()
                generator.add_task(task_title, task_desc)
                print(f"Added task: {task_title}")
                
            elif command == 'list':
                if not generator.tasks:
                    print("No tasks added yet.")
                else:
                    print(f"\nCurrent tasks in '{generator.list_title}':")
                    for i, task in enumerate(generator.tasks, 1):
                        status = "✓" if task.completed else "○"
                        print(f"  {i}. {status} {task.title}")
                        if task.description:
                            print(f"     {task.description}")
                print()
                
            elif command.startswith('toggle '):
                try:
                    index = int(command.split()[1]) - 1
                    if generator.toggle_task_completion(index):
                        task = generator.tasks[index]
                        status = "completed" if task.completed else "pending"
                        print(f"Task '{task.title}' marked as {status}")
                    else:
                        print("Invalid task number!")
                except (ValueError, IndexError):
                    print("Usage: toggle <task_number>")
                    
            elif command.startswith('remove '):
                try:
                    index = int(command.split()[1]) - 1
                    if 0 <= index < len(generator.tasks):
                        removed_task = generator.tasks[index]
                        generator.remove_task(index)
                        print(f"Removed task: {removed_task.title}")
                    else:
                        print("Invalid task number!")
                except (ValueError, IndexError):
                    print("Usage: remove <task_number>")
                    
            elif command.startswith('export '):
                try:
                    format_type = command.split()[1].lower()
                    if format_type == 'markdown':
                        print("\n" + generator.export_to_markdown())
                    elif format_type == 'text':
                        print("\n" + generator.export_to_plain_text())
                    elif format_type == 'json':
                        print("\n" + generator.export_to_json())
                    else:
                        print("Supported formats: markdown, text, json")
                except IndexError:
                    print("Usage: export <markdown|text|json>")
            else:
                if command:  # Don't show error for empty commands
                    print(f"Unknown command: {command}. Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")
    
    # Final export options
    if generator.tasks:
        print(f"\nCompleted task list with {len(generator.tasks)} tasks.")
        format_choice = input("Export format (markdown/text/json): ").strip().lower()
        
        if format_choice == 'markdown':
            output = generator.export_to_markdown()
        elif format_choice == 'text':
            output = generator.export_to_plain_text()
        elif format_choice == 'json':
            output = generator.export_to_json()
        else:
            output = generator.export_to_markdown()  # Default to markdown
            
        filename = input("Save to file (enter filename or press Enter to print): ").strip()
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(output)
                print(f"Task list saved to: {filename}")
            except IOError as e:
                print(f"Error saving file: {e}")
                print("\nOutput:")
                print(output)
        else:
            print("\nOutput:")
            print(output)
    else:
        print("No tasks were added.")


def main():
    """Main function for the CLI tool."""
    parser = argparse.ArgumentParser(
        description="Generate structured task lists with export options",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --interactive                    # Interactive mode
  %(prog)s --title "Project Tasks" --add "Setup environment" --add "Write tests" --export markdown
  %(prog)s --load tasks.json --export text --output tasks.txt
  %(prog)s --title "Daily Tasks" --add "Review code:Check pull requests" --export markdown
        """
    )
    
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Run in interactive mode')
    parser.add_argument('--title', '-t', default='Task List',
                       help='Title for the task list (default: "Task List")')
    parser.add_argument('--add', '-a', action='append', metavar='TASK',
                       help='Add a task. Format: "title" or "title:description"')
    parser.add_argument('--load', '-l', metavar='FILE',
                       help='Load tasks from JSON file')
    parser.add_argument('--export', '-e', choices=['markdown', 'text', 'json'],
                       default='markdown', help='Export format (default: markdown)')
    parser.add_argument('--output', '-o', metavar='FILE',
                       help='Output file (default: print to stdout)')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode()
        return
    
    # Non-interactive mode
    generator = TaskListGenerator()
    generator.set_list_title(args.title)
    
    # Load from file if specified
    if args.load:
        try:
            with open(args.load, 'r', encoding='utf-8') as f:
                generator.load_from_json(f.read())
            print(f"Loaded tasks from: {args.load}")
        except (IOError, ValueError) as e:
            print(f"Error loading file: {e}", file=sys.stderr)
            sys.exit(1)
    
    # Add tasks from command line
    if args.add:
        for task_spec in args.add:
            if ':' in task_spec:
                title, description = task_spec.split(':', 1)
                generator.add_task(title.strip(), description.strip())
            else:
                generator.add_task(task_spec.strip())
    
    # Check if we have any tasks
    if not generator.tasks:
        print("No tasks to export. Use --add to add tasks or --interactive for interactive mode.")
        sys.exit(1)
    
    # Export based on format
    if args.export == 'markdown':
        output = generator.export_to_markdown()
    elif args.export == 'text':
        output = generator.export_to_plain_text()
    elif args.export == 'json':
        output = generator.export_to_json()
    
    # Output to file or stdout
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Task list exported to: {args.output}")
        except IOError as e:
            print(f"Error writing to file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(output)


if __name__ == "__main__":
    main()