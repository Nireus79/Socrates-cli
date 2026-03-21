# socrates-cli Library Guide

## Overview

**socrates-cli** is a production-ready command-line interface for the Socrates AI platform. It provides a terminal-based experience for developers and educators to create projects, generate code, and access Socratic AI guidance.

**Current Version**: 0.1.0
**Package Name**: `socrates-cli`
**Python Support**: 3.8+
**License**: MIT
**Status**: Production Ready

## What This Library Does

socrates-cli provides:

### 1. Project Management
- Create new projects
- List and view projects
- Initialize projects from templates
- Configure project settings
- Export projects to GitHub

### 2. Code Generation
- Generate code from specifications
- Interactive code generation
- Multi-file project generation
- Code analysis and suggestions

### 3. Socratic Guidance
- Interactive Socratic questioning
- Step-by-step learning
- Best practice recommendations
- Architecture assistance

### 4. GitHub Integration
- Initialize Git repository
- Create GitHub repository
- Export project to GitHub
- Automatic commit workflow
- Pull request creation

### 5. Authentication
- User registration and login
- Session management
- API key configuration
- Secure credential storage

## Architecture

```
socrates-cli
    │
    ├── commands/        # CLI command modules
    ├── client.py        # API client
    ├── auth.py          # Authentication
    ├── config.py        # Configuration
    └── __init__.py      # Public API
```

## Installation

```bash
# Install from PyPI
pip install socrates-cli

# Install with optional dependencies
pip install socrates-cli[full]

# Install for development
pip install socrates-cli[dev]

# Add to PATH (optional)
# If not using pip, add to ~/.bashrc or ~/.zshrc:
# export PATH="$PATH:~/.local/bin"
```

## Quick Start

### 1. Initialize Configuration
```bash
# Set up API endpoint and credentials
socrates init

# Follow the prompts:
# API Endpoint: http://localhost:8000
# Email: your@email.com
# Password: ****
```

### 2. Create a Project
```bash
# Create new project
socrates project create --name "my-app" --language python

# With template
socrates project create --name "web-api" \
  --template "rest-api" \
  --language python
```

### 3. Generate Code
```bash
# Generate code for project
socrates code generate --project-id abc123 \
  --description "Create user authentication module"

# Generate with options
socrates code generate --project-id abc123 \
  --include-tests \
  --include-docs \
  --style pep8
```

### 4. Export to GitHub
```bash
# Export project to GitHub
socrates project export --project-id abc123 \
  --repository "username/repo-name" \
  --branch main
```

## Command Reference

### Project Commands
```bash
# Create project
socrates project create --name "project-name" \
  --language python \
  --template "template-name" \
  --description "Optional description"

# List projects
socrates project list
socrates project list --format table  # or json, csv

# View project
socrates project show --project-id abc123

# Update project
socrates project update --project-id abc123 \
  --name "new-name" \
  --description "new description"

# Delete project
socrates project delete --project-id abc123

# Export to GitHub
socrates project export --project-id abc123 \
  --repository "user/repo" \
  --branch main
```

### Code Commands
```bash
# Generate code
socrates code generate --project-id abc123 \
  --description "What to generate" \
  --include-tests \
  --include-docs

# Analyze code
socrates code analyze --project-id abc123 \
  --file "src/main.py"

# Show code
socrates code show --project-id abc123 \
  --file "src/main.py"
```

### Socratic Guidance
```bash
# Start interactive session
socrates guidance --topic "API Design"

# Ask a question
socrates ask --question "How do I design a REST API?"

# Get recommendation
socrates recommend --type "architecture" \
  --context "Python web application"
```

### Authentication Commands
```bash
# Register
socrates auth register --email user@example.com

# Login
socrates auth login

# Logout
socrates auth logout

# Show current user
socrates auth whoami

# Configure API key
socrates config set api-key "sk-..."
```

### Configuration Commands
```bash
# Show configuration
socrates config show

# Set configuration
socrates config set api-endpoint http://localhost:8000
socrates config set log-level debug

# Get configuration
socrates config get api-endpoint

# Reset to defaults
socrates config reset
```

### System Commands
```bash
# Show version
socrates --version
socrates version

# Show help
socrates --help
socrates help

# Health check
socrates health

# Show environment
socrates info
socrates env
```

## Configuration

### Configuration File Locations
```bash
# Linux/macOS
~/.config/socrates/config.toml
~/.socrates/config.toml

# Windows
%APPDATA%\socrates\config.toml
C:\Users\<username>\AppData\Local\socrates\config.toml
```

### Environment Variables
```bash
# API Configuration
export SOCRATES_API_ENDPOINT="http://localhost:8000"
export SOCRATES_API_KEY="sk-..."

# Authentication
export SOCRATES_EMAIL="user@example.com"
export SOCRATES_PASSWORD="password"
export SOCRATES_TOKEN="jwt-token"

# Logging
export SOCRATES_LOG_LEVEL="INFO"
export SOCRATES_LOG_FILE="/var/log/socrates.log"

# Project defaults
export SOCRATES_DEFAULT_LANGUAGE="python"
export SOCRATES_DEFAULT_TEMPLATE="basic"
```

### Configuration File Format
```toml
[api]
endpoint = "http://localhost:8000"
timeout = 30
retries = 3

[auth]
email = "user@example.com"
api_key = "sk-..."

[project]
default_language = "python"
default_template = "basic"
auto_initialize_git = true

[logging]
level = "INFO"
format = "json"
file = "/var/log/socrates.log"

[github]
username = "your-github-username"
token = "github-token"  # Optional, for automation
```

## Common Workflows

