# Complete Module Code

**File: Symposium/.gitignore**

*\# Python virtual environment*

symposium_env/

*\# API keys*

.env

*\# Python cache files*

\_\_pycache\_\_/

\*.pyc

**File: Symposium/publish.bat**

@**echo** off

*REM =================================================================*

*REM == Publishes The Symposium to GitHub and Google Drive ==*

*REM =================================================================*

*REM Change the current directory to the script\'s directory.*

**cd** /d \"%\~dp0\"

*REM Prompt for a commit message*

**echo**.

**set** **/p** commitMessage=\"Enter a commit message for this update:
\"

*REM =================================================================*

**echo**.

**echo** \[STEP 1\] Pushing changes to GitHub\...

*REM Add all changes to the staging area*

git add .

*REM Commit the changes with the provided message*

git commit -m \"%commitMessage%\"

*REM Push the commit to the \'main\' branch on the remote \'origin\'*

git push origin main

**echo**.

**echo** GitHub push complete.

**echo**
=================================================================

**echo**.

**echo** \[STEP 2\] Syncing project to Google Drive\...

**echo** Excluding .env, .git, \_\_pycache\_\_, and symposium_env\...

rclone sync . \"gdrive:Symposium\" \--exclude \"/symposium_env/\*\*\"
\--exclude \"/.git/\*\*\" \--exclude \"/\_\_pycache\_\_/\*\*\"
\--exclude \".env\" \--progress

**echo**.

**echo** Google Drive sync complete.

**echo**
=================================================================

**echo**.

**echo** PUBLISH COMPLETE - CONTEXT IS NOW SHARED

**echo**
=================================================================

**pause**

**File: Symposium/run.bat**

@**echo** off

*REM =================================================================*

*REM == Runner for The Multi-LLM Symposium ==*

*REM =================================================================*

*REM Change the current directory to the script\'s directory.*

**cd** /d \"%\~dp0\"

**echo** \[STEP 1\] Activating virtual environment\...

**call** \"symposium_env\\Scripts\\activate.bat\"

**echo**.

**echo** \[STEP 2\] Executing the Python script\...

python src/symposium_manager_v2.py

**echo**.

**echo**
=================================================================

**echo** == SCRIPT FINISHED ==

**echo**
=================================================================

**pause**

**File: Symposium/src/models/agent.py**

*\"\"\"*

*Core Agent model with LLM provider integration.*

*Contains Agent class, provider enums, and model factory logic.*

*\"\"\"*

**import** **os**

**from** **dataclasses** **import** dataclass, field

**from** **typing** **import** List, Optional, Any

**from** **enum** **import** Enum

**from** **dotenv** **import** load_dotenv

*\# LangChain LLM Provider imports*

**from** **langchain_anthropic** **import** ChatAnthropic

**from** **langchain_google_genai** **import** ChatGoogleGenerativeAI

**from** **langchain_groq** **import** ChatGroq

**from** **langchain_mistralai** **import** ChatMistralAI

**from** **langchain_cerebras** **import** ChatCerebras

**from** **langchain_core.tools** **import** Tool

*\# Load environment variables*

load_dotenv()

**class** **ModelProvider**(Enum):

*\"\"\"Enumeration of supported LLM providers.\"\"\"*

GEMINI = \"gemini\"

CLAUDE = \"claude\"

GROQ = \"groq\"

MISTRAL = \"mistral\"

CEREBRAS = \"cerebras\"

**class** **AgentTier**(Enum):

*\"\"\"Classification of agent capability and cost.\"\"\"*

SENIOR_FELLOW = \"senior_fellow\" *\# Premium models for complex
reasoning*

RESEARCH_ASSISTANT = \"research_assistant\" *\# Cheaper models for tool
use*

\@dataclass

**class** **Agent**:

*\"\"\"Represents a configured LLM agent with specific
capabilities.\"\"\"*

name: str

provider: ModelProvider

model_name: str

tier: AgentTier

persona_prompt: str

tools: List\[Tool\] = field(default_factory=list)

temperature: float = 0.0

