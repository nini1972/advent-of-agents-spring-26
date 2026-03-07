from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from google.adk.tools import google_search
from google.adk.agents import LlmAgent

LlmAgent.set_default_model('gemini-2.5-flash')

# ==============================================================================
# HIERARCHICAL DECOMPOSITION (Russian Doll Pattern)
# ==============================================================================
# In cases where a user prompt is extremely complex, we might not know ahead
# of time what specific research needs to be done.
# 
# Instead of hardcoding specialized agents (like we did in the 'fanout' example),
# we introduce a Manager agent. The Manager's sole job is to read the complex 
# prompt and break it down into an explicit, structured plan. 
#
# By writing this plan to the ADK session state (output_key='manager_plan'),
# downstream Worker agents can dynamically interpolate that plan into their 
# instructions, allowing them to execute specific slices of the Manager's
# dynamically generated task list.
# ==============================================================================

manager = Agent(
    name='manager',
    description='A high-level planner that breaks a complex prompt into distinct parts.',
    instruction='''
    You are an AI Architect Manager. Read the user's complex prompt and break it down into exactly three distinct research themes or chronological phases (e.g., Historical, Current State, Future Outlook). 
    
    Output nothing but a numbered list:
    1. [Theme 1 Description]
    2. [Theme 2 Description]
    3. [Theme 3 Description]
    ''',
    output_key='manager_plan',
)

# ==============================================================================
# THE WORKERS
# ==============================================================================
# Each worker is identical in capability (they all have google_search), but 
# their instructions explicitly tell them to focus on a different bullet point
# from the dynamically generated {manager_plan}.
# ==============================================================================

worker_1 = Agent(
    name='worker_1',
    description='Executes the first part of the manager plan.',
    tools=[google_search],
    output_key='worker_1_output',
    instruction='''
    You are Researcher 1. Use the google_search tool to complete ONLY task #1 from the Manager's Plan below. Provide a detailed summary of your findings.
    
    # Manager's Plan
    {manager_plan}
    '''
)

worker_2 = Agent(
    name='worker_2',
    description='Executes the second part of the manager plan.',
    tools=[google_search],
    output_key='worker_2_output',
    instruction='''
    You are Researcher 2. Use the google_search tool to complete ONLY task #2 from the Manager's Plan below. Provide a detailed summary of your findings.
    
    # Manager's Plan
    {manager_plan}
    '''
)

worker_3 = Agent(
    name='worker_3',
    description='Executes the third part of the manager plan.',
    tools=[google_search],
    output_key='worker_3_output',
    instruction='''
    You are Researcher 3. Use the google_search tool to complete ONLY task #3 from the Manager's Plan below. Provide a detailed summary of your findings.
    
    # Manager's Plan
    {manager_plan}
    '''
)

worker_squad = ParallelAgent(
    name='worker_squad',
    description='Runs the three workers concurrently.',
    sub_agents=[worker_1, worker_2, worker_3],
)

# ==============================================================================
# THE SYNTHESIZER
# ==============================================================================
# Gathers the manager's original plan and the specific outputs from the parallel 
# workers to write the final unified response.
# ==============================================================================

synthesizer = Agent(
    name='synthesizer',
    description='Synthesizes the worker outputs.',
    instruction='''
    You are the Lead Editor. Using the original Manager's Plan and the specific outputs from your three researchers, synthesize a comprehensive, cohesive report on the topic.
    
    # Original Plan
    {manager_plan}
    
    # Researcher 1 Findings
    {worker_1_output}
    
    # Researcher 2 Findings
    {worker_2_output}
    
    # Researcher 3 Findings
    {worker_3_output}
    '''
)

root_agent = SequentialAgent(
    name='root_agent',
    description='Orchestrates the manager, parallel workers, and synthesizer.',
    sub_agents=[manager, worker_squad, synthesizer]
)

from google.adk.apps import App

app = App(
    name="hierarchical",
    root_agent=root_agent
)

if __name__ == '__main__':
    # Provided for local testing if running directly with `uv run python` instead of `adk run`
    import asyncio
    from google.adk.runners import InMemoryRunner

    async def run_demo():
        runner = InMemoryRunner(app=app)
        print("Starting Hierarchical Agent Demo...")
        await runner.run_debug("Research the evolution of generative AI in software engineering. Cover its historical roots, its current impact on standard IDEs, and predict what software engineering will look like 10 years from now.")

    asyncio.run(run_demo())
