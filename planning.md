# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain
The domain I chose is practical life navigation for international students at Northwestern University —specifically SSN applications, federal tax filing as an F-1/J-1 student, work authorization (CPT/OPT), and opening a US bank account without an established credit history or SSN.These are Some of the topics that most international have questions about

Accessing this knowledge is frustrating in practice: it takes multiple Google searches just to land on the right page, and once you're there, the answer to your specific question is buried several paragraphs down. The information is also scattered across the OISS website, IRS publications, Sprintax guides, and community forums. Having to do all this just for a simple question is really annoying

My goal was to simulate a very knowledgeable international friend, someone who has already been through the process and can give you a direct answer to your specific question, explain how different pieces connect, and point you to the right official resource if you need more detail.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Type | Description | URL | Local File |
|---|--------|------|-------------|-----|------------|
| 1 | NU OISS: How to apply for SSN | Official | Step-by-step guide for F-1 students on obtaining a Social Security Number | https://www.northwestern.edu/international/resources/social-security/how-to-apply-for-an-ssn.html | docs/nu_oiss_ssn_guide.pdf |
| 2 | NU OISS: Tax filing resources & Sprintax guide | Official | Overview of tax obligations and Sprintax software instructions for international students | https://www.northwestern.edu/international/resources/taxes/oiss-tax-resources.html | docs/nu_oiss_tax_resources.pdf |
| 3 | NU OISS: CPT for F-1 students | Official | Curricular Practical Training eligibility, application process, and employer requirements | https://www.northwestern.edu/international/international-students/student-employment/cpt-for-f1-students.html | docs/nu_oiss_cpt_guide.pdf |
| 4 | NU OISS: OPT for F-1 students | Official | Optional Practical Training application timeline, STEM extension, and reporting requirements | https://www.northwestern.edu/international/international-students/student-employment/opt-f1-students/ | docs/nu_oiss_opt_guide.pdf |
| 5 | NU OISS: Tax FAQ page | Official | Frequently asked questions on tax residency status, treaties, and filing deadlines | https://www.northwestern.edu/international/resources/taxes/tax-faqs.html | docs/nu_oiss_tax_faq.pdf |
| 6 | Sprintax blog: Form 8843 explainer | 3rd party | Instructions for completing Form 8843 (exempt individual statement for nonresident aliens) | https://blog.sprintax.com/tax-form-8843-filing-instructions/ | docs/sprintax_form8843.pdf |
| 7 | Wise blog: Opening a US bank account as a non-resident | 3rd party | Guide on opening a Chase bank account without a SSN, covering required documents and alternatives | https://wise.com/us/blog/chase-open-account-non-resident | docs/wise_bank_account_guide.pdf |
| 8 | r/f1visa — Tax Question Megathread 2025 | Community | Crowdsourced Q&A on 2025 tax filing, treaty benefits, and Sprintax tips from F-1 students | https://www.reddit.com/r/f1visa/comments/1qvvadf/tax_question_megathread_2025_tax_submissions/ | docs/reddit_f1_visa_tax.pdf |
| 9 | r/f1visa — SSN Threads | Community | Reddit threads discussing SSN application experiences, denials, and workarounds for F-1 students | https://www.reddit.com/r/f1visa/ | docs/reddit_f1_visa_ssn.pdf |
| 10 | NU Off-Campus: Public train/bus transportation | Official | Guide to CTA, Metra, and Pace transit options for getting around the Chicago area from Northwestern | https://www.northwestern.edu/offcampus/resources/getting-around/public-trainbus-transportation.html | docs/nu_oiss_transportation.pdf |
| 11 | NU OISS: While on OPT | Official | Obligations, reporting requirements, and tips for maintaining F-1 status while working on OPT | https://www.northwestern.edu/international/international-students/student-employment/while-on-opt-stem-opt1/while-on-opt.html | docs/nu_oiss_while_on_opt.pdf |

---

## Document Ingestion

**Approach:** All sources are fetched once and saved as `.txt` files in `docs/`. The Reddit files (`reddit_f1_visa_tax.txt`, `reddit_f1_visa_ssn.txt`) were saved manually in advance. All other sources are fetched via `trafilatura`, which downloads the page and strips HTML/boilerplate to return clean body text.

