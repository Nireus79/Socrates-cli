"""
Socrates CLI - Command-line interface for Socrates AI

Provides a user-friendly command-line interface to the Socrates AI platform.
Can operate in two modes:
1. API mode (recommended): Connects to a running Socrates API server
2. Standalone mode: Uses local orchestrator (requires socrates-ai package)

Uses Click for command-line argument parsing and colorama for colored output.
"""

import logging
import os
import sys
from pathlib import Path
from typing import Optional

import click
import httpx
from colorama import Fore, Style, init

from socratic_core import SocratesConfig, ConfigBuilder

from socrates_cli.commands import get_command_client

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("socrates_cli")

# Global API client
_api_client: Optional[httpx.Client] = None
_api_url: str = os.getenv("SOCRATES_API_URL", "http://localhost:8000")


def get_api_client() -> httpx.Client:
    """Get or create the API client."""
    global _api_client
    if _api_client is None:
        _api_client = httpx.Client(base_url=_api_url, timeout=30.0)
    return _api_client


def api_request(
    method: str, endpoint: str, json_data: Optional[dict] = None, **kwargs
) -> dict:
    """
    Make a request to the Socrates API.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint path
        json_data: JSON payload for POST/PUT requests
        **kwargs: Additional httpx.Client.request arguments

    Returns:
        Response data as dictionary

    Raises:
        click.ClickException: If API request fails
    """
    try:
        client = get_api_client()
        response = client.request(method, endpoint, json=json_data, **kwargs)
        response.raise_for_status()
        return response.json() if response.text else {}
    except httpx.HTTPStatusError as e:
        error_msg = f"API Error: {e.response.status_code}"
        try:
            error_data = e.response.json()
            if "message" in error_data:
                error_msg += f" - {error_data['message']}"
        except (ValueError, KeyError):
            pass
        raise click.ClickException(error_msg)
    except httpx.RequestError as e:
        raise click.ClickException(
            f"Connection error: {e}. Is the API server running at {_api_url}?"
        )


@click.group()
@click.version_option(version="1.3.3", prog_name="socrates")
@click.pass_context
def main(ctx):
    """
    Socrates AI - A Socratic method tutoring system powered by Claude AI

    Use 'socrates COMMAND --help' for more information on a command.

    Examples:
        socrates init                  Initialize a new Socrates project
        socrates project create        Create a new project
        socrates ask                   Ask a Socratic question
        socrates generate-code         Generate code for your project

    API Configuration:
        Set SOCRATES_API_URL to change the API server (default: http://localhost:8000)
    """
    ctx.ensure_object(dict)


@main.command()
@click.option(
    "--api-key",
    envvar="ANTHROPIC_API_KEY",
    prompt=False,
    hide_input=True,
    help="Claude API key (or set ANTHROPIC_API_KEY env var)",
)
@click.option(
    "--data-dir",
    type=click.Path(),
    default=None,
    help="Data directory for storing projects (defaults to ~/.socrates)",
)
def init(api_key, data_dir):
    """
    Initialize Socrates configuration.

    Creates necessary directories and validates your Claude API key.
    """
    if not api_key:
        api_key = click.prompt("Enter your Claude API key", hide_input=True)

    try:
        # Test the configuration locally
        config = ConfigBuilder(api_key)
        if data_dir:
            config = config.with_data_dir(Path(data_dir))
        config = config.build()

        # Test API connection
        try:
            result = api_request("GET", "/health")
            click.echo(f"{Fore.GREEN}API Server: OK{Style.RESET_ALL}")
        except click.ClickException as e:
            click.echo(f"{Fore.YELLOW}Warning: {e}{Style.RESET_ALL}")

        click.echo(f"{Fore.GREEN}Socrates initialized successfully!{Style.RESET_ALL}")
        click.echo(f"  Data directory: {config.data_dir}")
        click.echo(f"  Model: {config.claude_model}")
        click.echo(f"  API Server: {_api_url}")

    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", err=True)
        sys.exit(1)


@main.group()
def project():
    """Manage projects."""
    pass


