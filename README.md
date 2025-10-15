Spin up a Docker environment for Python development. 

The default templates spins up two identical environments, one with Jupyter and one without.

## Quick Start (First Time Setup)

### Option 1: Automated Setup (Recommended)

Run the setup script:

```bash
./setup.sh
```

This script will:
- Check if `uv` is installed (with installation instructions if not)
- Initialize the uv project
- Create `pyproject.toml` and `uv.lock` files from `requirements.txt`

After the script completes, start Docker:

```bash
docker-compose up -d
```

### Option 2: Manual Setup

Before starting Docker, you need to initialize the `uv` project and create the required lock files.

#### Step 1: Install uv (if not already installed)

```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using pip
pip install uv
```

#### Step 2: Initialize the uv project

Run the following commands in the project root directory:

```bash
# Initialize a new uv project (if not already initialized)
uv init

# Sync dependencies from requirements.txt to create pyproject.toml and uv.lock
uv add --requirements requirements.txt

# This will create:
# - pyproject.toml (project configuration)
# - uv.lock (locked dependency versions)
```

#### Step 3: Start Docker

Once `pyproject.toml` and `uv.lock` are created, you can build and start the Docker containers:

```bash
docker-compose up -d
```

Or use the Dev Container feature in VS Code to open the project in a container. 
