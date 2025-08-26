import os
import asyncio
from pydantic import BaseModel
from dotenv import load_dotenv  # <-- NEW: for loading .env
from agents import (
    Agent,
    InputGuardrail,
    GuardrailFunctionOutput,
    Runner,
    OpenAIChatCompletionsModel,
    RunConfig,
    AsyncOpenAI,
)

# ------------------------------
# 1. Load environment variables
# ------------------------------
load_dotenv()  # this will read from .env file

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY is not set in the .env file.")

# ------------------------------
# 2. Gemini client
# ------------------------------
external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# ------------------------------
# 3. Gemini model
# ------------------------------
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",  # can be gemini-1.5-flash or gemini-1.5-pro
    openai_client=external_client,
)

# ------------------------------
# 4. RunConfig
# ------------------------------
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# ------------------------------
# 5. Guardrail output schema
# ------------------------------
class RequirementOutput(BaseModel):
    is_requirement: bool
    reasoning: str

# ------------------------------
# 6. Guardrail agent
# ------------------------------
guardrail_agent = Agent(
    name="Guardrail check",
    instructions=(
        "You are a filter agent. "
        "Your job is to decide if the user query is safe, relevant, and should be answered. "
        "- If the query is about math, history, or general learning → set is_requirement=True. "
        "- If the query is harmful, unsafe, spam, or irrelevant → set is_requirement=False. "
        "Always explain your reasoning briefly."
    ),
    output_type=RequirementOutput,
)

# ------------------------------
# 7. Math & History tutor agents
# ------------------------------
math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for Math Tutoring",
    instructions="You provide help with math-related queries. Explain step by step with reasoning and examples.",
)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for History Tutoring",
    instructions="You provide assistance with history-related queries. Explain important events and context clearly.",
)

# ------------------------------
# 8. Guardrail function
# ------------------------------
async def requirement_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context, run_config=config)
    final_output = result.final_output_as(RequirementOutput)

    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_requirement
    )

# ------------------------------
# 9. Triage agent
# ------------------------------
triage_agent = Agent(
    name="Triage Agent",
    instructions="You decide which agent (Math or History) should handle the query.",
    handoffs=[math_tutor_agent, history_tutor_agent],
    input_guardrails=[InputGuardrail(guardrail_function=requirement_guardrail)],
)

# ------------------------------
# 10. Main runner with user input
# ------------------------------
async def main():
    print("🤖 Multiple Agents (Math + History) Powered by Gemini\n")
    while True:
        user_query = input("Enter your question (or type 'exit' to quit): ").strip()
        if user_query.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        result = await Runner.run(triage_agent, user_query, run_config=config)
        print(f"\nAnswer:\n{result.final_output}\n")

if __name__ == "__main__":
    asyncio.run(main())
