# Socrates CLI

Command-line interface and comprehensive command system for Socrates AI framework.

## Features

- **25+ CLI Commands** for project management, code analysis, collaboration, and more
- **Command Infrastructure** with base classes and command handlers
- **Rich Output** with colored text and formatted tables
- **Error Handling** with helpful error messages
- **Integration Ready** with Socratic libraries (learning, analyzer, workflow, conflict, agents)

## Installation

```bash
pip install socrates-cli
```

## Quick Start

### Using as a Library

```python
from socrates_cli.commands import ProjectListCommand, AnalyticsAnalyzeCommand

# Create and use commands
project_list_cmd = ProjectListCommand(orchestrator)
result = project_list_cmd.execute([], context)
```

### Commands Overview

#### Project Management
- `project list` - List all projects
- `project create` - Create new project
- `project load` - Load a project
- `project info` - Display project information

#### Code Analysis
- `code generate` - Generate code
- `code explain` - Explain code
- `code docs` - Generate documentation
- `code review` - Review code

#### Analytics
- `analytics analyze` - Analyze categories
- `analytics trends` - Show progression trends
- `analytics recommend` - Get recommendations
- `analytics summary` - Quick overview

#### Sessions
- `session create` - Create new session
- `session list` - List sessions
- `session load` - Load a session
- `session save` - Save session

#### Collaboration
- `collab add` - Add collaborator
- `collab list` - List collaborators
- `collab role` - Set collaborator role

#### And More...

## Architecture

### Command Base Class

```python
from socrates_cli.commands.base import BaseCommand

class MyCommand(BaseCommand):
    def __init__(self, name: str):
        super().__init__(name)

    def execute(self, args: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
        # Command implementation
        return {"status": "success"}
```

### Command Handler

```python
from socrates_cli.command_handler import CommandHandler

handler = CommandHandler()
handler.register_command(MyCommand("my command"))
result = handler.execute("/my command arg1 arg2", context)
```

## Dependencies

- **socratic-learning** - Learning system integration
- **socratic-analyzer** - Code analysis
- **socratic-workflow** - Workflow orchestration
- **socratic-conflict** - Conflict detection
- **socratic-agents** - Multi-agent orchestration
- **colorama** - Colored terminal output

## Testing

```bash
pytest tests/ -v
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest tests/`
5. Format with Black: `black src/`
6. Check types: `mypy src/`
7. Submit a pull request

## License

MIT - See LICENSE file

## Support

- [GitHub Issues](https://github.com/Nireus79/Socrates-cli/issues)
- [Documentation](https://github.com/Nireus79/Socrates-cli)

---

Part of the Socrates AI Framework ecosystem.
