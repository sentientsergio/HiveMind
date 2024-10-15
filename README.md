# HiveMind

![HiveMind Logo](./assets/hivemind.png)

HiveMind is an extension of [OpenAI's Swarm library](https://github.com/openai/swarm) that introduces a centralized **HiveMindAgent** to orchestrate interactions between multiple specialized **SwarmAgents**. Both the `HiveMindAgent` and `SwarmAgents` are subclasses of the `Agent` class in the OpenAI Swarm library, inheriting and extending its core functionalities.

The `HiveMindAgent` interprets user requests, delegates tasks to `SwarmAgents` based on a machine-readable workflow specification, and integrates their responses to deliver cohesive and efficient outcomes.

## Vision

The vision of HiveMind is to create a flexible and scalable framework for orchestrating complex interactions between AI agents. By leveraging a `HiveMindAgent` that reads machine-readable workflow specifications (in JSON or YAML), HiveMind aims to simplify the development and management of multi-agent systems. This approach enables dynamic task delegation, conditional logic, seamless communication between `SwarmAgents`, and interactive user engagement when needed, making it easier to build sophisticated AI applications adaptable to various requirements.

## Key Concepts

### HiveMindAgent

- **Role**: Acts as the central orchestrator that manages the workflow, handles user interactions, and delegates tasks to `SwarmAgents`.
- **Inheritance**: Subclass of the `Agent` class in the OpenAI Swarm library, extending its capabilities for centralized orchestration.
- **Responsibilities**:
  - Interpret user requests and determine the appropriate workflow.
  - Read and parse the workflow specification.
  - Invoke `SwarmAgents` as per the workflow, providing them with necessary context and objectives.
  - Handle responses from `SwarmAgents`, including processing any requests for additional user input.
  - Maintain and manage the conversation context.
  - Aggregate responses from `SwarmAgents` and present the final result to the user.

### SwarmAgents

- **Role**: Specialized agents that perform designated tasks within the workflow.
- **Inheritance**: Subclasses of the `Agent` class in the OpenAI Swarm library, tailored for specific functionalities within HiveMind.
- **Characteristics**:
  - Designed to handle specific functions or expertise areas.
  - Operate based on the prompts and context provided by the `HiveMindAgent`.
  - Can request additional user input by signaling the need in their response to the `HiveMindAgent`.
  - Do not interact directly with the user unless specified through the workflow.

### Workflow Specification

- **Format**: Defined in JSON or YAML.
- **Contents**:
  - **Agents**: Definitions of all `SwarmAgents` involved, including their roles and initialization parameters.
  - **Workflow Steps**: A sequence outlining the invocation of `SwarmAgents`, actions to perform, and control flow.
  - **Conditions**: Logic to determine the flow between steps based on `SwarmAgent` responses.
  - **User Input Handling**: Instructions for obtaining additional user input when requested by `SwarmAgents`.

## Workflow Example (Conceptual)

1. **User Interaction**:

   - The user submits a request to the `HiveMindAgent`.

2. **Task Delegation**:

   - The `HiveMindAgent` identifies the appropriate `SwarmAgent` to handle the initial task based on the workflow specification.

3. **Agent Processing**:

   - The `SwarmAgent` processes the task and returns a response to the `HiveMindAgent`.
   - If the `SwarmAgent` requires additional user input, it indicates this in its response to the `HiveMindAgent`.

4. **User Input Handling**:

   - Upon receiving a prompt for user input, the `HiveMindAgent` interacts with the user to gather the required information.
   - The `HiveMindAgent` then provides this input to the requesting `SwarmAgent`, which proceeds with its task based on the new information.

5. **Workflow Progression**:

   - Based on the `SwarmAgent`'s response and any conditional logic in the workflow, the `HiveMindAgent` determines the next steps.
   - This could involve invoking another `SwarmAgent`, looping back for revisions, or concluding the workflow.

6. **Result Compilation**:
   - The `HiveMindAgent` aggregates the responses from all involved `SwarmAgents`.
   - Presents a comprehensive outcome to the user.

## Requirements

### Functional Requirements

- **HiveMindAgent Functionality**:

  - Must accept user requests and parse them to determine the required workflow.
  - Should read a machine-readable specification (JSON or YAML) that defines the workflow, `SwarmAgents` involved, and the sequence of actions.
  - Must invoke `SwarmAgents` based on the workflow specification.
  - Should process and evaluate responses from `SwarmAgents` to make decisions on subsequent actions, including conditional logic and looping.
  - Must maintain the conversation context and provide relevant parts to each `SwarmAgent` as needed.
  - Should collect and aggregate responses from all `SwarmAgents` to present a final result to the user.
  - **User Interaction Handling**:
    - If a `SwarmAgent` requires additional user input, it indicates this need in its response to the `HiveMindAgent`.
    - When prompted to seek additional input, the `HiveMindAgent` will interact with the user, gather the required information, and provide it to the requesting `SwarmAgent` before proceeding with the workflow.

- **SwarmAgent Functionality**:

  - Must perform specific tasks as directed by the `HiveMindAgent`.
  - Should accept prompts and context from the `HiveMindAgent` and return responses accordingly.
  - May determine the need for additional user input and signal this in the response to the `HiveMindAgent`.
  - Must be designed to handle tasks without direct user interaction unless specified through the `HiveMindAgent`.

- **Workflow Specification**:

  - The system must support workflows defined in JSON or YAML format.
  - The specification should include:
    - **SwarmAgents involved**: Their identifiers, roles, and any initialization parameters.
    - **Sequence of SwarmAgent invocations**: The order in which `SwarmAgents` are to be invoked.
    - **Conditional logic**: Conditions under which certain `SwarmAgents` are invoked or skipped.
    - **Data flow**: Parameters and context to be passed between `SwarmAgents`.
    - **Looping and Iteration**: Instructions for repeating steps based on conditions.
    - **User Input Requests**: Instructions for handling situations where additional user input is required by `SwarmAgents`.

- **Context Management**:

  - The system must maintain a conversation history that includes all interactions between the `HiveMindAgent` and `SwarmAgents`.
  - Each `SwarmAgent` invocation should include the relevant context to perform its task effectively.
  - All `SwarmAgents` have access to the cumulative conversation context to ensure consistency.

- **Workflow Flexibility**:

  - The system should allow for `SwarmAgents` to be invoked multiple times or skipped based on the `HiveMindAgent`'s decisions and workflow conditions.
  - Should support looping back to previous `SwarmAgents` for revisions or additional input.
  - Must handle dynamic adjustments in the workflow, such as incorporating new user input when required.

- **Extensibility**:
  - The framework should be designed to easily add new `SwarmAgents` and workflows by updating the workflow specification without altering the codebase.
  - `SwarmAgents` should be modular and encapsulated to promote reusability.

### Non-Functional Requirements

- **Performance**:

  - The system should handle agent interactions efficiently to minimize latency.
  - Should manage resources effectively to handle complex workflows.

- **Scalability**:

  - The architecture should support scaling to include more `SwarmAgents` and complex workflows without significant refactoring.

- **Reliability**:

  - Must ensure that conversation context is consistently maintained and accurately passed between agents.
  - Should handle exceptions and errors gracefully, providing meaningful feedback to the `HiveMindAgent` for decision-making.
  - Must ensure that user input is correctly obtained and integrated into the workflow when requested.

- **Usability**:

  - The system should provide clear and coherent outputs to the user, abstracting the complexity of `SwarmAgent` interactions.
  - Workflow specifications should be user-friendly, allowing easy modification and creation of workflows.
  - Should facilitate easy understanding of how `SwarmAgents` interact within a workflow without relying on enumerated agent examples.

- **Security**:
  - Must ensure that sensitive data within the conversation context is protected.
  - Should enforce access controls where appropriate between `SwarmAgents`.

## Future Extensions

While the initial MVP focuses on the core functionality of orchestrating `SwarmAgents` through a `HiveMindAgent` using workflow specifications, future enhancements may include:

- **Advanced Decision-Making**: Incorporating more sophisticated logic within the `HiveMindAgent` for complex workflows.
- **Parallel Processing**: Enabling the `HiveMindAgent` to invoke multiple `SwarmAgents` concurrently when tasks can be parallelized.
- **User Feedback Loop**: Providing mechanisms for users to give feedback on `SwarmAgent` performance to refine the system.
- **Graphical Workflow Editor**: Developing tools to visually design and edit workflow specifications.
- **Dynamic Workflow Modification**: Allowing workflows to be modified in real-time based on evolving requirements or user inputs.

## Getting Started

_Instructions on how to install and use the HiveMind MVP will be provided in future updates._

## Contributing

Contributions to HiveMind are welcome. Please follow the contribution guidelines (to be provided) for submitting issues and pull requests.

## License

HiveMind is released under the MIT License.

---

_Note: This README outlines the vision and requirements for the first MVP of the HiveMind framework. Implementation details, code examples, and detailed documentation will be developed in subsequent stages._
