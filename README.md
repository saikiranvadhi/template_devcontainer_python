Spin up a Docker environment for Python development. 

The default templates spins up two identical environments, one with Jupyter and one without.

## Quick Start (First Time Setup)

Run the setup script:

```bash
./setup.sh
```

This script will:
- Check if `uv` is installed (with installation instructions if not)
- Initialize the uv project
- Create `pyproject.toml` and `uv.lock` files from `requirements.txt`

#### Manual process:
After the script completes, start Docker:

```bash
docker-compose up -d
```
Or use the Dev Container feature in VS Code to open the project in a container. 


## SQL Usage

To connect to SQL Server from python docker container, use the following command:
```bash
mysql -h mysql_server -P ${MYSQL_PORT} -u ${MYSQL_USER} -p${MYSQL_PASSWORD} ${MYSQL_DATABASE}
```