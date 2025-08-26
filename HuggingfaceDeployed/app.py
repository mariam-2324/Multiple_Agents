import os
import asyncio
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from pydantic import BaseModel

# ------------------------------
# 1. Load environment variables
# ------------------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("❌ GEMINI_API_KEY is not set in Secrets.")
    st.stop()

# ------------------------------
# 2. Configure Gemini client
# ------------------------------
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# ------------------------------
# 3. Guardrail output schema
# ------------------------------
class RequirementOutput(BaseModel):
    is_requirement: bool
    reasoning: str

# ------------------------------
# 4. Guardrail check
# ------------------------------
async def requirement_guardrail(query: str) -> RequirementOutput:
    guardrail_prompt = f"""
    Decide if the user query should be answered.

    Query: {query}

    Rules:
    - If query is about math, history, or learning → is_requirement=True.
    - If query is unsafe, spam, or irrelevant → is_requirement=False.
    Always explain your reasoning.
    """

    resp = model.generate_content(guardrail_prompt)
    text = resp.text.strip()

    if "true" in text.lower():
        return RequirementOutput(is_requirement=True, reasoning=text)
    else:
        return RequirementOutput(is_requirement=False, reasoning=text)

# ------------------------------
# 5. Math & History agents
# ------------------------------
async def math_tutor(query: str) -> str:
    resp = model.generate_content(f"Explain step by step: {query}")
    return resp.text

async def history_tutor(query: str) -> str:
    resp = model.generate_content(f"Explain clearly: {query}")
    return resp.text

# ------------------------------
# 6. Triage agent
# ------------------------------
async def triage_agent(query: str) -> str:
    triage_prompt = f"""
    Decide which agent should answer.

    Query: {query}

    Options: Math Tutor or History Tutor.
    Reply with exactly one: "math" or "history".
    """

    resp = model.generate_content(triage_prompt)
    decision = resp.text.strip().lower()

    if "math" in decision:
        return await math_tutor(query)
    elif "history" in decision:
        return await history_tutor(query)
    else:
        return "🤖 Sorry, I could not decide which tutor should handle this question."

# ------------------------------
# 7. Streamlit UI
# ------------------------------
st.set_page_config(page_title="Multiple Agents App", page_icon="🤖", layout="centered")
st.title("🤖 Multiple Agents Tutor (Math + History)")
st.markdown("This app is powered by **Google Gemini** and uses multiple AI agents with guardrails.")

user_query = st.text_input("Enter your question:", placeholder="e.g., What is 10 divided by 2?")
submit = st.button("Get Answer")

if submit and user_query.strip():
    async def run_query():
        guardrail = await requirement_guardrail(user_query)
        if not guardrail.is_requirement:
            return f"❌ Blocked by guardrail: {guardrail.reasoning}"
        return await triage_agent(user_query)

    with st.spinner("Thinking... 🤔"):
        answer = asyncio.run(run_query())
        st.success("✅ Answer:")
        st.write(answer)
