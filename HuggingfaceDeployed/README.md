---
title: Multiple Agents
emoji: "🚀"
colorFrom: red
colorTo: green
sdk: streamlit
app_file: app.py
app_port: 8501
tags:
  - streamlit
pinned: false
short_description: "This app is powered by Google Gemini and OpenAI-style."

---

# Welcome to Streamlit!

Edit `/src/streamlit_app.py` to customize this app to your heart's desire. :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).



# 🤖 Multiple Agents Tutor (Math + History)

A **Streamlit application** deployed on [Hugging Face Spaces](https://huggingface.co/spaces) that demonstrates how to build a **multi-agent system with guardrails** using **Google Gemini API**.  

This project uses **specialized AI agents** to answer user queries in **Math** and **History**, while a **Guardrail agent** ensures the safety and relevance of the input.

---

## 🚀 Features
- ✅ **Multi-Agent Architecture**:  
  - *Guardrail Agent* → Filters harmful/irrelevant queries  
  - *Triage Agent* → Decides whether Math or History agent should respond  
  - *Math Tutor Agent* → Solves math queries step by step  
  - *History Tutor Agent* → Explains historical events and context  
- ✅ Powered by **Google Gemini (2.0 Flash / 1.5 Pro)**  
- ✅ Simple, interactive **Streamlit UI**  
- ✅ Deployable on **Hugging Face Spaces**  

---

## 🛠️ Tech Stack
- [Python 3.9+](https://www.python.org/)  
- [Streamlit](https://streamlit.io/) – Interactive UI  
- [agents](https://pypi.org/project/agents/) – Agent orchestration framework  
- [Google Gemini API](https://ai.google.dev/) – LLM backend  
- [dotenv](https://pypi.org/project/python-dotenv/) – Environment variable management  

---

## 📂 Project Structure
---
