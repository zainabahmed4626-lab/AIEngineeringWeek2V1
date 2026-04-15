# Textbook RAG Assistant (LangChain + Chroma + OpenAI)

End-to-end **Retrieval-Augmented Generation (RAG)** system built for **Applied AI Engineering** workflows: ingest PDF textbooks, chunk + enrich metadata, embed into a vector database, evaluate retrieval quality, and ship a lightweight **Gradio** UI for interactive Q&A.

**Live repo:** https://github.com/zainabahmed4626-lab/AIEngineeringWeek2V1

---

## What this project demonstrates 

- **Production-shaped RAG**: not “call an LLM”—a full pipeline from documents → chunks → embeddings → retrieval → grounded answers.
- **Grounding + safety posture**: answers are constrained to retrieved context with an explicit fallback when evidence is insufficient.
- **Retrieval engineering**: hybrid retrieval (**vector similarity + BM25**) and **metadata-aware filtering** hooks (source / section / date).
- **Evaluation discipline**: a small eval loop reporting retrieval / faithfulness / correctness style signals (assignment-oriented, extensible).
- **Product thinking**: a simple **Gradio** interface for manual testing, plus debug panels to inspect retrieved chunks.

---

## Architecture (high level)
<img width="1920" height="991" alt="image" src="https://github.com/user-attachments/assets/028fc97a-ca7f-4777-b332-59e8587d504f" />

  PDFs[PDF textbooks] --> Load[LangChain PDF loader]
  Load --> Chunk[RecursiveCharacterTextSplitter + metadata]
  Chunk --> Embed[HuggingFace embeddings]
  Embed --> VS[Chroma vector store]
  VS --> RetV[Vector retriever]
  Chunk --> RetB[BM25 retriever]
  RetV --> Ens[Ensemble retriever]
  RetB --> Ens
  Ens --> QA[RetrievalQA (OpenAI chat)]
  QA --> UI[Gradio UI]
```

---

## Tech stack

- **Orchestration**: LangChain (`RetrievalQA`, prompts, retrievers)
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2` (via LangChain community integrations)
- **Vector DB**: Chroma (persistent store)
- **Hybrid retrieval**: BM25 (`rank-bm25`) + dense vectors (`EnsembleRetriever`)
- **LLM**: OpenAI chat model (`gpt-3.5-turbo`, temperature configurable)
- **UI**: Gradio
- **Notebook**: `rag1.ipynb` (single runnable artifact for the assignment)

---

## Key features implemented

- **Step 1 — Load**: PDF ingestion + sanity prints (document count + preview)
- **Step 2 — Chunk**: `RecursiveCharacterTextSplitter` with two chunking experiments + stats
- **Step 3 — Embed + Store**: embeddings persisted to Chroma (`./chroma_db`, collection `textbook_rag`)
- **Step 4 — Retrieval test**: `similarity_search` with annotated relevance notes
- **Step 5 — RAG chain**: `RetrievalQA` + custom prompt + retriever tuning
- **Step 6 — Evaluation**: mini eval set + structured reporting + aggregate scores
- **Hybrid retrieval**: vector + BM25 ensemble for stronger keyword coverage
- **Metadata enrichment**: `source`, `section`, `date` on chunks + optional filtered retrieval path
- **UX polish**: greeting handling in the Gradio path for a friendlier chat experience

---

## Quickstart (local)

### 1) Prerequisites

- Python 3.10+ recommended (your notebook metadata may show newer; adjust if needed)
- OpenAI API access

### 2) Configure secrets locally

Create a `.env` file in the project folder:

```bash
OPENAI_API_KEY=...your key...
```

This repo intentionally **does not** commit `.env`.

### 3) Add your PDFs

Place these next to `rag1.ipynb` (not committed here):

- `textbook_1.pdf`
- `textbook_2.pdf`

### 4) Run the notebook

Open `rag1.ipynb` and run cells **in order** (setup → load → chunk → embed → retrieval tests → RAG → eval → optional UI).

---

## Observations — What Worked, What Didn’t, What I’d Improve 
**What Worked**
The combination of metadata filtering + hybrid retrieval (BM25 + vector search) noticeably improved relevance, especially for definition‑heavy sections.
Chunking at 500 characters produced more accurate retrieval for specific questions.
The custom grounding prompt kept answers concise and reduced hallucinations.

**What Didn’t Work**
Some textbook sections still produced noisy chunks due to headers, footers, and formatting artifacts.
A few queries returned context that was technically related but not the most precise match.

**What I’d Improve**
Clean the PDF text further before chunking to remove repeated structural elements.
Experiment with stronger embedding models to improve semantic matching.
Add lightweight evaluation automation to speed up iteration.

---

## Optional helper script

`build_github_push_payload.py` generates a JSON payload for GitHub uploads. It is **not** required to run the RAG notebook.
