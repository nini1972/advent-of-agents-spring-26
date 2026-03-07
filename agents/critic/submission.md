# Day [X] - Submission

### **Topic: Writer-Critic Pattern with LoopAgent**

### **Owner: luissala**

### **Status: Complete**

### **1. The Kata (Website Modal Content)**

The Writer-Critic (or Generator-Evaluator) pattern is a powerful way to automatically refine LLM outputs. In this Kata, we use ADK's `LoopAgent` to orchestrate a conversation between a creative "Writer" (`gemini-2.5-flash`) and a strict "Critic" (`gemini-3.1-pro-preview`). 

By assigning an `output_key` to each agent, we elegantly route the Writer's draft to the Critic, and the Critic's feedback back to the Writer using ADK's native `{var}` templating. The loop continues until the Critic determines the strict rubric is met, at which point it calls an `approve_draft` tool that uses `tool_context.actions.escalate = True` to break out of the loop and return the final polished result.

### **2. The Code (The "Modal" Snippet)**

```python
from google.adk.agents import Agent, LoopAgent
from google.adk.tools import FunctionTool, ToolContext

def approve_draft(tool_context: ToolContext) -> dict:
    tool_context.actions.escalate = True # Breaks the loop execution early
    return {"status": "success", "message": "Approved."}

writer = Agent(
    name='writer', model='gemini-3-flash-preview',
    instruction="Revise your draft based on feedback: {latest_feedback?}",
    output_key='latest_draft'
)

critic = Agent(
    name='critic', model='gemini-3-flash-preview',
    instruction=(
        "Evaluate draft: {latest_draft}. "
        "RUBRIC: 1. Must be sci-fi. 2. Must be under 100 words. "
        "If it FAILS, provide feedback. If it PASSES perfectly, call approve_draft."
    ),
    tools=[FunctionTool(approve_draft)],
    output_key='latest_feedback'
)

root_agent = LoopAgent(name="loop", sub_agents=[writer, critic], max_iterations=4)

from google.adk.apps import App
app = App(name="critic", root_agent=root_agent)
```

**Run it locally:**
```bash
uv run adk run agents/critic
```

### **3. Visuals (The "No Slop" Policy) 📹**

1. **The "Hype" GIF (Socials):**  
   * **Target:** A fast-paced terminal recording of `uv run adk run agents/critic`. Show the Writer failing the word count and missing the required "glitch" keyword, the Critic snapping back with the correction, and the final approved story streaming out.
2. **The "Human" Demo (Website):**  
   * **Target:** A 3-minute screen recording walking through the codebase. Focus heavily on how `output_key` routes the state back into the `{latest_feedback?}` template variable, and how the `escalate=True` tool breaks the ADK loop.

### **4. Links:** 

* [Writer-Critic Demo Source Code](https://github.com/LuisSala/advent-of-agents-spring-26/tree/main/agents/critic)
* [LlmAgent Reference](https://google.github.io/adk-docs/agents/llm-agents/)
* [LoopAgent Reference](https://google.github.io/adk-docs/agents/workflow-agents/loop-agents/)
* [Function Tools Reference](https://google.github.io/adk-docs/tools-custom/function-tools/)
