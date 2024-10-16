from swarm import Agent
from typing import Dict, Optional

class SwarmAgent(Agent):
    """
    A specialized agent that performs specific tasks as directed by the HiveMindAgent.
    """

    async def perform_action(self, action: str, user_input: Optional[str] = None) -> str:
        """
        Performs the action specified in the task_input.
        """
        method = getattr(self, action, self.action_not_found)
        result = await method(user_input)
        return result

    async def action_not_found(self, user_input: Optional[str]) -> str:
        """
        Default method when the action is not found.
        """
        return "Action not recognized."

    # Example action methods
    async def collect_issue_details(self, user_input: Optional[str]) -> str:
        """
        Collects issue details from the user.
        """
        if user_input:
            issue_details = f"Collected issue details: {user_input}"
        else:
            issue_details = "No issue details provided."
        return issue_details

    async def propose_fix(self, user_input: Optional[str]) -> str:
        """
        Proposes a fix to the user's issue.
        """
        fix = "Based on the issue, we recommend restarting the device."
        return fix

    async def offer_refund(self, user_input: Optional[str]) -> str:
        """
        Offers a refund to the user.
        """
        refund_message = "We have processed your refund."
        return refund_message

    async def process_refund(self, user_input: Optional[str]) -> str:
        """
        Processes the refund after user confirmation.
        """
        if user_input and user_input.lower() in ['yes', 'y']:
            confirmation = "Refund processed successfully."
        else:
            confirmation = "Refund process cancelled."
        return confirmation

    # Additional actions can be implemented as needed