@project.command("create")
@click.option("--name", prompt="Project name", help="Name of the project")
@click.option("--owner", prompt="Owner username", help="Project owner")
@click.option("--description", default="", help="Project description")
def project_create(name, owner, description):
    """Create a new project."""
    try:
        result = api_request(
            "POST",
            "/projects",
            json_data={
                "name": name,
                "owner": owner,
                "description": description,
            },
        )

        if result.get("status") == "success":
            project = result.get("data", {})
            click.echo(f"{Fore.GREEN}Project created successfully!{Style.RESET_ALL}")
            click.echo(f"  Project ID: {project.get('project_id', 'N/A')}")
            click.echo(f"  Name: {project.get('name', 'N/A')}")
        else:
            message = result.get("message", "Unknown error")
            click.echo(
                f"{Fore.RED}Failed to create project: {message}{Style.RESET_ALL}",
                err=True,
            )
            sys.exit(1)

    except click.ClickException:
        raise
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", err=True)
        sys.exit(1)


@project.command("list")
@click.option("--owner", default=None, help="Filter by project owner")
def project_list(owner):
    """List projects."""
    try:
        params = {}
        if owner:
            params["owner"] = owner

        result = api_request("GET", "/projects", params=params)

        projects = result.get("data", [])

        if not projects:
            click.echo(f"{Fore.YELLOW}No projects found{Style.RESET_ALL}")
            return

        click.echo(
            f"{Fore.CYAN}{'ID':<8} {'Name':<20} {'Owner':<15}{Style.RESET_ALL}"
        )
        click.echo("-" * 43)

        for project in projects:
            click.echo(
                f"{project.get('project_id', 'N/A'):<8} {project.get('name', 'N/A'):<20} {project.get('owner', 'N/A'):<15}"
            )

    except click.ClickException:
        raise
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", err=True)
        sys.exit(1)


@main.group()
def code():
    """Generate and manage code."""
    pass


@code.command("generate")
@click.option("--project-id", prompt="Project ID", help="Project ID to generate code for")
def generate_code(project_id):
    """Generate code for a project."""
    try:
        # Load the project first
        result = api_request("GET", f"/projects/{project_id}")

        if not result.get("status") == "success":
            click.echo(f"{Fore.RED}Project not found{Style.RESET_ALL}", err=True)
            sys.exit(1)

        project = result.get("data", {})

        # Generate code
        click.echo(
            f"{Fore.CYAN}Generating code for project '{project.get('name')}'...{Style.RESET_ALL}"
        )

        code_result = api_request(
            "POST",
            f"/projects/{project_id}/code/generate",
            json_data={},
        )

        script = code_result.get("data", {}).get("code", "")
        lines = len(script.split("\n"))

        click.echo(f"{Fore.GREEN}Code generated successfully!{Style.RESET_ALL}")
        click.echo(f"  Lines of code: {lines}")
        click.echo("")
        click.echo(f"{Fore.CYAN}--- Generated Code ---{Style.RESET_ALL}")
        click.echo(script)

    except click.ClickException:
        raise
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", err=True)
        sys.exit(1)


@main.group()
def chat():
    """Start interactive chat sessions."""
    pass


@chat.command("start")
@click.option("--project-id", required=True, help="Project ID to chat about")
@click.option("--session-id", default=None, help="Existing session ID to resume")
def chat_start(project_id, session_id):
    """Start an interactive chat session."""
    try:
        if session_id:
            # Resume existing session
            result = api_request("GET", f"/chat/sessions/{session_id}")
            if result.get("status") != "success":
                click.echo(f"{Fore.RED}Session not found{Style.RESET_ALL}", err=True)
                sys.exit(1)
            click.echo(f"{Fore.GREEN}Resumed session: {session_id}{Style.RESET_ALL}")
        else:
            # Create new session
            result = api_request("POST", "/chat/sessions", json_data={"project_id": project_id})
            if result.get("status") != "success":
                click.echo(f"{Fore.RED}Failed to create session{Style.RESET_ALL}", err=True)
                sys.exit(1)
            session_id = result.get("data", {}).get("session_id")
            click.echo(f"{Fore.GREEN}Session created: {session_id}{Style.RESET_ALL}")

        # Interactive loop
        click.echo(f"{Fore.CYAN}Chat Session Started (type 'exit' to quit){Style.RESET_ALL}")
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() == "exit":
                break

            # Send message
            msg_result = api_request(
                "POST",
                f"/chat/sessions/{session_id}/messages",
                json_data={"message": user_input},
            )

            if msg_result.get("status") == "success":
                response = msg_result.get("data", {}).get("response", "")
                click.echo(f"\n{Fore.CYAN}Socrates: {response}{Style.RESET_ALL}")
            else:
                click.echo(f"{Fore.RED}Error: {msg_result.get('message', 'Unknown error')}{Style.RESET_ALL}")

    except click.ClickException:
        raise
    except KeyboardInterrupt:
        click.echo(f"\n{Fore.YELLOW}Chat session ended{Style.RESET_ALL}")
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", err=True)
        sys.exit(1)


