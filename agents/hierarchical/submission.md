**Note: Make a copy of this for your specific day** 

# Day [X] - Submission

### **Topic: Hierarchical Agents (Russian Doll Pattern)**

### **Owner: [add your ldap]**

### **Status: Started**

### **The Golden Rule: "Always Kata" 🥋**

Our goal is **actionable skills, zero fluff, deployed in under 5 minutes.** If a developer cannot copy-paste your code and see a result in 300 seconds, it is not a Kata.

### **⚠️ The "Lean Team" Reality Check**

We are approaching Google Next. Everyone is busy. We cannot fix broken demos or edit bad videos.

* **The Queue:** We have a prioritized queue. High-quality submissions (perfect code + great video) go live immediately.  
* **The Backlog:** Submissions with "slop" (AI voiceovers, broken snippets, no visuals) go to the back of the line until *you* fix them.

## **📋 The Deliverable Template**

*Please make a copy of this doc and share it with [Owners].*

### **1. The Kata (Website Modal Content)**

*Target Audience: Developers. Style: AdventOfCode / DevRel.*

* **Goal:** Explain *how* it works technically.  
* **Constraint:** 2-3 paragraphs max. No marketing fluff. Pure engineering.  
* **Draft:**  
  When dealing with an extremely complex prompt, we often don't know the required tasks ahead of time. The Hierarchical (or "Nested" / "Russian Doll") pattern solves this by using a top-level Manager agent that utilizes an `AgentTool` to dynamically generate a plan before executing it.

  Instead of pre-coding separate parallel workers, the Manager leverages a dedicated Planner agent as a tool. Once the plan is returned to the Manager, it activates its nested `SequentialAgent` sub-pipeline—containing a Researcher and a Synthesizer—to fully execute the plan autonomously without requiring a human-in-the-loop.

### **2. The Code (The "Modal" Snippet)**

* **Constraint:** Must fit in a code block on a single screen. No massive files.  
* **Type:** CLI Commands or short Python/YAML Snippet.  
* **Requirement:** Must be copy-pasteable and functional.  
* **Snippet:**

```python
from google.adk.tools.agent_tool import AgentTool
from google.adk.agents import LlmAgent, SequentialAgent

# The Planner is used purely as a tool by the Manager
planner = LlmAgent(
    name='planner',
    model='gemini-3-flash-preview',
    instruction='Break the user prompt into exactly three distinct research themes.'
)

# A logical pipeline of sub-agents to handle execution
execution_pipeline = SequentialAgent(
    name='execution_pipeline',
    sub_agents=[researcher, synthesizer] # Defined elsewhere
)

# The Manager orchestrates the whole flow autonomously
manager = LlmAgent(
    name='manager',
    model='gemini-3-flash-preview',
    tools=[AgentTool(planner)],
    sub_agents=[execution_pipeline],
    instruction='''
    1. Use the planner tool to create a detailed research plan based on the user's prompt.
    2. Activate your execution_pipeline sub-agent and pass the completed plan to it so it can execute it.
    '''
)

root_agent = manager
app = App(name="hierarchical", root_agent=root_agent)
```

### **3. Visuals (The "No Slop" Policy) 📹**

*Based on recent feedback, "NotebookLM videos" or generic AI voiceovers feel "sloppy" and will be rejected.*

We need **two** assets:

1. **The "Hype" GIF (Socials):**  
   * **Length:** <20 seconds.  
   * **Content:** Fast-paced screen recording. Terminal flying by, UI updating. Pure dopamine.  
2. **The "Human" Demo (Website):**  
   * **Length:** 3-5 minutes max.  
   * **Content:** A real human (you) talking through the code.  
   * **Tool Tip:** Use **Remotion** or **Vibe Coding** tools to automate the editing, but keep the voice/intent human.

### **4. Links:** 

* [Project Repository](https://github.com/LuisSala/advent-of-agents-spring-26)
* [LlmAgent Reference](https://google.github.io/adk-docs/agents/llm-agents/)
* [ParallelAgent Reference](https://google.github.io/adk-docs/agents/workflow-agents/parallel-agents/)
* [SequentialAgent Reference](https://google.github.io/adk-docs/agents/workflow-agents/sequential-agents/)
