import sys
import os

# Add the parent directory of 'swarm' to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pydantic import BaseModel, Field
from hivemind.swarm_agent import SwarmAgent
from typing import Dict, List, Optional
import json
import yaml
import asyncio

class HiveMindAgent(BaseModel):
    """
    The central orchestrator that manages workflows, handles user interactions,
    and delegates tasks to SwarmAgents.
    """
    workflow_spec_path: str = Field(...)
    workflow_spec: Dict = Field(default_factory=dict)
    agents: Dict = Field(default_factory=dict)
    current_step: int = 0
    message_history: List[Dict[str, str]] = []

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data):
        super().__init__(**data)
        # Initialize other attributes or perform other setup here
        print(f"Initialized HiveMindAgent with workflow_spec_path: {self.workflow_spec_path}")
        self.load_workflow_spec()
        print(f"Loaded workflow spec: {self.workflow_spec}")
        self.initialize_agents()

    def load_workflow_spec(self):
        """
        Loads the workflow specification from a JSON or YAML file.
        """
        print(f"Loading workflow spec from: {self.workflow_spec_path}")
        with open(self.workflow_spec_path, 'r') as file:
            self.workflow_spec = yaml.safe_load(file)
        print(f"Workflow spec loaded successfully: {self.workflow_spec}")

    def initialize_agents(self):
        """
        Initializes SwarmAgents based on the workflow specification.
        """
        print("Initializing agents...")
        agents_spec = self.workflow_spec.get('agents', {})
        for agent_name, agent_data in agents_spec.items():
            if agent_name == "IssuesAndRepairsAgent":
                self.agents[agent_name] = SwarmAgent(instructions=agent_data['instructions'])
            elif agent_name == "RefundAgent":
                self.agents[agent_name] = SwarmAgent(instructions=agent_data['instructions'])
        print(f"Initialized agents: {list(self.agents.keys())}")

    async def routine(self):
        """
        Main routine of the HiveMindAgent to execute the workflow.
        """
        print("Executing workflow...")
        steps = self.workflow_spec.get('steps', [])
        for step in steps:
            print(f"Executing step: {step['step_name']}")
            agent_name = step['agent']
            action = step['action']
            requires_input = step.get('requires_user_input', False)
            prompt = step.get('prompt', '')
            user_input = None

            if requires_input:
                user_input = await self.get_user_input_async(prompt)
            
            if 'condition' in step:
                print(f"  Condition: {step['condition']}")

            agent = self.agents.get(agent_name)
            if agent:
                result = await agent.perform_action(action, user_input=user_input)
                print(f"  Result: {result}")
            else:
                print(f"Agent '{agent_name}' not found.")
            print("  Step completed")
        print("Workflow execution completed")

    async def execute_workflow(self):
        """
        Executes the workflow steps sequentially.
        """
        print("Executing workflow...")
        steps = self.workflow_spec.get('steps', [])
        print(f"Workflow steps found: {steps}")
        while self.current_step < len(steps):
            step = steps[self.current_step]
            print(f"Executing step {self.current_step}: {step}")
            agent_name = step.get('agent')
            action = step.get('action')
            requires_input = step.get('requires_user_input', False)
            condition = step.get('condition', None)

            if condition and not self.evaluate_condition(condition):
                print(f"Skipping step {self.current_step} due to condition: {condition}")
                self.current_step += 1
                continue

            if requires_input:
                user_input = self.get_user_input(step.get('prompt', 'Please provide input: '))
            else:
                user_input = None

            agent = self.agents.get(agent_name)
            if agent:
                result = await self.delegate_task(agent, action, user_input)
                self.handle_result(step, result)
            else:
                print(f"Agent '{agent_name}' not found.")
            self.current_step += 1

    async def delegate_task(self, agent: SwarmAgent, action: str, user_input: Optional[str]) -> str:
        """
        Delegates a task to a specified SwarmAgent.
        """
        print(f"Delegating task '{action}' to agent '{agent.name}' with input: {user_input}")
        task_input = {'action': action, 'user_input': user_input}
        result = await agent.routine(task_input)
        print(f"Result from agent '{agent.name}': {result}")
        return result

    def handle_result(self, step: Dict, result: str):
        """
        Handles the result returned by a SwarmAgent.
        """
        print(f"Handling result from {step.get('agent')}: {result}")
        # Store result or update state as needed
        # Implement any conditional logic or workflow branching based on result
        if 'on_success' in step:
            # Implement success handling logic
            pass
        if 'on_failure' in step:
            # Implement failure handling logic
            pass

    def evaluate_condition(self, condition: str) -> bool:
        """
        Evaluates a condition to decide whether to execute a step.
        """
        # Placeholder for condition evaluation logic
        # For now, we'll just return True
        return True

    def get_user_input(self, prompt: str) -> str:
        """
        Gets input from the user when required.
        """
        return input(prompt)

    async def get_user_input_async(self, prompt: str) -> str:
        loop = asyncio.get_event_loop()
        user_input = await loop.run_in_executor(None, input, prompt)
        return user_input
