# Task List Generator - Examples and Demonstrations

This document provides examples of using the Task List Generator CLI tool.

## Basic Usage Examples

### Simple Task List Creation
```bash
python3 task_list_generator.py --title "Daily Tasks" --add "Check emails" --add "Review code" --export markdown
```

**Output:**
```markdown
# Daily Tasks

*Generated on 2025-07-03 21:37:42*

- [ ] **Check emails**

- [ ] **Review code**
```

### Tasks with Descriptions
```bash
python3 task_list_generator.py --title "Research Project" --add "Literature review:Survey recent papers on mRNA vaccines" --add "Experiment design:Plan immunogenicity studies" --export text
```

**Output:**
```
Research Project
===============

Generated on 2025-07-03 21:37:42

 1. [TODO] Literature review
    Survey recent papers on mRNA vaccines

 2. [TODO] Experiment design
    Plan immunogenicity studies
```

### JSON Export for Integration
```bash
python3 task_list_generator.py --title "Lab Protocol" --add "Prepare samples" --add "Run assay:96-well plate format" --export json
```

**Output:**
```json
{
  "title": "Lab Protocol",
  "generated_at": "2025-07-03T21:37:42.123456",
  "tasks": [
    {
      "title": "Prepare samples",
      "description": "",
      "completed": false,
      "created_at": "2025-07-03T21:37:42.123440"
    },
    {
      "title": "Run assay",
      "description": "96-well plate format",
      "completed": false,
      "created_at": "2025-07-03T21:37:42.123452"
    }
  ]
}
```

## Interactive Mode Examples

### Starting Interactive Mode
```bash
python3 task_list_generator.py --interactive
```

**Interactive Session:**
```
Task List Generator - Interactive Mode
========================================
Enter task list title (default: 'Task List'): Research Milestones

Creating task list: Research Milestones
Enter tasks (type 'done' when finished, 'help' for commands)

Command> add
Task title: Complete literature review
Task description (optional): Comprehensive survey of neoantigen research
Added task: Complete literature review

Command> add
Task title: Design experiments
Task description (optional): Plan validation studies
Added task: Design experiments

Command> list

Current tasks in 'Research Milestones':
  1. ○ Complete literature review
     Comprehensive survey of neoantigen research
  2. ○ Design experiments
     Plan validation studies

Command> toggle 1
Task 'Complete literature review' marked as completed

Command> export markdown

# Research Milestones

*Generated on 2025-07-03 21:37:42*

- [x] **Complete literature review**
  Comprehensive survey of neoantigen research

- [ ] **Design experiments**
  Plan validation studies

Command> done

Completed task list with 2 tasks.
Export format (markdown/text/json): markdown
Save to file (enter filename or press Enter to print): research_milestones.md
Task list saved to: research_milestones.md
```

## File Operations

### Saving to Files
```bash
python3 task_list_generator.py --title "Project Tasks" --add "Task 1" --add "Task 2" --export markdown --output tasks.md
```

### Loading and Modifying
```bash
# Save initial tasks
python3 task_list_generator.py --title "Initial Tasks" --add "Task A" --add "Task B" --export json --output tasks.json

# Load and add more tasks
python3 task_list_generator.py --load tasks.json --add "Task C:Additional task" --export markdown --output updated_tasks.md
```

## Integration with mRNA Vaccine Research

### Research Workflow Example
```bash
python3 task_list_generator.py --title "mRNA Vaccine Development Pipeline" \
  --add "Neoantigen identification:Analyze tumor sequencing data" \
  --add "Plasmid design:Create expression vector using plasmid_builder.py" \
  --add "In vitro validation:Test protein expression and folding" \
  --add "Immunogenicity testing:Assess T cell activation in vitro" \
  --add "Mouse studies:Evaluate vaccine efficacy in vivo" \
  --add "Manufacturing optimization:Scale up production process" \
  --export markdown --output vaccine_development_tasks.md
```

### Lab Protocol Checklist
```bash
python3 task_list_generator.py --title "Daily Lab Protocol" \
  --add "Check equipment status" \
  --add "Prepare solutions:Make fresh buffers and media" \
  --add "Run plasmid_builder.py:Generate today's constructs" \
  --add "Document results:Update lab notebook" \
  --export text --output daily_protocol.txt
```

## Advanced Usage

### Combining with Other Tools
```bash
# Generate research tasks and save as JSON for further processing
python3 task_list_generator.py --title "Research Pipeline" \
  --add "Data collection" \
  --add "Analysis" \
  --add "Reporting" \
  --export json --output research_tasks.json

# Convert JSON to markdown later
python3 task_list_generator.py --load research_tasks.json --export markdown --output final_report.md
```

### Help and Version Information
```bash
# Get help
python3 task_list_generator.py --help

# Check version
python3 task_list_generator.py --version
```

## Tips and Best Practices

1. **Use descriptive titles**: Make task titles clear and actionable
2. **Add context with descriptions**: Use the colon notation for detailed descriptions
3. **Choose appropriate formats**: 
   - Markdown for documentation and GitHub integration
   - Plain text for simple checklists
   - JSON for programmatic processing
4. **Save important lists**: Use `--output` to save task lists for future reference
5. **Interactive mode for exploration**: Use interactive mode when planning or brainstorming
6. **Batch mode for automation**: Use command line arguments for scripted workflows