**Why trafilatura:** The original plan was to download PDFs and extract text with `pdfplumber`. This failed because Northwestern's pages were printed to PDF from a browser, which embeds content as rendered image layers rather than selectable text — `pdfplumber` returned empty strings for every page. Switching to live web scraping with `trafilatura` solved this cleanly: the underlying HTML has structured, selectable text.

**How to re-fetch:** Delete the `.txt` files and re-run `python ingest.py`. The script skips pre-saved Reddit files automatically.

**Fetched sources and sizes:**

| Source | Chars |
|--------|-------|
| nu_oiss_ssn_guide | 4,392 |
| nu_oiss_tax_resources | 4,318 |
| nu_oiss_cpt_guide | 8,027 |
| nu_oiss_opt_guide | 21,343 |
| nu_oiss_tax_faq | 6,168 |
| sprintax_form8843 | 7,650 |
| wise_bank_account_guide | 9,516 |
| reddit_f1_visa_tax | 717,963 (pre-saved) |
| reddit_f1_visa_ssn | 640,377 (pre-saved) |
| nu_oiss_transportation | 1,838 |
| nu_oiss_while_on_opt | 21,318 |

---

## Chunking Strategy

**Chunk size:** 500 characters

**Overlap:** 75 characters

**Reasoning:** The OISS pages are short (4k–21k chars) and structured as headed sections with bullet-point lists — a 500-char window captures one complete policy statement or procedural step without pulling in unrelated content from adjacent sections. The Reddit threads are very long (640k–717k chars) and consist of standalone Q&A comments; 500 chars is enough to hold a full comment or reply. The 75-char overlap ensures that a sentence split across a chunk boundary can still be retrieved intact — e.g., a tax deadline that starts at the end of one chunk and finishes at the start of the next won't be lost. Chunks shorter than 50 chars are discarded as noise (whitespace artifacts, isolated headers).

**Final chunk count:** 1,915 chunks across all 11 sources (11–51 per official page, 807–904 per Reddit file).

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** `all-MiniLM-L6-v2` via `sentence-transformers` (runs locally, no API key required)

**Top-k:** 3 chunks per query

**Production tradeoff reflection:** `all-MiniLM-L6-v2` maps text to 384-dimensional vectors and runs locally with no cost or latency from network calls — good for a class project. In a real deployment serving international students, the tradeoffs I would weigh are: (1) **multilingual support** — students may phrase questions mixing English with their native language; a multilingual model like `paraphrase-multilingual-MiniLM-L12-v2` would handle this; (2) **domain accuracy** — immigration and tax language is jargon-heavy; a larger model like OpenAI's `text-embedding-3-large` or a fine-tuned legal/government model would retrieve more precisely; (3) **context length** — Reddit comments can be long; `all-MiniLM-L6-v2` has a 256-token cap and silently truncates, so a model with a longer context window (e.g., `text-embedding-3-large` at 8191 tokens) would encode full comments rather than cut them off; (4) **latency** — a local model has zero network latency but is slower on CPU; an API-hosted model adds a round-trip but offloads compute.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Which documents do I need to gather before I start filing my taxes as an international student on an F-1 visa? | Passport, I-94 travel history, Form I-20, SSN or ITIN (if applicable). Income documents: W-2, 1042-S, 1099. An SSN/ITIN is not required if you only need to file Form 8843 (no U.S. income). |
| 2 | Do I need to pay for Sprintax as an F-1 student at Northwestern? | No. Northwestern OISS provides Sprintax access codes to international students at no cost. |
| 3 | Is it required to have an SSN before filing taxes? | No. If you have U.S. income but no SSN, you can apply for an ITIN instead. If you had no U.S. income, you only need to file Form 8843 and no SSN or ITIN is required at all. |
| 4 | What is the difference between CPT and OPT? | CPT (Curricular Practical Training) is temporary off-campus work authorization tied to the curriculum — required for any paid or unpaid off-campus work during the degree program. OPT (Optional Practical Training) is a 12-month post-completion work authorization for F-1 students who have been enrolled full-time for at least one academic year and want to work in their field of study after graduation. STEM graduates can extend OPT by 24 months. |
| 5 | Can I open a US bank account as an international student without an SSN? | Yes. Banks like Chase allow non-residents to open an account using a passport, visa, I-20, and proof of address. An SSN is not required at account opening, though some banks ask for it later once obtained. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. **Chunk boundary splits critical lists.** The tax document checklist (passport, I-20, W-2, 1042-S, etc.) is a bullet-point list that spans several hundred characters. A 500-char window could cut the list in half, returning only some of the required documents. A student who asks "what do I need for taxes?" might get a partial answer. Mitigation: the 75-char overlap helps bridge splits, and top-k=3 retrieves multiple chunks so the full list is more likely to be covered across them.