@main.group()
def knowledge():
    """Manage project knowledge base."""
    pass


@knowledge.command("list")
@click.option("--project-id", required=True, help="Project ID")
def knowledge_list(project_id):
    """List knowledge base documents."""
    try:
        result = api_request("GET", f"/projects/{project_id}/knowledge")

        documents = result.get("data", [])
        if not documents:
            click.echo(f"{Fore.YELLOW}No documents in knowledge base{Style.RESET_ALL}")
            return

        click.echo(
            f"{Fore.CYAN}{'ID':<12} {'Name':<40} {'Size (KB)':<12}{Style.RESET_ALL}"
        )
        click.echo("-" * 64)

        for doc in documents:
            size_kb = doc.get("size", 0) // 1024
            click.echo(
                f"{doc.get('id', 'N/A'):<12} {doc.get('name', 'N/A'):<40} {size_kb:<12}"
            )

    except click.ClickException:
        raise
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", err=True)
        sys.exit(1)


@knowledge.command("import")
@click.option("--project-id", required=True, help="Project ID")
@click.option("--path", required=True, type=click.Path(exists=True), help="File path to import")
def knowledge_import(project_id, path):
    """Import a document into the knowledge base."""
    try:
        with open(path, "rb") as f:
            files = {"file": f}
            client = get_api_client()
            response = client.post(
                f"/projects/{project_id}/knowledge/import",
                files=files,
                headers={},  # httpx handles multipart
            )
            response.raise_for_status()
            result = response.json()

            if result.get("status") == "success":
                click.echo(f"{Fore.GREEN}Document imported successfully!{Style.RESET_ALL}")
                click.echo(f"  Document ID: {result.get('data', {}).get('id')}")
            else:
                click.echo(f"{Fore.RED}Import failed: {result.get('message')}{Style.RESET_ALL}", err=True)
                sys.exit(1)

    except click.ClickException:
        raise
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", err=True)
        sys.exit(1)


@main.group()
def analytics():
    """View project analytics and metrics."""
    pass


