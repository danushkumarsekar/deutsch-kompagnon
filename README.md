# 🇩🇪 Deutsch-Kompagnon — German B2 AI Tutor

An AI-powered chatbot for German B2 exam preparation, built with **Retrieval-Augmented Generation (RAG)**. Ask any German grammar question and get structured, context-grounded answers with source citations — no hallucinations.

🚀 **[Try the live demo](https://deutsch-kompagnon.streamlit.app)** &nbsp;·&nbsp; 💬 Ask about cases, verbs, prepositions, and more

---

## ✨ What It Does

- Answers German grammar questions in English or German
- Retrieves relevant chunks from curated B2 learning materials
- Shows source citations under every answer (no black-box responses)
- Refuses to answer out-of-scope questions instead of hallucinating
- Covers Cases (Nom/Akk/Dat/Gen), Verbs, Prepositions, Subordinate Clauses, Passive and Konjunktiv II

## 🏗️ Architecture

```
User Question
     │
     ▼
[1] Convert to embedding (HuggingFace: all-MiniLM-L6-v2)
     │
     ▼
[2] Semantic search in ChromaDB → top 3 relevant chunks
     │
     ▼
[3] Send [question + retrieved context] to LLM (Groq: openai/gpt-oss-120b)
     │
     ▼
[4] Return grounded answer + source citations
```

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **UI** | Streamlit |
| **Orchestration** | LangChain |
| **Embeddings** | HuggingFace `sentence-transformers/all-MiniLM-L6-v2` (free, local) |
| **Vector DB** | ChromaDB (local persistence) |
| **LLM** | Groq API — `openai/gpt-oss-120b` (free tier) |
| **Hosting** | Streamlit Community Cloud (free) |

**Total cost to build & run: €0.** Chose free open-source stack to prove the system works before scaling.

## 🎯 Design Decisions

- **Why RAG instead of fine-tuning?** RAG lets me update the knowledge base by editing markdown files instead of retraining models. Cheaper, faster, more transparent for a learner-facing tool.
- **Why free-tier LLM (Groq) over OpenAI?** Groq offers `openai/gpt-oss-120b` at zero cost with sub-second inference — perfect for a portfolio project. Same code swaps to GPT-4 or Claude by changing one line.
- **Why local embeddings (HuggingFace) over OpenAI embeddings?** No API key needed, runs on CPU, ~90 MB one-time download. Anyone can clone and run this without signup.
- **Why refuse out-of-scope questions?** The prompt explicitly instructs the LLM to say "I don't have that in context" instead of guessing. Prevents hallucinations — a real concern with production RAG systems.

## 🚀 Run Locally

```bash
# Clone
git clone https://github.com/danushkumarsekar/deutsch-kompagnon
cd deutsch-kompagnon

# Create virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Add your free Groq API key
echo GROQ_API_KEY=gsk_your_key_here > .env

# Run
streamlit run app.py
```

Get a free Groq API key at [console.groq.com](https://console.groq.com).

## 📁 Repository Structure

```
deutsch-kompagnon/
├── app.py                    # Streamlit UI + RAG pipeline
├── requirements.txt          # Python dependencies
├── documents/                # German B2 grammar reference (markdown)
│   ├── 01_cases.md
│   ├── 02_verbs.md
│   ├── 03_prepositions.md
│   ├── 04_subordinate_clauses.md
│   └── 05_passive_conjunctive.md
├── .env                      # Secrets (gitignored)
└── chroma_db/                # Auto-built on first run (gitignored)
```

## 🔮 Roadmap

- [ ] Add conversation memory (query rewriting for follow-ups)
- [ ] Ingest more sources: Deutsche Welle, telc sample papers
- [ ] Add a quiz mode (bot asks the user grammar questions)
- [ ] Speech-to-text input for pronunciation practice
- [ ] Deploy a re-ranker for better retrieval quality

## 👤 Author

**Danush Kumar Sekar** — M.Sc. Big Data & AI, SRH Hochschule Leipzig  
🌐 [GitHub](https://github.com/danushkumarsekar) · 💼 [LinkedIn](https://www.linkedin.com/in/danushkumarsekar) · 📧 danushsekars@gmail.com  
📍 Leipzig, Germany 🇩🇪

Currently exploring **GenAI Application Engineering** and **MLOps** roles.

## 📄 License

MIT License — see [LICENSE](LICENSE)

Weather-style tribute: built weekend nights while grinding through my own B2 prep 🍺