2. **Reddit noise drowning out authoritative answers.** The Reddit `.txt` files are 640k–717k chars of mixed-quality community content — speculation, outdated advice, and off-topic tangents mixed with useful first-hand accounts. Because there is so much Reddit text, retrieval may favor a vague Reddit comment over a precise OISS answer simply because it matches more surface-level keywords. Mitigation: the grounded system prompt instructs the model to use only the retrieved context and cite the source, so low-quality Reddit chunks will produce visibly weak answers that can be caught during evaluation.

---

## Architecture

```
docs/*.txt  (pre-saved via trafilatura + manual Reddit export)
      │
      ▼
[1] INGEST — ingest.py
    read_all_documents() reads each .txt file into {name, text}
      │
      ▼
[2] CHUNK — ingest.py
    chunk_document() — character sliding window
    chunk_size=500, overlap=75, min_length=50
    output: [{text, source, chunk_id}, ...]
      │
      ▼
[3] EMBED + STORE — retriever.py
    sentence-transformers: all-MiniLM-L6-v2 (local, 384-dim)
    ChromaDB persistent collection (cosine similarity)
    runs once at startup; skipped if collection already populated
      │
      ▼
[4] RETRIEVE — retriever.py
    retrieve(query) → semantic search → top-3 chunks
    returns [{text, source, distance}, ...]
      │
      ▼
[5] GENERATE — generator.py
    Groq API — llama-3.3-70b-versatile
    system prompt: grounded to <context> block, cite source per claim
    temperature=0.0 for deterministic factual output
      │
      ▼
[6] UI — app.py
    Gradio ChatInterface — chat history, example questions
```

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
- Tool: Claude (Claude Code in the terminal)
- Input: the Chunking Strategy section of this file (chunk_size=500, overlap=75, min_length=50) and the `read_all_documents()` return format
- Expected output: `chunk_document(text, source_name)` function in `ingest.py` that returns a list of `{text, source, chunk_id}` dicts
- Verification: print total chunk count and spot-check 3–5 chunks from `nu_oiss_ssn_guide` to confirm they contain complete sentences and the correct source name

**Milestone 4 — Embedding and retrieval:**
- Tool: Claude (Claude Code in the terminal)
- Input: the Retrieval Approach section of this file, the chunk dict format from Milestone 3, and the `retriever.py` pattern from the rulesbot-starter reference project
- Expected output: `embed_and_store(chunks)` and `retrieve(query)` in `retriever.py`, using ChromaDB with `all-MiniLM-L6-v2`
- Verification: query "what documents do I need for taxes?" and confirm the top-3 returned chunks come from tax-related sources (`nu_oiss_tax_resources`, `nu_oiss_tax_faq`, `sprintax_form8843`)

**Milestone 5 — Generation and interface:**
- Tool: Claude (Claude Code in the terminal)
- Input: the Architecture section of this file, the `generate_response()` and `app.py` pattern from rulesbot-starter, and the 5 evaluation questions
- Expected output: `generate_response(query, chunks)` in `generator.py` with a grounded system prompt and source citations; `app.py` with a Gradio ChatInterface adapted for this domain
- Verification: run all 5 evaluation questions through the live app and compare responses against expected answers in the Evaluation Plan
