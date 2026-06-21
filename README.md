## Day 1
1. Install and setup Git and UV.
2. Decide the base outline of the architecture of the application.
3. Create the folder structure for the decided architecture.
4. Create and store the necessary environmental variables in the .env file.

### Starting a new Project
1. Install git in the system if not installed yet.
2. Install UV in the system if not installed yet.
3. Create a repo using UV. 

        uv init repo_name

4. Connect it with the remote GitHub.
    
        git remote add origin remote_repo_http_link

5. Do the 1st add and commit.

    - git add .
    - git commit -m "some meaningful message"
    
    _[
        From 2nd commit onwards, add and commit could be combined as a single command. Remember : Whenever a new file is created, git add . must be used as such. Commit -a will only consider files which were already present before.
            
            git add -a -m "some meaningful message"
    ]_

6. Instead of mentioning the branch name every time, 
    - Option 1) Use default current.

            git config --global push

    This tells Git:
        
    "Push the current branch to a branch with the same name on remote"

    - Option 2) Set upstream
        
            git push -u origin repo_name

    _[
        To remove upstream tracking,
            git branch --unset-upstream
    ]_
7. Git push if not pushed. It using option 2, No need to mention repo name as the previous command will handle that.
    
        git push

8. Create and Use Virtual Environment
    1.  Create venv
            
            uv venv

    2.  Activate
        - Windows
            
                .venv\Scripts\activate

        - Linux/macOS
                
                source .venv/bin/activate
9. Install libraries
    
        uv add library_name

_[
    To uninstall libraries,
        uv remove library_name
]_

10. Set up environment.
    1. Create .env file and store all environment variables and keys in it.
    2. Load the .env
        ```python
        from dotenv import load_dotenv
        load_dotenv()
        ```
    3. Verify via printing and checking (Just the 1st time only)
        ```python
        print(os.environ)
        ```
11. Run Python Using UV
    1. Normal python script

            uv run file_name.py
    2. FastAPI
       
            uv run uvicorn file_name:app --reload

    [
        To Install From Existing Project

                1. git clone  remote_repo_http_link
                2. cd repo_name
                3. uv sync
    ]



    

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
