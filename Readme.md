# 🔬 ResearchMind — Multi-Agent AI Research Pipeline

> An autonomous AI research system that searches, scrapes, writes, and critiques — delivering a polished research report on any topic in minutes.

---

## 📌 Overview

ResearchMind is a **production-grade multi-agent AI pipeline** built with LangChain, Mistral AI, Tavily Search, and Streamlit. It mimics how a human researcher works — finding sources, reading them deeply, drafting a report, and then self-critiquing it — but does it autonomously using specialized AI agents.

The system chains together **4 stages**:

```
User Input (Topic)
      ↓
[Agent 1: Search Agent]  ←→  Tavily Web Search API
      ↓ structured search results
[Agent 2: Reader Agent]  ←→  HTTP Scraper (BeautifulSoup)
      ↓ deep scraped content
[Chain 3: Writer Chain]  ←→  Mistral LLM
      ↓ full research report (markdown)
[Chain 4: Critic Chain]  ←→  Mistral LLM
      ↓
Final Report + Quality Score + Feedback
```

---

## ✨ Features

- 🤖 **Two autonomous LangChain ReAct agents** — agents decide *when* and *how* to use tools
- 🔍 **Web search via Tavily** — AI-optimized search returning clean, structured results
- 📄 **Deep content scraping** — BeautifulSoup-powered URL scraper that strips noise (nav, scripts, footers)
- ✍️ **LLM-powered report writer** — structured Introduction → Key Findings → Conclusion → Sources
- 🧐 **Automated critic** — scores the report 1–10 with strengths, improvements, and a one-line verdict
- 🌐 **Streamlit web UI** — real-time pipeline status, dark theme, report download as `.md`
- 💻 **CLI runner** — `pipeline.py` for terminal-based usage

---

## 🗂️ Project Structure

```
researchmind/
│
├── app.py              # Streamlit web application (UI + pipeline runner)
├── agents.py           # LangChain agent & chain definitions
├── custom_tools.py     # @tool-decorated functions (web_search, scrape_url)
├── pipeline.py         # Command-line pipeline runner
├── requirements.txt    # Python dependencies
├── .env                # API keys (never commit this)
│
└── scratch/            # Debug/test scripts used during development
    ├── debug_import.py
    └── test_all_imports.py
```

---

## ⚙️ Architecture Deep Dive

### Agents vs Chains

This project uses **both** LangChain primitives:

| Concept | What it does | Used for |
|---|---|---|
| **Agent** | LLM decides when/how to call tools, loops autonomously | Search Agent, Reader Agent |
| **Chain** | Fixed sequence: prompt → LLM → output, no tool use | Writer Chain, Critic Chain |

### Agent 1 — Search Agent
```python
create_agent(model=llm, tools=[web_search])
```
- Given the `web_search` tool backed by Tavily API
- Autonomously decides search queries, calls the tool, returns structured results
- Follows the **ReAct pattern**: Reason → Act → Observe → Repeat

### Agent 2 — Reader Agent
```python
create_agent(model=llm, tools=[scrape_url])
```
- Receives search results, **autonomously picks the most relevant URL**
- Calls `scrape_url` to fetch full page content
- Returns 3000 chars of clean extracted text

### Writer Chain (LCEL)
```python
writer_chain = writer_prompt | llm | StrOutputParser()
```
- Uses LangChain Expression Language (LCEL) — the `|` pipe operator
- System prompt sets role as "expert research writer"
- Human prompt injects `{topic}` and `{research}` variables
- Forces structured output: Introduction, Key Findings (3+), Conclusion, Sources

### Critic Chain (LCEL)
```python
critic_chain = critic_prompt | llm | StrOutputParser()
```
- Evaluates the generated report strictly
- Outputs: `Score: X/10`, Strengths, Areas to Improve, One-line verdict

---

## 🛠️ Custom Tools

### `web_search(query: str)`
```python
@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information on a topic."""
```
- Decorated with `@tool` — docstring becomes the description the LLM reads
- Calls Tavily's search API, fetches top 5 results
- Returns formatted titles, URLs, and 300-char snippets