@analytics.command("summary")
@click.option("--project-id", required=True, help="Project ID")
def analytics_summary(project_id):
    """Show analytics summary for a project."""
    try:
        result = api_request("GET", f"/projects/{project_id}/analytics")

        if result.get("status") != "success":
            click.echo(f"{Fore.RED}Failed to fetch analytics{Style.RESET_ALL}", err=True)
            sys.exit(1)

        analytics = result.get("data", {})

        click.echo(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
        click.echo(f"{Fore.CYAN}Project Analytics{Style.RESET_ALL}")
        click.echo(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
        click.echo("")

        click.echo(f"Messages: {analytics.get('message_count', 0)}")
        click.echo(f"Artifacts Generated: {analytics.get('artifact_count', 0)}")
        click.echo(f"Session Duration: {analytics.get('total_duration_minutes', 0)} minutes")
        click.echo(f"Last Active: {analytics.get('last_active', 'N/A')}")

        click.echo("")

    except click.ClickException:
        raise
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", err=True)
        sys.exit(1)


@main.group()
def collaboration():
    """Manage project collaboration."""
    pass


@collaboration.command("add")
@click.option("--project-id", required=True, help="Project ID")
@click.option("--username", prompt="Username to invite", help="Username of collaborator")
@click.option("--role", type=click.Choice(["viewer", "editor", "admin"]), default="editor")
def collab_add(project_id, username, role):
    """Invite a collaborator to the project."""
    try:
        result = api_request(
            "POST",
            f"/projects/{project_id}/collaborators",
            json_data={"username": username, "role": role},
        )

        if result.get("status") == "success":
            click.echo(f"{Fore.GREEN}Collaborator invited!{Style.RESET_ALL}")
            click.echo(f"  User: {username}")
            click.echo(f"  Role: {role}")
        else:
            click.echo(f"{Fore.RED}Failed: {result.get('message')}{Style.RESET_ALL}", err=True)
            sys.exit(1)

    except click.ClickException:
        raise
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", err=True)
        sys.exit(1)


@collaboration.command("list")
@click.option("--project-id", required=True, help="Project ID")
def collab_list(project_id):
    """List project collaborators."""
    try:
        result = api_request("GET", f"/projects/{project_id}/collaborators")

        collaborators = result.get("data", [])
        if not collaborators:
            click.echo(f"{Fore.YELLOW}No collaborators{Style.RESET_ALL}")
            return

        click.echo(
            f"{Fore.CYAN}{'Username':<20} {'Role':<15} {'Joined':<20}{Style.RESET_ALL}"
        )
        click.echo("-" * 55)

        for collab in collaborators:
            click.echo(
                f"{collab.get('username', 'N/A'):<20} {collab.get('role', 'N/A'):<15} {collab.get('joined_date', 'N/A'):<20}"
            )

    except click.ClickException:
        raise
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", err=True)
        sys.exit(1)


@main.group()
def commands():
    """Manage and discover available commands."""
    pass


@commands.command("list")
@click.option("--category", default=None, help="Filter by category")
def commands_list(category):
    """List all available commands."""
    try:
        client = get_command_client(_api_url)
        result = client.list_commands(category=category)

        if result.get("status") != "success":
            click.echo(f"{Fore.RED}Failed to list commands{Style.RESET_ALL}", err=True)
            sys.exit(1)

        commands_dict = result.get("data", {})

        if not commands_dict:
            click.echo(f"{Fore.YELLOW}No commands found{Style.RESET_ALL}")
            return

        click.echo(
            f"{Fore.CYAN}{'Command':<30} {'Category':<25} {'Description':<45}{Style.RESET_ALL}"
        )
        click.echo("-" * 100)

        for cmd_name in sorted(commands_dict.keys()):
            cmd_info = commands_dict[cmd_name]
            category_name = cmd_info.get("category", "N/A")
            description = cmd_info.get("description", "N/A")[:42] + "..."

            click.echo(f"{cmd_name:<30} {category_name:<25} {description:<45}")

    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", err=True)
        sys.exit(1)


@commands.command("categories")
def commands_categories():
    """List all command categories."""
    try:
        client = get_command_client(_api_url)
        result = client.list_categories()

        if result.get("status") != "success":
            click.echo(f"{Fore.RED}Failed to list categories{Style.RESET_ALL}", err=True)
            sys.exit(1)

        categories = result.get("data", [])

        if not categories:
            click.echo(f"{Fore.YELLOW}No categories found{Style.RESET_ALL}")
            return

        click.echo(f"{Fore.CYAN}Available Categories:{Style.RESET_ALL}")
        for category in sorted(categories):
            click.echo(f"  • {category}")

    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", err=True)
        sys.exit(1)


@commands.command("help")
@click.option("--command", default=None, help="Specific command to get help for")
def commands_help(command):
    """Get help documentation for commands."""
    try:
        client = get_command_client(_api_url)
        result = client.get_help(command=command)

        if result.get("status") != "success":
            click.echo(f"{Fore.RED}Failed to get help{Style.RESET_ALL}", err=True)
            sys.exit(1)

        help_text = result.get("data", "")
        click.echo(help_text)

    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", err=True)
        sys.exit(1)


@commands.command("search")
@click.option("--query", prompt="Search query", help="Search for commands")
def commands_search(query):
    """Search for commands by name or description."""
    try:
        client = get_command_client(_api_url)
        matching = client.search_commands(query)

        if not matching:
            click.echo(f"{Fore.YELLOW}No commands found matching '{query}'{Style.RESET_ALL}")
            return

        click.echo(f"{Fore.CYAN}Found {len(matching)} matching commands:{Style.RESET_ALL}")
        for cmd_name in sorted(matching):
            click.echo(f"  • {cmd_name}")

        # Offer to show help
        if len(matching) == 1:
            show_help = click.confirm(f"\nShow help for '{matching[0]}'?")
            if show_help:
                result = client.get_help(command=matching[0])
                help_text = result.get("data", "")
                click.echo(f"\n{help_text}")

    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", err=True)
        sys.exit(1)


@main.group()
def libraries():
    """Manage Socratic ecosystem library integrations."""
    pass


@libraries.command("status")
def libraries_status():
    """Show status of all library integrations."""
    try:
        result = api_request("GET", "/libraries/status")

        if result.get("status") == "error":
            click.echo(f"{Fore.RED}Failed to get library status{Style.RESET_ALL}", err=True)
            sys.exit(1)

        click.echo(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
        click.echo(f"{Fore.CYAN}Socratic Library Integration Status{Style.RESET_ALL}")
        click.echo(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
        click.echo("")

        libraries_info = result.get("libraries", {})
        enabled = result.get("enabled", 0)
        total = result.get("total", 0)

        click.echo(f"Overall: {enabled}/{total} libraries enabled")
        click.echo("")

        click.echo(f"{Fore.CYAN}{'Library':<25} {'Status':<15}{Style.RESET_ALL}")
        click.echo("-" * 40)

        for lib_name, is_enabled in libraries_info.items():
            status = f"{Fore.GREEN}Enabled{Style.RESET_ALL}" if is_enabled else f"{Fore.YELLOW}Disabled{Style.RESET_ALL}"
            click.echo(f"{lib_name:<25} {status}")

        click.echo("")

    except click.ClickException:
        raise
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", err=True)
        sys.exit(1)


@libraries.command("analyze")
@click.option("--file", required=True, type=click.Path(exists=True), help="Python file to analyze")
def libraries_analyze(file):
    """Analyze code quality using socratic-analyzer."""
    try:
        with open(file, "r") as f:
            code = f.read()

        click.echo(f"{Fore.CYAN}Analyzing code in '{file}'...{Style.RESET_ALL}")

        result = api_request(
            "POST",
            "/libraries/analyzer/analyze-code",
            json_data={"code": code, "filename": file},
        )

        if not result:
            click.echo(f"{Fore.YELLOW}Code analyzer unavailable{Style.RESET_ALL}")
            return

        click.echo(f"{Fore.GREEN}Analysis complete!{Style.RESET_ALL}")
        click.echo("")

        quality_score = result.get("quality_score", 0)
        issues_count = result.get("issues_count", 0)

        click.echo(f"Quality Score: {Fore.CYAN}{quality_score}/100{Style.RESET_ALL}")
        click.echo(f"Issues Found: {issues_count}")

        recommendations = result.get("recommendations", [])
        if recommendations:
            click.echo(f"\n{Fore.CYAN}Recommendations:{Style.RESET_ALL}")
            for rec in recommendations[:5]:
                click.echo(f"  • {rec}")

        click.echo("")

    except click.ClickException:
        raise
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", err=True)
        sys.exit(1)


@libraries.command("knowledge-store")
@click.option("--tenant-id", required=True, help="Organization/tenant ID")
@click.option("--title", required=True, help="Knowledge item title")
@click.option("--content", required=True, help="Knowledge content")
@click.option("--tags", multiple=True, help="Tags for categorization")
def libraries_knowledge_store(tenant_id, title, content, tags):
    """Store knowledge in socratic-knowledge."""
    try:
        click.echo(f"{Fore.CYAN}Storing knowledge item...{Style.RESET_ALL}")

        result = api_request(
            "POST",
            "/libraries/knowledge/store",
            json_data={
                "tenant_id": tenant_id,
                "title": title,
                "content": content,
                "tags": list(tags) if tags else [],
            },
        )

        if result.get("status") == "stored" or result.get("item_id"):
            click.echo(f"{Fore.GREEN}Knowledge stored successfully!{Style.RESET_ALL}")
            if result.get("item_id"):
                click.echo(f"  Item ID: {result.get('item_id')}")
        else:
            click.echo(f"{Fore.YELLOW}Knowledge system unavailable{Style.RESET_ALL}")

    except click.ClickException:
        raise
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", err=True)
        sys.exit(1)


@libraries.command("knowledge-search")
@click.option("--tenant-id", required=True, help="Organization/tenant ID")
@click.option("--query", required=True, help="Search query")
@click.option("--limit", default=5, type=int, help="Max results")
def libraries_knowledge_search(tenant_id, query, limit):
    """Search knowledge base using socratic-knowledge."""
    try:
        click.echo(f"{Fore.CYAN}Searching knowledge base...{Style.RESET_ALL}")

        result = api_request(
            "GET",
            "/libraries/knowledge/search",
            params={
                "tenant_id": tenant_id,
                "query": query,
                "limit": limit,
            },
        )

        if not result:
            click.echo(f"{Fore.YELLOW}No results found{Style.RESET_ALL}")
            return

        click.echo(f"{Fore.GREEN}Found {len(result)} results:{Style.RESET_ALL}")
        click.echo("")

        for i, item in enumerate(result, 1):
            click.echo(f"{Fore.CYAN}{i}. {item.get('title', 'N/A')}{Style.RESET_ALL}")
            preview = item.get("content_preview", "")
            if preview:
                click.echo(f"   {preview[:100]}...")
            click.echo("")

    except click.ClickException:
        raise
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", err=True)
        sys.exit(1)


@libraries.command("docs-generate")
@click.option("--project-name", required=True, help="Project name")
@click.option("--description", default="", help="Project description")
def libraries_docs_generate(project_name, description):
    """Generate documentation using socratic-docs."""
    try:
        click.echo(f"{Fore.CYAN}Generating documentation for '{project_name}'...{Style.RESET_ALL}")

        result = api_request(
            "POST",
            "/libraries/docs/generate-readme",
            json_data={
                "project_info": {
                    "name": project_name,
                    "description": description,
                }
            },
        )

        if result:
            click.echo(f"{Fore.GREEN}Documentation generated!{Style.RESET_ALL}")
            click.echo(f"\n{result}\n")
        else:
            click.echo(f"{Fore.YELLOW}Documentation generator unavailable{Style.RESET_ALL}")

    except click.ClickException:
        raise
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", err=True)
        sys.exit(1)


@main.command()
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"]),
    default="INFO",
    help="Logging level",
)
def info(log_level):
    """Show Socrates system information."""
    try:
        result = api_request("GET", "/info")

        click.echo(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
        click.echo(f"{Fore.CYAN}Socrates AI System Information{Style.RESET_ALL}")
        click.echo(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
        click.echo("")

        info_data = result.get("data", {})
        click.echo(f"Library Version: {info_data.get('version', 'N/A')}")
        click.echo(f"Claude Model: {info_data.get('claude_model', 'N/A')}")
        click.echo(f"Data Directory: {info_data.get('data_dir', 'N/A')}")
        click.echo(f"Log Level: {log_level}")
        click.echo("")

        # Test API connection
        try:
            health = api_request("GET", "/health")
            click.echo(f"{Fore.GREEN}API Connection: OK{Style.RESET_ALL}")
        except Exception:
            click.echo(f"{Fore.RED}API Connection: FAILED{Style.RESET_ALL}")

        click.echo("")

    except click.ClickException:
        raise
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", err=True)
        sys.exit(1)


def cleanup():
    """Clean up resources on exit."""
    global _api_client
    if _api_client:
        try:
            _api_client.close()
        except Exception:
            pass


if __name__ == "__main__":
    try:
        main()
    finally:
        cleanup()