model_instance: Optional\[Any\] = field(default=**None**,
init=**False**)

**def** \_\_post_init\_\_(self):

*\"\"\"Initialize the actual LLM instance after dataclass
creation.\"\"\"*

self.model_instance = self.\_create_model_instance()

**def** \_create_model_instance(self) -\> Any:

*\"\"\"Factory method to create the appropriate LLM instance.\"\"\"*

**try**:

**if** self.provider == ModelProvider.GEMINI:

**return** ChatGoogleGenerativeAI(

model=self.model_name,

temperature=self.temperature

)

**elif** self.provider == ModelProvider.CLAUDE:

**return** ChatAnthropic(

model=self.model_name,

temperature=self.temperature

)

**elif** self.provider == ModelProvider.GROQ:

**return** ChatGroq(

model_name=self.model_name,

temperature=self.temperature

)

**elif** self.provider == ModelProvider.MISTRAL:

**return** ChatMistralAI(

model_name=self.model_name,

temperature=self.temperature

)

**elif** self.provider == ModelProvider.CEREBRAS:

**return** ChatCerebras(

model=self.model_name,

temperature=self.temperature

)

**else**:

**raise** **ValueError**(f\"Unsupported provider:
**{**self.provider**}**\")

**except** **Exception** **as** e:

print(f\"Error creating model instance for **{**self.name**}**:
**{**e**}**\")

**return** **None**

**File: Symposium/src/models/symposium.py**

*\"\"\"*

*Agent registry and symposium management.*

*Handles agent creation, registration, and retrieval.*

*\"\"\"*

**from** **typing** **import** Dict, List, Optional

**from** **.agent** **import** Agent, ModelProvider, AgentTier

**class** **Symposium**:

*\"\"\"Main class for managing the agent registry and their
relationships.\"\"\"*

**def** \_\_init\_\_(self):

self.agents: Dict\[str, Agent\] = {}

self.\_initialize_default_agents()

**def** \_initialize_default_agents(self) -\> **None**:

*\"\"\"Create the standard agent roster based on verified
providers.\"\"\"*

*\# Senior Fellows (premium models)*

self.register_agent(Agent(

name=\"Gemini\",

provider=ModelProvider.GEMINI,

model_name=\"gemini-2.5-pro\",

tier=AgentTier.SENIOR_FELLOW,

persona_prompt=\"You are Gemini, a visionary Senior Fellow. Your role is
strategic thinking, creative problem-solving, and comprehensive
analysis.\"

))

self.register_agent(Agent(

name=\"Claude\",

provider=ModelProvider.CLAUDE,

model_name=\"claude-sonnet-4-20250514\",

tier=AgentTier.SENIOR_FELLOW,

persona_prompt=\"You are Claude, a analytical Senior Fellow. Your role
is critical evaluation, logical reasoning, and identifying potential
flaws.\"

))

*\# Research Assistants (tool-using models)*

self.register_agent(Agent(

name=\"Groq_Assistant\",

provider=ModelProvider.GROQ,

model_name=\"llama-3.3-70b-versatile\",

tier=AgentTier.RESEARCH_ASSISTANT,

persona_prompt=\"You are a Research Assistant. Your role is to execute
specific tasks using tools and provide concise, factual results.\"

))

self.register_agent(Agent(

name=\"Mistral_Assistant\",

provider=ModelProvider.MISTRAL,

model_name=\"mistral-large-latest\",

tier=AgentTier.RESEARCH_ASSISTANT,

persona_prompt=\"You are a Research Assistant specialized in analysis
and synthesis of information from multiple sources.\"

))

self.register_agent(Agent(

name=\"Cerebras_Assistant\",

provider=ModelProvider.CEREBRAS,

model_name=\"llama-3.3-70b\",

tier=AgentTier.RESEARCH_ASSISTANT,

persona_prompt=\"You are a fast Research Assistant optimized for quick
responses and straightforward task execution.\"

))

**def** register_agent(self, agent: Agent) -\> **None**:

*\"\"\"Add an agent to the registry.\"\"\"*

**if** agent.model_instance **is** **None**:

print(f\"Warning: Agent **{**agent.name**}** failed to initialize\")

**return**

self.agents\[agent.name\] = agent

print(f\"Registered agent: **{**agent.name**}**
(**{**agent.provider.value**}**)\")

**def** get_agent_registry(self) -\> Dict\[str, Agent\]:

*\"\"\"Return the complete agent registry.\"\"\"*

**return** self.agents.copy()

**def** get_agent(self, name: str) -\> Optional\[Agent\]:

*\"\"\"Retrieve a specific agent by name.\"\"\"*

**return** self.agents.get(name)

**def** list_agents_by_tier(self, tier: AgentTier) -\> List\[Agent\]:

*\"\"\"Get all agents of a specific tier.\"\"\"*

**return** \[agent **for** agent **in** self.agents.values() **if**
agent.tier == tier\]

**File: Symposium/src/models/workflow.py**

*\"\"\"*

*LangGraph workflow management with provider-specific handling.*

*Contains workflow creation logic and execution state management.*

*\"\"\"*

**from** **dataclasses** **import** dataclass, field

**from** **typing** **import** Dict, List, Any, Optional

**from** **typing_extensions** **import** Annotated

**from** **langgraph.graph.message** **import** add_messages

**from** **langgraph.graph** **import** StateGraph, END

**from** **langchain_core.messages** **import** BaseMessage,
HumanMessage, AIMessage, ToolMessage

**from** **langchain_core.tools** **import** Tool

**from** **.agent** **import** Agent, AgentTier

**from** **.tools.calculator** **import** create_calculator_tool

**from** **.tools.python_executor** **import**
create_python_executor_tool

\@dataclass

**class** **GraphState**:

*\"\"\"State object that flows through LangGraph workflows.\"\"\"*

messages: Annotated\[List\[BaseMessage\], add_messages\]

current_agent: Optional\[str\] = **None**

task_context: Optional\[str\] = **None**

metadata: Dict\[str, Any\] = field(default_factory=dict)

**class** **WorkflowManager**:

*\"\"\"Manages LangGraph workflow creation and execution.\"\"\"*

**def** create_tool_agent_graph(self, agent: Agent, tools:
Optional\[List\[Tool\]\] = **None**) -\> StateGraph:

*\"\"\"Create a LangGraph workflow for a tool-using agent.\"\"\"*

**if** tools **is** **None** **and** agent.tier ==
AgentTier.RESEARCH_ASSISTANT:

tools = \[create_calculator_tool(), create_python_executor_tool()\]

**elif** tools **is** **None**:

tools = \[\]

*\# Bind tools to the agent\'s model instance*

**if** tools:

model_with_tools = agent.model_instance.bind_tools(tools)

**else**:

model_with_tools = agent.model_instance

**def** agent_node(state: GraphState) -\> Dict\[str, Any\]:

*\"\"\"Node function for the tool-using agent.\"\"\"*

*\# Construct system message with persona*

system_message = HumanMessage(content=agent.persona_prompt)

*\# Get all messages including system context*

messages = \[system_message\] + state.messages

print(f\"\-\-- Calling **{**agent.name**}** \-\--\")

response = model_with_tools.invoke(messages)

print(f\"\-\-- Response from **{**agent.name**}**:
**{**response.content\[:100\]**}**\... \-\--\")

**return** {

\"messages\": \[response\],

\"current_agent\": agent.name

}

**def** should_continue(state: GraphState) -\> str:

*\"\"\"Determine if the agent should use tools or finish.\"\"\"*

last_message = state.messages\[-1\]

*\# Check if the last message has tool calls*

**if** hasattr(last_message, \'tool_calls\') **and**
last_message.tool_calls:

**return** \"tools\"

**else**:

**return** \"end\"

**def** tool_node(state: GraphState) -\> Dict\[str, Any\]:

*\"\"\"Execute tool calls and return results.\"\"\"*

last_message = state.messages\[-1\]

tool_calls = last_message.tool_calls

tool_messages = \[\]

current_agent_name = state.current_agent

**for** tool_call **in** tool_calls:

tool_name = tool_call\[\"name\"\]

tool_call_id = tool_call\[\"id\"\]

*\# Handle different parameter key formats across providers*

parameter_container = tool_call.get(\"parameters\") **or**
tool_call.get(\"args\")

**if** **not** parameter_container:

result = f\"Error: No parameters found in tool call\"

**else**:

tool_to_use = **None**

**for** tool **in** tools:

**if** tool.name == tool_name:

tool_to_use = tool

**break**

**if** tool_to_use:

**try**:

**if** \"\_\_arg1\" **in** parameter_container:

result = tool_to_use.func(parameter_container\[\"\_\_arg1\"\])

**else**:

result = tool_to_use.func(\*\*parameter_container)

**except** **Exception** **as** e:

result = f\"Error: **{**str(e)**}**\"

**else**:

result = f\"Error: Tool \'**{**tool_name**}**\' not found\"

*\# Apply Cerebras-specific workaround*

**if** current_agent_name == \"Cerebras_Assistant\":

*\# Cerebras doesn\'t handle ToolMessage objects properly*

tool_messages.append(

HumanMessage(content=f\"Tool \'**{**tool_name**}**\' returned the
result: **{**result**}**\", name=tool_name)

)

**else**:

*\# Standard ToolMessage format for other providers*

tool_messages.append(

ToolMessage(content=str(result), tool_call_id=tool_call_id)

)

**return** {\"messages\": tool_messages}

*\# Build the graph*

workflow = StateGraph(GraphState)

workflow.add_node(\"agent\", agent_node)

workflow.add_node(\"tools\", tool_node)

workflow.set_entry_point(\"agent\")

workflow.add_conditional_edges(

\"agent\",

should_continue,

{\"tools\": \"tools\", \"end\": END}

)

*\# Cerebras requires different workflow termination*

**if** agent.name == \"Cerebras_Assistant\":

workflow.add_edge(\"tools\", END)

**else**:

workflow.add_edge(\"tools\", \"agent\")

**return** workflow.compile()

**File: Symposium/src/models/tools/calculator.py**

*\"\"\"*

*Basic calculator tool for fast arithmetic operations.*

*\"\"\"*

**from** **langchain_core.tools** **import** Tool

**def** create_calculator_tool() -\> Tool:

*\"\"\"Create a simple calculator tool for basic math.\"\"\"*

**def** calculate(expression: str) -\> str:

*\"\"\"Simple calculator that evaluates basic math expressions.\"\"\"*

**try**:

*\# Only allow basic math operations for security*

allowed_chars = set(\'0123456789+-\*/.() \')

**if** **not** all(c **in** allowed_chars **for** c **in** expression):

**return** \"Error: Only basic math operations allowed\"

result = eval(expression)

**return** f\"Result: **{**result**}**\"

**except** **Exception** **as** e:

**return** f\"Calculation error: **{**str(e)**}**\"

**return** Tool(

name=\"calculator\",

description=\"Fast arithmetic for simple expressions (2+2, 127\*89). Use
for basic math only.\",

func=calculate

)

**File: Symposium/src/models/tools/python_executor.py**

*\"\"\"*

*Whitelist-based Python execution tool.*

*Safe for basic calculations, falls back to Docker for complex
operations.*

*\"\"\"*

**import** **ast**

**import** **sys**

**import** **io**

**from** **contextlib** **import** redirect_stdout, redirect_stderr

**from** **langchain_core.tools** **import** Tool

*\# Whitelist of safe operations*

SAFE_IMPORTS = {

\'math\', \'decimal\', \'statistics\', \'random\', \'json\', \'re\',
\'datetime\'

}

SAFE_BUILTINS = {

\'print\', \'len\', \'range\', \'enumerate\', \'zip\', \'sum\', \'max\',
\'min\',

\'abs\', \'round\', \'sorted\', \'reversed\', \'any\', \'all\', \'int\',
\'float\',

\'str\', \'list\', \'dict\', \'set\', \'tuple\', \'bool\'

}

**def** \_analyze_code_safety(code: str) -\> tuple\[bool, str\]:

*\"\"\"Analyze if code contains only whitelisted operations.\"\"\"*

**try**:

tree = ast.parse(code)

**except** **SyntaxError** **as** e:

**return** **False**, f\"Syntax error: **{**e**}**\"

**for** node **in** ast.walk(tree):

**if** isinstance(node, ast.Import):

**for** alias **in** node.names:

**if** alias.name **not** **in** SAFE_IMPORTS:

**return** **False**, f\"Non-whitelisted import: **{**alias.name**}**\"

**elif** isinstance(node, ast.ImportFrom):

**if** node.module **not** **in** SAFE_IMPORTS:

**return** **False**, f\"Non-whitelisted import: **{**node.module**}**\"

**return** **True**, \"Safe\"

**def** create_python_executor_tool() -\> Tool:

*\"\"\"Create whitelist-based Python executor with Docker fallback
option.\"\"\"*

**def** execute_python(code: str) -\> str:

*\"\"\"Execute Python code with safety analysis.\"\"\"*

*\# Analyze code safety*

is_safe, safety_msg = \_analyze_code_safety(code)

**if** **not** is_safe:

**return** f\"Code rejected by whitelist: **{**safety_msg**}\\n**(Docker
fallback not implemented yet)\"

*\# Execute safe code directly*

stdout_capture = io.StringIO()

stderr_capture = io.StringIO()

safe_globals = {

\'\_\_builtins\_\_\': {name: getattr(\_\_builtins\_\_, name) **for**
name **in** SAFE_BUILTINS}

}

*\# Add safe modules*

**try**:

**import** **math**, **decimal**, **statistics**, **random**, **json**,
**re**, **datetime**

safe_globals.update({

\'math\': math,

\'decimal\': decimal,

\'Decimal\': decimal.Decimal,

\'statistics\': statistics,

\'random\': random,

\'json\': json,

\'re\': re,

\'datetime\': datetime,

})

**except** **ImportError**:

**pass**

**try**:

**with** redirect_stdout(stdout_capture),
redirect_stderr(stderr_capture):

exec(code, safe_globals)

stdout_output = stdout_capture.getvalue()

stderr_output = stderr_capture.getvalue()

**if** stderr_output:

**return** f\"Error: **{**stderr_output.strip()**}**\"

**elif** stdout_output:

**return** stdout_output.strip()

**else**:

**return** \"Code executed successfully (no output)\"

**except** **Exception** **as** e:

**return** f\"Execution error: **{**str(e)**}**\"

**return** Tool(

name=\"python_executor\",

description=\"Execute Python code with whitelist security. Supports
math, decimal, statistics, datetime, json, re modules. Include print()
statements to show results.\",

func=execute_python

)

**File: Symposium/src/controllers/orchestrator.py**

*\"\"\"*

*Main orchestration controller for agent selection and message routing.*

*Handles the core Director-Agent interaction logic.*

*\"\"\"*

**from** **typing** **import** Optional

**from** **langchain_core.messages** **import** HumanMessage

**from** **models.symposium** **import** Symposium

**from** **models.agent** **import** Agent, AgentTier

**from** **models.workflow** **import** WorkflowManager, GraphState

**class** **Orchestrator**:

*\"\"\"Main controller for routing messages to appropriate
agents.\"\"\"*

**def** \_\_init\_\_(self):

self.symposium = Symposium()

self.workflow_manager = WorkflowManager()

self.active_workflows = {}

**def** quick_ask(self, agent_name: str, message: str, use_tools: bool =
**False**) -\> str:

*\"\"\"Simple method to ask a single agent a question.\"\"\"*

agent = self.symposium.get_agent(agent_name)

**if** **not** agent:

**return** f\"Error: Agent **{**agent_name**}** not found\"

**try**:

**if** use_tools **and** agent.tier == AgentTier.RESEARCH_ASSISTANT:

*\# Use the tool-enabled workflow*

graph = self.workflow_manager.create_tool_agent_graph(agent)

initial_state = GraphState(

messages=\[HumanMessage(content=message)\],

current_agent=agent_name

)

final_state = **None**

**for** event **in** graph.stream(initial_state):

final_state = event

**if** final_state **and** \"agent\" **in** final_state:

last_message = final_state\[\"agent\"\]\[\"messages\"\]\[-1\]

**return** last_message.content

**else**:

*\# Handle case where graph terminates at tools node (Cerebras)*

last_message = final_state\[\"tools\"\]\[\"messages\"\]\[-1\]

**return** last_message.content

**else**:

*\# Direct model call*

response =
agent.model_instance.invoke(\[HumanMessage(content=message)\])

**return** response.content

**except** **Exception** **as** e:

**return** f\"Error calling **{**agent_name**}**: **{**str(e)**}**\"

**def** get_agent_registry(self):

*\"\"\"Expose the agent registry for external access.\"\"\"*

**return** self.symposium.get_agent_registry()

**def** get_agent(self, name: str) -\> Optional\[Agent\]:

*\"\"\"Get a specific agent.\"\"\"*

**return** self.symposium.get_agent(name)

**def** list_agents_by_tier(self, tier: AgentTier):

*\"\"\"List agents by capability tier.\"\"\"*

**return** self.symposium.list_agents_by_tier(tier)

**File: Symposium/src/views/cli.py**

*\"\"\"*

*Command-line interface for testing and interacting with the symposium.*

*\"\"\"*

**from** **controllers.orchestrator** **import** Orchestrator

**from** **models.agent** **import** AgentTier

**class** **SymposiumCLI**:

*\"\"\"Simple CLI interface for testing symposium functionality.\"\"\"*

**def** \_\_init\_\_(self):

self.orchestrator = Orchestrator()

**def** run_demo(self):

*\"\"\"Run the standard demo sequence from the original manager.\"\"\"*

print(\"\-\-- Initializing Symposium \-\--\")

print(\"**\\n**\-\-- Agent Registry \-\--\")

**for** name, agent **in**
self.orchestrator.get_agent_registry().items():

status = \"✓\" **if** agent.model_instance **else** \"✗\"

print(f\"**{**status**}** **{**name**}**
(**{**agent.provider.value**}**) - **{**agent.tier.value**}**\")

print(\"**\\n**\-\-- Testing Simple Agent Call \-\--\")

response = self.orchestrator.quick_ask(\"Claude\", \"What is 2+2? Answer
in exactly 5 words.\")

print(f\"Response: **{**response**}**\")

print(\"**\\n**\-\-- Testing Tool-Using Agents \-\--\")

research_assistants = \[\"Groq_Assistant\", \"Mistral_Assistant\",
\"Cerebras_Assistant\"\]

test_calculation = \"Calculate 127 \* 89 + 456\"

**for** assistant_name **in** research_assistants:

print(f\"**\\n**\-\-- Testing **{**assistant_name**}** \-\--\")

response = self.orchestrator.quick_ask(assistant_name, test_calculation,
use_tools=**True**)

print(f\"**{**assistant_name**}**: **{**response**}**\")

print(\"**\\n**\-\-- Symposium Ready \-\--\")

**if** \_\_name\_\_ == \"\_\_main\_\_\":

cli = SymposiumCLI()

cli.run_demo()

**File: Symposium/src/symposium_manager_v2.py**

*#!/usr/bin/env python3*

*\"\"\"*

*Multi-LLM Symposium Manager v2.0*

*Clean entry point using modular MVC architecture.*

*\"\"\"*

**from** **views.cli** **import** SymposiumCLI

**from** **controllers.orchestrator** **import** Orchestrator

**def** main():

*\"\"\"Main entry point for the symposium system.\"\"\"*

*\# For direct access to orchestrator*

*\# orchestrator = Orchestrator()*

*\# For CLI demo*

cli = SymposiumCLI()

cli.run_demo()

**if** \_\_name\_\_ == \"\_\_main\_\_\":

main()
