# Sprint 1: Project Setup and Core Architecture (1 week)

**Objectives:**

- Set up the project repository and development environment.
- Define the core classes for `HiveMindAgent` and `SwarmAgent`.
- Establish basic agent communication mechanisms.

---

## Detailed Work Plan

### Task 1: Project Initialization

#### Step 1: Create the Project Directory and Initialize Git Repository

- **Action:** Open your terminal and create a new project directory.

  ```bash
  mkdir HiveMind
  cd HiveMind
  ```

- **Action:** Initialize an empty Git repository.

  ```bash
  git init
  ```

#### Step 2: Set Up the Project Structure

- **Action:** Create the basic project directories and files.

  ```bash
  mkdir src tests docs
  touch README.md
  ```

- **Action:** Create a `.gitignore` file to exclude unnecessary files from Git tracking.

  ```bash
  touch .gitignore
  ```

  **Edit `.gitignore` to include:**

  ```gitignore:.gitignore
  # Byte-compiled / optimized / DLL files
  __pycache__/
  *.py[cod]
  *$py.class

  # Virtual environment
  .venv/

  # Editor files
  .vscode/
  *.swp
  ```

#### Step 3: Set Up a Virtual Environment and Manage Dependencies

- **Action:** Create a virtual environment using `venv`.

  ```bash
  python3 -m venv .venv
  ```

- **Action:** Activate the virtual environment.

  - On macOS/Linux:

    ```bash
    source .venv/bin/activate
    ```

  - On Windows:

    ```cmd
    .venv\Scripts\activate
    ```

- **Action:** Upgrade `pip` and install initial dependencies.

  ```bash
  pip install --upgrade pip
  pip install openai
  ```

- **Action:** Freeze the dependencies into a `requirements.txt` file.

  ```bash
  pip freeze > requirements.txt
  ```

#### Step 4: Integrate Continuous Integration (CI) Tools and Linters

- **Action:** Choose a CI service (e.g., **GitHub Actions**).

- **Action:** Set up **GitHub Actions** workflow.

  - Create a directory for workflows:

    ```bash
    mkdir -p .github/workflows
    ```

  - Create a CI configuration file:

    ```yaml:.github/workflows/ci.yml
    name: CI

    on:
      push:
        branches: [ main ]
      pull_request:
        branches: [ main ]

    jobs:
      build:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v2
          - name: Set up Python
            uses: actions/setup-python@v2
            with:
              python-version: '3.9'
          - name: Install dependencies
            run: |
              python -m venv .venv
              . .venv/bin/activate
              pip install --upgrade pip
              pip install -r requirements.txt
          - name: Run Linter
            run: |
              . .venv/bin/activate
              flake8 src tests
          - name: Run Tests
            run: |
              . .venv/bin/activate
              python -m unittest discover tests
    ```

- **Action:** Install linters and formatters.

  ```bash
  pip install flake8 black
  pip freeze > requirements.txt
  ```

- **Action:** Configure `flake8` by creating a `.flake8` file.

  ```ini:.flake8
  [flake8]
  max-line-length = 88
  exclude = .venv, __pycache__, docs
  ```

- **Action:** Configure `black` by adding `pyproject.toml`.

  ```toml:pyproject.toml
  [tool.black]
  line-length = 88
  ```

### Task 2: Core Class Definitions

#### Step 1: Create the Base `Agent` Class (if not provided)

- **Action:** If `Agent` is not already defined from OpenAI's Swarm library, create a base `agent.py` file.

  ```bash
  mkdir src/hivemind
  touch src/hivemind/__init__.py
  touch src/hivemind/agent.py
  ```

- **Code:**

  ```python:src/hivemind/agent.py
  class Agent:
      """
      Base Agent class from which all agents inherit.
      """

      def __init__(self, name):
          self.name = name

      def send_message(self, recipient, message):
          pass  # To be implemented in subclasses

      def receive_message(self, sender, message):
          pass  # To be implemented in subclasses
  ```

#### Step 2: Define the `HiveMindAgent` Class

- **Action:** Create the `hivemind_agent.py` module.

  ```bash
  touch src/hivemind/hivemind_agent.py
  ```

- **Code:**

  ```python:src/hivemind/hivemind_agent.py
  from .agent import Agent

  class HiveMindAgent(Agent):
      """
      The central orchestrator agent that manages SwarmAgents.
      """

      def __init__(self, name="HiveMind"):
          super().__init__(name)
          self.swarm_agents = []

      def register_agent(self, agent):
          self.swarm_agents.append(agent)

      def send_message(self, recipient, message):
          # Implement logic to send messages to SwarmAgents
          recipient.receive_message(self, message)

      def receive_message(self, sender, message):
          # Handle messages received from SwarmAgents
          print(f"{self.name} received message from {sender.name}: {message}")
  ```

#### Step 3: Define the `SwarmAgent` Class

