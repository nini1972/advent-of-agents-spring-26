# Day [X] - Submission

### **Topic: Parallel LLM Fanout and State Interpolation**

### **Owner: luissala**

### **Status: Draft**

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

* **Goal:** Explain *how* to drastically reduce latency by running independent, grounded LLM tasks concurrently and automatically synthesizing their outputs using Google ADK.
* **Draft:**  
  By leveraging ADK's `ParallelAgent` and `output_key` routing, we run multiple grounded LLM calls via Google Search concurrently, saving massive amounts of time. The results are automatically funneled into a session state dictionary. A downstream `SequentialAgent` then seamlessly injects these outputs as `{placeholders}` into a synthesis prompt without writing custom orchestration or data-passing code.

### **2. The Code (The "Modal" Snippet)**

* **Constraint:** Must fit in a code block on a single screen. No massive files.  
* **Type:** CLI Commands or short Python/YAML Snippet.  
* **Requirement:** Must be copy-pasteable and functional.  
* **Snippet:**

```python
from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from google.adk.tools import google_search

# 1. Define independent research agents with explicit output_keys and grounding tools
healthcare_researcher = Agent(name='healthcare_researcher', model='gemini-3.0-flash-preview', output_key='healthcare_research', tools=[google_search], instruction='Use the Google Search tool to...')
finance_researcher = Agent(name='finance_researcher', model='gemini-3.0-flash-preview', output_key='finance_research', tools=[google_search], instruction='Use the Google Search tool to...')

# 2. Fanout: Run them all concurrently
research_squad = ParallelAgent(
    name='research_squad',
    sub_agents=[healthcare_researcher, finance_researcher],
)

# 3. State Interpolation: Use `{output_key}` placeholders in the synthesizer prompt
synthesizer = Agent(
    name='synthesizer',
    model='gemini-3.0-flash-preview',
    instruction="Synthesize the following trends: \n\n{healthcare_research}\n\n{finance_research}",
)

# 4. Sequential block ensures fanout completes and populates state before synthesis
root_agent = SequentialAgent(
    name='root_agent',
    sub_agents=[research_squad, synthesizer],
)

from google.adk.apps import App
app = App(name="fanout", root_agent=root_agent)
```

### **3. Visuals (The "No Slop" Policy) 📹**

*Based on recent feedback, "NotebookLM videos" or generic AI voiceovers feel "sloppy" and will be rejected.*

We need **two** assets:

1. **The "Hype" GIF (Socials):**  
   * **Length:** <20 seconds.  
   * **Content:** Fast-paced screen recording showing multiple researcher logs executing concurrently and resolving to a final report.
2. **The "Human" Demo (Website):**  
   * **Length:** 3-5 minutes max.  
   * **Content:** Real human talking through how `output_key` implicitly solves data routing issues when chaining complex agents in ADK.

### **4. Links:** 

* [Project Repository](https://github.com/LuisSala/advent-of-agents-spring-26)
* [LlmAgent Reference](https://google.github.io/adk-docs/agents/llm-agents/)
* [ParallelAgent Reference](https://google.github.io/adk-docs/agents/workflow-agents/parallel-agents/)
* [SequentialAgent Reference](https://google.github.io/adk-docs/agents/workflow-agents/sequential-agents/)