### `scrape_url(url: str)`
```python
@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL."""
```
- Makes HTTP GET with browser-like User-Agent header
- Uses BeautifulSoup to remove `<script>`, `<style>`, `<nav>`, `<footer>` tags
- Returns first 3000 characters of clean body text
- Handles failures gracefully with try/except

---

## 🖥️ Streamlit UI (`app.py`)

### Layout
- **3-column layout**: Input area | Spacer | Pipeline status
- **Left column**: Topic input, Run button, example topic chips
- **Right column**: Live pipeline step cards (01 → 02 → 03 → 04) with status indicators

### Pipeline Step Cards
Each step shows one of three states:
- `WAITING` — grey, not yet started
- `● RUNNING` — orange, currently active
- `✓ DONE` — green, completed

### State Management
Uses `st.session_state` to persist data across Streamlit's full-page reruns:
```python
st.session_state.results  # dict: {"search": ..., "reader": ..., "writer": ..., "critic": ...}
st.session_state.running  # bool: pipeline is executing
st.session_state.done     # bool: pipeline finished
```

### Results Display
- Raw Search + Scraped outputs in collapsible `st.expander` panels
- Final report rendered as native Markdown
- Download button exports report as `.md` file
- Critic feedback in a green-bordered panel

### Styling
- Fonts: `Syne` (headings), `DM Mono` (labels/code), `DM Sans` (body)
- Dark background: `#0a0a0f` with radial orange gradient overlays
- Accent color: `#ff8c32` (orange)
- All custom CSS injected via `st.markdown(..., unsafe_allow_html=True)`

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Mistral AI API key → [console.mistral.ai](https://console.mistral.ai/)
- Tavily API key → [tavily.com](https://tavily.com/)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/researchmind.git
cd researchmind

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env and add your API keys
```

### Configure `.env`
```env
MISTRAL_API_KEY="your_mistral_key_here"
MISTRAL_MODEL="mistral-small-latest"
TAVILY_API_KEY="your_tavily_key_here"
```

### Run the Web App
```bash
streamlit run app.py
```
Opens at `http://localhost:8501`

### Run via CLI
```bash
python pipeline.py
# Enter your research topic when prompted
```

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `langchain` | Agent & chain orchestration framework |
| `langchain-mistralai` | Mistral LLM integration |
| `langchain-core` | Core LCEL primitives, prompts, parsers |
| `tavily-python` | AI-optimized web search API |
| `beautifulsoup4` | HTML parsing and text extraction |
| `requests` | HTTP requests for scraping |
| `streamlit` | Web UI framework |
| `python-dotenv` | Load environment variables from `.env` |
| `rich` | Colored terminal output |
| `pydantic` | Data validation (used by LangChain internals) |

---

## 🧠 Key Concepts

### ReAct Pattern (Agents)
Agents follow: **Re**ason → **Act** → **Observe** → Repeat until task complete. The LLM reasons about what tool to call, calls it, observes the result, and loops.

### LCEL (LangChain Expression Language)
The `|` pipe syntax composes components declaratively:
```python
chain = prompt | llm | output_parser
```
Supports streaming, async, and batching automatically.

### `temperature=0`
Used for all LLM calls — deterministic/greedy output. No randomness. Appropriate for factual research tasks where consistency matters.

### `@tool` Decorator
Converts a Python function into an LLM-callable tool. The **docstring** becomes the tool description that the LLM reads to decide when to use it — so clear docstrings are critical.

---

## 🔮 Possible Improvements

- [ ] Add memory/vector store (FAISS or Chroma) to avoid re-scraping known URLs
- [ ] Support multiple URL scraping in the Reader Agent (currently scrapes one)
- [ ] Add streaming output so the report renders word-by-word
- [ ] Integrate LangSmith for tracing agent decisions
- [ ] Add a feedback loop — critic can trigger re-writing if score < 7
- [ ] Export report as PDF in addition to Markdown
- [ ] Deploy to Streamlit Cloud or HuggingFace Spaces

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 👤 Author

Built as a demonstration of multi-agent LLM orchestration using LangChain, Mistral AI, and Streamlit.

---

*ResearchMind · Powered by LangChain multi-agent pipeline · Built with Streamlit*