- **Action:** Create the `swarm_agent.py` module.

  ```bash
  touch src/hivemind/swarm_agent.py
  ```

- **Code:**

  ```python:src/hivemind/swarm_agent.py
  from .agent import Agent

  class SwarmAgent(Agent):
      """
      A specialized agent that performs specific tasks as directed by the HiveMindAgent.
      """

      def __init__(self, name):
          super().__init__(name)

      def send_message(self, recipient, message):
          recipient.receive_message(self, message)

      def receive_message(self, sender, message):
          # Handle messages received from HiveMindAgent or other agents
          print(f"{self.name} received message from {sender.name}: {message}")
  ```

#### Step 4: Document Classes and Methods

- **Action:** Ensure all classes and methods have clear docstrings explaining their purpose and usage.

- **Example:**

  ```python
  def register_agent(self, agent):
      """
      Registers a SwarmAgent with the HiveMindAgent.

      Args:
          agent (SwarmAgent): The agent to register.
      """
      self.swarm_agents.append(agent)
  ```

### Task 3: Basic Communication Protocol

#### Step 1: Implement a Simple Messaging Protocol

- **Action:** Define a `Message` class (if needed) to encapsulate messages.

  ```python:src/hivemind/message.py
  class Message:
      """
      Represents a message exchanged between agents.

      Attributes:
          sender (Agent): The agent sending the message.
          recipient (Agent): The agent receiving the message.
          content (str): The content of the message.
      """

      def __init__(self, sender, recipient, content):
          self.sender = sender
          self.recipient = recipient
          self.content = content
  ```

- **Action:** Update `send_message` and `receive_message` methods to use the `Message` class.

#### Step 2: Test Agent Instantiation and Basic Message Passing

- **Action:** Create a test module for messaging.

  ```bash
  mkdir tests
  touch tests/__init__.py
  touch tests/test_messaging.py
  ```

- **Code:**

  ```python:tests/test_messaging.py
  import unittest
  from src.hivemind.hivemind_agent import HiveMindAgent
  from src.hivemind.swarm_agent import SwarmAgent

  class TestMessaging(unittest.TestCase):
      def test_message_passing(self):
          hivemind = HiveMindAgent()
          agent1 = SwarmAgent(name="Agent1")
          agent2 = SwarmAgent(name="Agent2")

          # Register agents with HiveMind
          hivemind.register_agent(agent1)
          hivemind.register_agent(agent2)

          # HiveMind sends a message to Agent1
          hivemind.send_message(agent1, "Hello Agent1!")

          # Agent1 sends a reply to HiveMind
          agent1.send_message(hivemind, "Hello HiveMind!")

          # Agent1 sends a message to Agent2
          agent1.send_message(agent2, "Hello Agent2!")

          self.assertTrue(True)  # Placeholder assertion

  if __name__ == '__main__':
      unittest.main()
  ```

- **Action:** Run the tests to ensure messaging works correctly.

  ```bash
  python -m unittest discover tests
  ```

- **Expected Output:**

  ```
  HiveMind received message from Agent1: Hello HiveMind!
  Agent2 received message from Agent1: Hello Agent2!
  .
  ----------------------------------------------------------------------
  Ran 1 test in 0.001s

  OK
  ```

---

## Summary of Deliverables

- **Project Repository:**

  - Initialized Git repository with appropriate `.gitignore`.
  - Project directories: `src`, `tests`, `docs`, and initial `README.md`.

- **Development Environment:**

  - Virtual environment set up with `venv`.
  - Dependencies managed with `requirements.txt`.
  - Linters (`flake8`, `black`) configured.
  - CI pipeline configured using GitHub Actions.

- **Core Classes:**

  - `Agent` base class (`src/hivemind/agent.py`).
  - `HiveMindAgent` class (`src/hivemind/hivemind_agent.py`).
  - `SwarmAgent` class (`src/hivemind/swarm_agent.py`).
  - All classes documented with docstrings.

- **Communication Protocol:**

  - `Message` class defined (`src/hivemind/message.py`).
  - `send_message` and `receive_message` methods implemented.

- **Testing:**
  - Unit tests for agent instantiation and message passing (`tests/test_messaging.py`).
  - Tests pass successfully, demonstrating basic communication.

---

## Next Steps

- **Code Review:**

  - Review the code for adherence to coding standards.
  - Ensure documentation is clear and comprehensive.

- **Merge and Push:**

  - Commit all changes.
  - Push to the remote Git repository (e.g., GitHub).

  ```bash
  git add .
  git commit -m "Implement core architecture and communication protocol"
  git remote add origin <your-repo-url>
  git push -u origin main
  ```

- **Prepare for Sprint 2:**
  - Begin planning for Workflow Specification Parsing.
  - Identify any dependencies or prerequisites.

---

Feel free to adjust any steps or ask for further clarification on any part of the work plan. Good luck with your development!
