from google.adk.agents import Agent, LoopAgent, SequentialAgent
from google.adk.tools import FunctionTool, ToolContext

def approve_draft(tool_context: ToolContext) -> dict:
    """
    Call this tool when the draft completely meets the rubric and is approved.
    DO NOT CALL THIS IF THE DRAFT FAILS ANY RUBRIC CRITERIA.
    """
    tool_context.actions.escalate = True
    return {"status": "success", "message": "Draft approved. Escalating out of loop to finish."}

approve_tool = FunctionTool(approve_draft)

writer = Agent(
    name='writer',
    model='gemini-2.5-flash',
    description='You are a creative sci-fi writer.',
    instruction=(
        "You are a sci-fi writer. Your job is to write a short story based on the user's prompt. "
        "IMPORTANT: If the critic provides feedback, revise your story strictly following their feedback. "
        "Do not explain yourself, just provide the revised story."
    )
)

critic = Agent(
    name='critic',
    model='gemini-3.1-pro-preview',
    description='You are a strict editor and critic.',
    instruction=(
        "You evaluate the writer's draft against the following RUBRIC:\n"
        "1. The story must be a sci-fi story.\n"
        "2. The story must exactly contain the words: 'nebula', 'glitch', and 'chronometer'.\n"
        "3. The story must be very short, under 100 words.\n\n"
        "If the draft FAILS any criteria, output actionable feedback on what needs to be fixed. "
        "DO NOT approve the draft. "
        "If the draft PASSES all criteria perfectly, you MUST call the `approve_draft` tool to signal "
        "that the draft is approved and the loop can end."
    ),
    tools=[approve_tool]
)

root_agent = LoopAgent(
    name="writer_critic_loop",
    sub_agents=[writer, critic],
    max_iterations=4
)