### Workflow 1: Create and Generate a Project
```bash
# 1. Create project
socrates project create --name "my-api" --language python

# 2. Get the project ID
ID=$(socrates project list --format json | jq -r '.[0].id')

# 3. Generate code
socrates code generate --project-id $ID \
  --description "Create FastAPI REST API"

# 4. Export to GitHub
socrates project export --project-id $ID \
  --repository "username/my-api"
```

### Workflow 2: Update Existing Project
```bash
# 1. List projects
socrates project list

# 2. Update project
socrates project update --project-id abc123 \
  --name "updated-name"

# 3. Generate new code
socrates code generate --project-id abc123 \
  --description "Add database models"

# 4. View changes
socrates code show --project-id abc123
```

### Workflow 3: Learning Path
```bash
# 1. Start Socratic guidance
socrates guidance --topic "REST APIs"

# 2. Ask follow-up questions
socrates ask --question "What about authentication?"

# 3. Get recommendations
socrates recommend --type "best-practices"

# 4. Generate example code
socrates code generate --project-id abc123 \
  --description "Implement what we discussed"
```

## Advanced Usage

### Batch Processing
```bash
# Create multiple projects
for lang in python javascript go; do
  socrates project create --name "project-$lang" \
    --language $lang
done

# Generate code for all
for id in $(socrates project list --format json | jq -r '.[].id'); do
  socrates code generate --project-id $id \
    --description "Auto-generate"
done
```

### Scripting and Automation
```bash
#!/bin/bash
# Create project workflow script

set -e

PROJECT_NAME=$1
LANGUAGE=$2
DESCRIPTION=$3

# Create project
echo "Creating project..."
ID=$(socrates project create \
  --name $PROJECT_NAME \
  --language $LANGUAGE \
  --format json | jq -r '.id')

echo "Project created: $ID"

# Generate code
echo "Generating code..."
socrates code generate \
  --project-id $ID \
  --description "$DESCRIPTION" \
  --include-tests

# Export
echo "Exporting to GitHub..."
socrates project export \
  --project-id $ID \
  --repository "username/$PROJECT_NAME"

echo "Done!"
```

### Output Formatting
```bash
# JSON output
socrates project list --format json | jq '.[] | select(.language=="python")'

# CSV output
socrates project list --format csv > projects.csv

# Table output (default)
socrates project list --format table

# Custom format
socrates project list --format custom:'{id} - {name} ({language})'
```

## Authentication & Security

### Secure Login
```bash
# Interactive login (password prompted)
socrates auth login

# With email
socrates auth login --email user@example.com

# Configure without storing password
socrates config set api-key "sk-..."
socrates config set api-endpoint "http://localhost:8000"
```

### Token Management
```bash
# Show current token
socrates config get token

# Refresh token
socrates auth refresh

# Logout (revoke token)
socrates auth logout
```

### API Key Configuration
```bash
# Set API key
socrates config set api-key "sk-..."

# Use environment variable
export SOCRATES_API_KEY="sk-..."

# Or in config file
cat ~/.config/socrates/config.toml
# [auth]
# api_key = "sk-..."
```

## Troubleshooting

### Connection Issues
```bash
# Check API endpoint
socrates config get api-endpoint

# Test connection
socrates health

# Set endpoint if needed
socrates config set api-endpoint http://localhost:8000
```

### Authentication Issues
```bash
# Check current user
socrates auth whoami

# Login again
socrates auth login

# Clear credentials
socrates config reset
```

### Proxy Configuration
```bash
# Set proxy
export HTTP_PROXY="http://proxy.example.com:8080"
export HTTPS_PROXY="http://proxy.example.com:8080"

# Or in config
[network]
proxy = "http://proxy.example.com:8080"
```

### Debug Mode
```bash
# Enable debug logging
socrates --debug project list

# Set log level
export SOCRATES_LOG_LEVEL=DEBUG
socrates project list

# Output raw API responses
socrates --verbose project list
```

## Integration

### With Git
```bash
# Auto-initialize Git in projects
socrates config set auto-initialize-git true

# View Git status
git -C my-project status

# Make commits
socrates project export --project-id abc123 \
  --message "Generated from Socrates"
```

### With GitHub Actions
```yaml
# .github/workflows/socrates-generate.yml
name: Generate Code with Socrates

on: [push]

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install socrates-cli
      - run: socrates code generate \
          --project-id ${{ secrets.SOCRATES_PROJECT_ID }} \
          --description "Auto-generate from GitHub Actions"
```

## Performance

### Connection Pooling
```bash
# Configure connection pool
socrates config set \
  pool-size 20 \
  pool-recycle 3600
```

### Caching
```bash
# Enable response caching
socrates config set cache-enabled true
socrates config set cache-ttl 3600

# Clear cache
socrates cache clear
```

### Timeout Configuration
```bash
# Set timeout
socrates config set request-timeout 30

# Or per command
socrates project list --timeout 60
```

## Version History

### v0.1.0 (Current)
- Project management (create, list, view, update, delete)
- Code generation
- Code analysis
- GitHub integration
- Socratic guidance
- Authentication and authorization
- Configuration management
- Multiple output formats

## Contributing

When extending socrates-cli:
1. Follow Click command patterns
2. Add tests for new commands
3. Update command help text
4. Update this guide
5. Maintain backward compatibility

## Related Documentation

- [Socrates Ecosystem Architecture](../../docs/SOCRATES_ECOSYSTEM_ARCHITECTURE.md)
- [socrates-core-api Guide](https://github.com/Nireus79/Socrates-api/tree/main/docs)
- [Click Documentation](https://click.palletsprojects.com/)

## Support

For issues or questions:
- GitHub Issues: https://github.com/Nireus79/Socrates-cli/issues
- Documentation: https://github.com/Nireus79/Socrates-cli/tree/main/docs
- Discussions: https://github.com/Nireus79/Socrates-cli/discussions
