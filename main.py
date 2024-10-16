import asyncio
from hivemind.hivemind_agent import HiveMindAgent

async def main():
    hivemind_agent = HiveMindAgent(workflow_spec_path='workflows/refund_workflow.yaml')
    await hivemind_agent.routine()

if __name__ == "__main__":
    asyncio.run(main())
