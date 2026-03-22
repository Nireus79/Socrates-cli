# Library Integrations CLI - Command Reference

## Overview

The `socrates libraries` command group provides CLI access to all 12 Socratic ecosystem libraries integrated into the Socrates AI system.

---

## Command Structure

```
socrates libraries
├── status                 # Show library integration status
├── analyze                # Analyze code quality
├── knowledge-store        # Store knowledge item
├── knowledge-search       # Search knowledge base
└── docs-generate          # Generate documentation
```

---

## Commands

### `socrates libraries status`

Show status of all library integrations.

**Usage**:
```bash
socrates libraries status
```

**Output**:
```
============================================================
Socratic Library Integration Status
============================================================

Overall: 7/7 libraries enabled

Library                  Status
----------------------------------------
learning                 Enabled
analyzer                 Enabled
conflict                 Enabled
knowledge                Enabled
workflow                 Enabled
docs                     Enabled
performance              Enabled

```

**What it does**:
- Connects to API server at `SOCRATES_API_URL` (default: http://localhost:8000)
- Calls `GET /libraries/status`
- Displays formatted table of library statuses
- Shows count of enabled libraries

**Exit codes**:
- 0: Success
- 1: API error or connection failure

---

### `socrates libraries analyze`

Analyze Python file for code quality issues.

**Usage**:
```bash
socrates libraries analyze --file path/to/file.py
```

**Options**:
- `--file` (required): Path to Python file to analyze

**Output**:
```
Analyzing code in 'path/to/file.py'...
Analysis complete!

Quality Score: 85/100
Issues Found: 2

Recommendations:
  • Add type hints to function parameters
  • Use context managers for file operations
  • Simplify conditional logic

```

**What it does**:
- Reads Python file from disk
- Sends code to `POST /libraries/analyzer/analyze-code`
- Displays quality score (0-100)
- Shows number of issues detected
- Lists top 5 recommendations
- Uses socratic-analyzer library

**Quality Score Interpretation**:
- 90-100: Excellent code quality
- 70-89: Good code quality with minor improvements
- 50-69: Acceptable code with areas for improvement
- 0-49: Significant code quality issues

**Exit codes**:
- 0: Success (may show "unavailable" if analyzer not installed)
- 1: File not found or API error

---

### `socrates libraries knowledge-store`

Store a knowledge item in the enterprise knowledge base.

**Usage**:
```bash
socrates libraries knowledge-store \
  --tenant-id org-123 \
  --title "Python Best Practices" \
  --content "Always use type hints..." \
  --tags python practices best-practices
```

**Options**:
- `--tenant-id` (required): Organization/tenant identifier
- `--title` (required): Knowledge item title
- `--content` (required): Knowledge content/description
- `--tags` (optional): Tags for categorization (repeatable, space-separated)

**Output**:
```
Storing knowledge item...
Knowledge stored successfully!
  Item ID: kb-abc123

```

**What it does**:
- Takes provided content and metadata
- Sends to `POST /libraries/knowledge/store`
- Stores in socratic-knowledge with indexing
- Returns item ID if successful
- Shows "unavailable" if knowledge system not running

**Tags**:
- Can specify multiple tags: `--tags tag1 tag2 tag3`
- Used for searching and categorization
- Optional but recommended

**Exit codes**:
- 0: Success
- 1: API error or missing parameters

---

### `socrates libraries knowledge-search`

Search the knowledge base using semantic search.

**Usage**:
```bash
socrates libraries knowledge-search \
  --tenant-id org-123 \
  --query "type hints python" \
  --limit 10
```

**Options**:
- `--tenant-id` (required): Organization/tenant identifier
- `--query` (required): Search query
- `--limit` (optional): Maximum results to return (default: 5, max: 50)

**Output**:
```
Searching knowledge base...
Found 3 results:

1. Python Type Hints Guide
   Type hints are optional annotations that specify the types...

2. Static Type Checking with mypy
   mypy is a static type checker for Python...

3. Advanced Type Hints Patterns
   Generic types, protocols, type aliases...

```

**What it does**:
- Takes search query
- Sends to `GET /libraries/knowledge/search`
- Uses semantic search (not keyword matching)
- Displays results with title and preview
- Results are ranked by relevance

**Query Tips**:
- Use natural language: "how to optimize database queries"
- Include domain keywords: "python performance optimization"
- Be specific: "flask web framework routing" vs "web framework"

**Exit codes**:
- 0: Success (may show "No results found")
- 1: API error or missing parameters

---

### `socrates libraries docs-generate`

Generate project documentation automatically.

**Usage**:
```bash
socrates libraries docs-generate \
  --project-name "My Project" \
  --description "A Socratic tutoring application"
```

**Options**:
- `--project-name` (required): Project name
- `--description` (optional): Project description

**Output**:
```
Generating documentation for 'My Project'...
Documentation generated!

# My Project

A Socratic tutoring application

## Installation

```bash
pip install my-project
```

## Usage

```python
from my_project import Socrates
socrates = Socrates()
```

## Features

- Socratic method-based tutoring
- Multi-agent code generation
- Real-time learning analytics

## License

MIT License

```

**What it does**:
- Takes project information
- Sends to `POST /libraries/docs/generate-readme`
- Uses socratic-docs library with LLM
- Generates comprehensive README
- Includes installation, usage, features sections
- Shows "unavailable" if docs generator not running

**Generated Content Includes**:
- Project title and description
- Installation instructions
- Usage examples
- Features overview
- License section
- Contributing guidelines (if applicable)

**Exit codes**:
- 0: Success
- 1: API error or missing parameters

---

## Common Workflows

### Workflow 1: Code Review Pipeline

```bash
# 1. Check library availability
socrates libraries status

# 2. Analyze your code
socrates libraries analyze --file myapp.py

# 3. Store analysis results as knowledge
socrates libraries knowledge-store \
  --tenant-id myorg \
  --title "Code Review Results for myapp.py" \
  --content "Quality score: 85/100. Main issues: Add type hints, optimize loops." \
  --tags review code-quality

# 4. Later, search for similar issues
socrates libraries knowledge-search \
  --tenant-id myorg \
  --query "type hints code quality" \
  --limit 5
```

### Workflow 2: Knowledge Base Building

```bash
# Build corporate knowledge base
socrates libraries knowledge-store \
  --tenant-id mycompany \
  --title "REST API Design Standards" \
  --content "Our company uses RESTful conventions..." \
  --tags api design standards

socrates libraries knowledge-store \
  --tenant-id mycompany \
  --title "Python Performance Best Practices" \
  --content "Always profile before optimizing..." \
  --tags python performance optimization

socrates libraries knowledge-store \
  --tenant-id mycompany \
  --title "Security Guidelines" \
  --content "Never store secrets in code..." \
  --tags security guidelines

# Search the knowledge base
socrates libraries knowledge-search \
  --tenant-id mycompany \
  --query "API design patterns" \
  --limit 5
```

### Workflow 3: Project Setup

```bash
# Create new project
socrates project create --name "MyNewApp" --owner me

# Generate initial documentation
socrates libraries docs-generate \
  --project-name "MyNewApp" \
  --description "A web application for managing tasks"

# Analyze generated code
socrates code generate --project-id project-123
socrates libraries analyze --file generated_code.py
```

### Workflow 4: Team Collaboration

```bash
# Centralized knowledge base for team
TENANT_ID="team-acme"

# Store team standards
socrates libraries knowledge-store \
  --tenant-id $TENANT_ID \
  --title "Code Review Checklist" \
  --content "1. Type hints present\n2. Docstrings complete\n3. Tests written" \
  --tags team standards review checklist

# Team members search standards
socrates libraries knowledge-search \
  --tenant-id $TENANT_ID \
  --query "code review standards" \
  --limit 10
```

---

## Environment Variables

```bash
# Set API server URL (default: http://localhost:8000)
export SOCRATES_API_URL=http://api.socrates.app:8000

# Use in commands (URL determined at command execution)
socrates libraries status
```

---

## Error Messages and Troubleshooting

### "Connection error: Is the API server running?"

**Cause**: API server not running or wrong URL

**Solutions**:
```bash
# Check if API is running
curl http://localhost:8000/health

# Set correct API URL
export SOCRATES_API_URL=http://your-server:8000

# Verify connection
socrates libraries status
```

### "socratic-analyzer is not available"

**Cause**: Optional library not installed in API server

**Solution**:
```bash
# On API server machine
pip install socratic-analyzer

# Restart API server
```

### "No results found"

**Cause**: Knowledge base empty or query doesn't match

**Solutions**:
1. Store some knowledge items first
2. Try broader search query: "python" instead of "python type hints"
3. Check tenant_id is correct
4. Increase limit to see more results

### "File not found"

**Cause**: Invalid path provided to --file option

**Solutions**:
```bash
# Use absolute path
socrates libraries analyze --file /home/user/project/code.py

# Use relative path from current directory
cd /home/user/project
socrates libraries analyze --file code.py

# Check file exists
ls -la /path/to/code.py
```

---

## Tips and Tricks

### Tip 1: Chain Commands for Automation

```bash
#!/bin/bash
# analyze_and_store.sh

CODE_FILE=$1
PROJECT_NAME=$2

# Analyze code
socrates libraries analyze --file "$CODE_FILE"

# Store analysis in knowledge base
socrates libraries knowledge-store \
  --tenant-id default \
  --title "Analysis of $PROJECT_NAME" \
  --content "$(socrates libraries analyze --file "$CODE_FILE")" \
  --tags analysis automated
```

### Tip 2: Use JSON Output for Integration

```bash
# Get library status and parse with jq
curl http://localhost:8000/libraries/status | jq '.libraries'
```

### Tip 3: Bulk Knowledge Import

```bash
#!/bin/bash
# import_docs.sh

TENANT_ID=$1
DOCS_DIR=$2

for file in $DOCS_DIR/*.md; do
    title=$(basename "$file" .md)
    content=$(cat "$file")

    socrates libraries knowledge-store \
        --tenant-id "$TENANT_ID" \
        --title "$title" \
        --content "$content" \
        --tags documentation imported
done
```

### Tip 4: Search Knowledge and Open in Editor

```bash
#!/bin/bash
# search_and_edit.sh

QUERY=$1
TENANT_ID=${2:-default}

# Search and capture first result
socrates libraries knowledge-search \
    --tenant-id "$TENANT_ID" \
    --query "$QUERY" \
    --limit 1
```

---

## Integration with Other CLI Commands

The `libraries` command group integrates with other Socrates CLI commands:

```bash
# Generate code, then analyze it
socrates code generate --project-id proj-123
socrates libraries analyze --file generated_code.py

# Store learned patterns in knowledge base
socrates libraries knowledge-store \
  --tenant-id org-123 \
  --title "Generated Code Pattern" \
  --content "Used for project proj-123"

# Search for similar patterns
socrates libraries knowledge-search \
  --tenant-id org-123 \
  --query "code generation patterns"
```

---

## API Endpoints Called

Each CLI command calls corresponding API endpoint:

| CLI Command | API Endpoint | Method |
|-------------|--------------|--------|
| `libraries status` | `/libraries/status` | GET |
| `libraries analyze` | `/libraries/analyzer/analyze-code` | POST |
| `libraries knowledge-store` | `/libraries/knowledge/store` | POST |
| `libraries knowledge-search` | `/libraries/knowledge/search` | GET |
| `libraries docs-generate` | `/libraries/docs/generate-readme` | POST |

See `LIBRARY_INTEGRATIONS_QUICK_REFERENCE.md` for API documentation.

---

## Version Information

```bash
# Check CLI version
socrates --version

# Check API server version (if running)
curl http://localhost:8000/info
```

---

## Support and Feedback

- **Issues**: Report at https://github.com/Nireus79/Socrates/issues
- **Documentation**: https://github.com/Nireus79/Socrates/tree/master/docs
- **Quick Reference**: See `LIBRARY_INTEGRATIONS_QUICK_REFERENCE.md`
- **Full Integration Details**: See `FULL_LIBRARY_INTEGRATION_SUMMARY.md`
