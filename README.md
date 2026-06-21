## Day 1
1. Install and setup Git and UV.
2. Decide the base outline of the architecture of the application.
3. Create the folder structure for the decided architecture.
4. Create and store the necessary environmental variables in the .env file.


### Using .env Files in Python
Environment variables are essential for separating sensitive configuration data (like API keys, database URLs, etc.) from your codebase. The .env file is a simple way to manage these values during development. This document explains how to use .env files in Python with the python-dotenv package.

#### What is a .env File?
A .env file is a plaintext file containing key-value pairs representing environment variables. These are used to configure an application without hardcoding values in the source code.

#### Example .env file:

    API_KEY=abc123
    DEBUG=True
    DATABASE_URL=postgres://user:pass@localhost:5432/mydb

#### Why Use .env Files?

- Security: Keep secrets (like API keys) out of version control.
- Portability: Share only required environment settings using a .env.example file.
- Configurability: Easily switch between environments (development, testing, production).

#### Step-by-Step Guide
##### 1. Install python-dotenv
To get started, install the package:

    pip install python-dotenv

##### 2. Create a .env File
Add a .env file to your project root:

    API_KEY=abc123
    
    DEBUG=True

    DATABASE_URL=postgres://user:pass@localhost:5432/mydb

    PORT=8080

__Note: Never commit your .env file to version control. Add it to .gitignore:
.env__

##### 3. Load Environment Variables in Python
Use load_dotenv() to read the file:
```python
from dotenv import load_dotenv
import os
load_dotenv()  # Loads the .env file automatically
api_key = os.getenv("API_KEY")
debug_mode = os.getenv("DEBUG")
db_url = os.getenv("DATABASE_URL")
port = os.getenv("PORT")
print("API Key:", api_key)
print("Debug Mode:", debug_mode)
print("Database URL:", db_url)
print("Port:", port)
```

##### 4. Type Conversion
All values are strings by default. Convert them as needed:
```python
debug = os.getenv("DEBUG", "False").lower() == "true"
port = int(os.getenv("PORT", 8000))
```
#### Advanced Usage

##### Load from a Custom Path

If your .env file is not in the root directory:
```python
from dotenv import load_dotenv
from pathlib import Path
env_path = Path("config/.env.dev")
load_dotenv(dotenv_path=env_path)
```
##### Access with os.environ

You can also use os.environ if you're sure the variable exists:
```python
api_key = os.environ["API_KEY"]  # Raises KeyError if not found
```
#### Using .env.example

Create a .env.example to document the required environment variables:

    API_KEY=your_api_key_here
    DEBUG=True
    DATABASE_URL=your_database_url
    PORT=8000

### Best Practices
- Use .env only for non-sensitive dev/local configs. Use cloud-based secrets management for production (e.g., AWS Secrets Manager).
- Avoid global mutable access. Instead, use a config class or function to encapsulate access to environment variables.
- Use default fallbacks in your os.getenv() calls.

### Integration with Popular Frameworks
- FastAPI/Flask: Load .env before initializing the app.
- LangGraph: Use .env to manage credentials, model configs, and tool endpoints.
- Docker: Use --env-file .env to pass values when running containers.

### Summary
    Step	Action

    1	Install python-dotenv
    2	Create a .env file
    3	Load it using load_dotenv()
    4	Access values using os.getenv()
    5	Convert types as necessary

Using .env files in Python is a clean, safe, and effective way to manage configuration. For any production use, combine this with secure secrets management systems.
