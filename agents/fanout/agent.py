from google.adk.agents import Agent, ParallelAgent, SequentialAgent

# We specify our target model once since child agents can inherit it.
from google.adk.agents import LlmAgent
LlmAgent.set_default_model('gemini-2.5-flash')

healthcare_researcher = Agent(
    name='healthcare_researcher',
    description='Specializes in AI trends in healthcare',
    instruction='Research how AI is impacting healthcare. Provide a simple, concise bulleted list of 2-3 key trends. Cite examples if possible.',
)

finance_researcher = Agent(
    name='finance_researcher',
    description='Specializes in AI trends in finance',
    instruction='Research how AI is impacting finance and banking. Provide a simple, concise bulleted list of 2-3 key trends. Cite examples if possible.',
)

education_researcher = Agent(
    name='education_researcher',
    description='Specializes in AI trends in education',
    instruction='Research how AI is impacting education. Provide a simple, concise bulleted list of 2-3 key trends. Cite examples if possible.',
)

research_squad = ParallelAgent(
    name='research_squad',
    description='A squad of researchers that run concurrently.',
    sub_agents=[healthcare_researcher, finance_researcher, education_researcher],
)

synthesizer = Agent(
    name='synthesizer',
    description='Takes compiled research and writes a final report.',
    instruction='You are the Lead Editor. Read the aggregated research trends provided by the squad and synthesize them into a single, cohesive brief report titled "The AI Impact Matrix". Compare and contrast the trends where applicable.',
)

# SequentialAgent executes agents in list order, passing the output of the previous to the next.
root_agent = SequentialAgent(
    name='root_agent',
    description='The main pipeline that orchestrates the fanout and synthesis.',
    sub_agents=[research_squad, synthesizer],
)

if __name__ == '__main__':
    # Provided for local testing if running directly with `uv run python` instead of `adk run`
    import asyncio
    from google.adk.runners import InMemoryRunner

    async def run_demo():
        runner = InMemoryRunner(agent=root_agent)
        # Using a dummy prompt because the agents are already hardcoded with specific instructions.
        print("Starting Parallel Fanout Demo...")
        async for event in runner.run_async("Please execute the AI trend research task."):
            if event.is_final_response():
                print(f"[{event.author}] {event.content.text}")

    asyncio.run(run_demo())
