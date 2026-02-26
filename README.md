# Bash/Powershell Agent

A lightweight Python project that wraps an LLM-powered chat interface around a restricted Bash/PowerShell environment. The agent is designed to interpret user requests, generate structured tool calls, and safely execute a limited set of shell commands.

---

## Features

- **Interactive chat interface** with the LLM (`LLMChat`) for natural language instructions.
- **Safe command execution** via `Bash.exec_bash_command` with a whitelist of allowed commands.
- **Structured tool calls** that follow an OpenAI-style JSON schema to request command execution.
- **Context tracking** of the working directory (`cwd`) across commands.
- **Configurable model and API endpoints** for plugging into local or remote LLM servers.

## Prerequisites

- Python 3.8+ installed on Windows (PowerShell is used under the hood)
- A running LLM inference server exposing a `/v1/chat/completions` endpoint

## Installation

1. Clone the repository:
   ```powershell
   git clone <repo-url> Bash_Agent
   cd Bash_Agent
   ```

2. Create and activate a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install required packages:
   ```powershell
   pip install -r requirements.txt
   ```

## Configuration

All configuration values live in `src/config.py`:

- `MODEL` & `API_URL`: specify the LLM model and server address.
- `SYSTEM_PROMPT`: initial system message guiding the assistant's behaviour.
- `ALLOWED_COMMANDS`: list of whitelisted shell commands.
- `TOOL_REQUEST_PATTERN`: regex used to pick up tool calls from assistant output.

Adjust these values according to your environment.

## Usage

Run the main interface from the workspace root:

```powershell
python -m src.main
```

You'll see a prompt like:

```
C:\Users\You\Projects\Bash_Agent> User:
```

Type natural language queries. The agent will either respond directly or generate a
`exec_bash_command` tool call. When a command is about to be executed you'll be
asked to confirm.

### Example session

```
C:\...> User: List files in current directory

# Agent returns a tool call, you confirm with "y"
Execute command: ls? (y/n): y
file1.txt
file2.py

C:\...> User: Change directory to src and show contents
...
```

The agent keeps track of `cwd` and prints any stdout/stderr from executed commands.
