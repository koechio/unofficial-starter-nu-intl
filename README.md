# The Unofficial Guide — Project 1

---

## Domain

This system covers practical life navigation for international students at Northwestern University — specifically SSN applications, federal tax filing as an F-1/J-1 student, CPT/OPT work authorization, opening a US bank account without an established credit history, and getting around Chicago via public transit.

This knowledge is genuinely hard to access. It's scattered across the OISS website, IRS publications, third-party guides, and Reddit threads. A simple question like "do I need an SSN to file taxes?" requires multiple Google searches, landing on the right page, and reading several paragraphs to extract a one-sentence answer. The goal of this system is to simulate a knowledgeable friend who has been through the process and can give a direct, cited answer immediately.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | NU OISS: How to apply for SSN | Official | https://www.northwestern.edu/international/resources/social-security/how-to-apply-for-an-ssn.html |
| 2 | NU OISS: Tax filing resources & Sprintax guide | Official | https://www.northwestern.edu/international/resources/taxes/oiss-tax-resources.html |
| 3 | NU OISS: CPT for F-1 students | Official | https://www.northwestern.edu/international/international-students/student-employment/cpt-for-f1-students.html |
| 4 | NU OISS: OPT for F-1 students | Official | https://www.northwestern.edu/international/international-students/student-employment/opt-f1-students/ |
| 5 | NU OISS: Tax FAQ page | Official | https://www.northwestern.edu/international/resources/taxes/tax-faqs.html |
| 6 | Sprintax blog: Form 8843 explainer | 3rd party | https://blog.sprintax.com/tax-form-8843-filing-instructions/ |
| 7 | Wise blog: Opening a US bank account as a non-resident | 3rd party | https://wise.com/us/blog/chase-open-account-non-resident |
| 8 | r/f1visa — Tax Question Megathread 2025 | Community | https://www.reddit.com/r/f1visa/comments/1qvvadf/tax_question_megathread_2025_tax_submissions/ |
| 9 | r/f1visa — SSN Threads | Community | https://www.reddit.com/r/f1visa/ |
| 10 | NU Off-Campus: Public train/bus transportation | Official | https://www.northwestern.edu/offcampus/resources/getting-around/public-trainbus-transportation.html |
| 11 | NU OISS: While on OPT | Official | https://www.northwestern.edu/international/international-students/student-employment/while-on-opt-stem-opt1/while-on-opt.html |

---

## Document Ingestion

All sources are fetched once and saved as `.txt` files in `docs/`. The Reddit community threads (`reddit_f1_visa_tax.txt`, `reddit_f1_visa_ssn.txt`) were saved manually in advance. All other sources are fetched using `trafilatura`, which downloads the HTML and strips boilerplate to return clean body text. Running `python ingest.py` re-fetches and overwrites the web sources; Reddit files are skipped automatically.

**Why trafilatura instead of PDFs:** The original plan was to download PDFs from Northwestern's site and parse them with `pdfplumber`. This failed because browser-printed PDFs embed content as rendered image layers rather than selectable text objects — `pdfplumber` returned empty strings for every page. Fetching the live HTML directly avoids this entirely.

---

## Chunking Strategy

**Chunk size:** 500 characters

**Overlap:** 75 characters

**Why these choices fit your documents:** The OISS pages are short (4k–21k chars) and structured as headed sections with bullet-point lists — a 500-char window captures one complete policy statement or procedural step. The Reddit threads are very long (640k–717k chars) and consist of standalone Q&A comments; 500 chars fits a full comment or reply. The 75-char overlap ensures that a sentence split across a chunk boundary can still be retrieved intact. Chunks under 50 chars are discarded as whitespace artifacts. No additional HTML cleaning was needed because `trafilatura` strips all markup before saving.

**Final chunk count:** 1,915 chunks across all 11 sources.

---

## Sample Chunks

**Chunk 1** — `nu_oiss_ssn_guide`
```
How to apply for an SSN
Who can apply for an SSN & required documentation
| Visa/Employment Type | Eligible? | Required Documentation |
| Newly arrived F-1 or J-1 student who is not yet enrolled in classes and/or has not yet
completed OISS check-in (Initial SEVIS Status) | Not yet eligible | Newly arrived students
must complete OISS check-in and be registered in classes at NU before OISS can update your
SEVIS status to Active.
```

**Chunk 2** — `nu_oiss_tax_resources`
```
l students and scholars and walks through the filing process. Step 2: Receive Your Sprintax
Access Code OISS distributes Sprintax access codes by email to eligible F-1 and J-1 students
and scholars. This access code waives the federal tax preparation fee. Once you receive your
access code, you can create a Sprintax account and begin preparing your tax return.
```

**Chunk 3** — `nu_oiss_cpt_guide`
```
Curricular Practical Training (CPT) is temporary work authorization required for any
off-campus work, paid or unpaid, during an F-1 student's academic program. CPT must be
directly related to your major field of study and authorized by your DSO before the
employment begins. Working without valid CPT authorization is a serious violation of your
F-1 status.
```

**Chunk 4** — `wise_bank_account_guide`
```
ccount with Chase. We'll cover all the documents needed in detail later, but the key
requirements to know about include: a foreign passport, a US visa, proof of a US address,
and an Individual Taxpayer Identification Number (ITIN) or Social Security Number (SSN).
In some cases Chase may accept an ITIN as an alternative to an SSN for non-residents.
```

**Chunk 5** — `reddit_f1_visa_tax`
```
For those asking about Sprintax — Northwestern gives you a free access code through OISS.
Check your email from international@northwestern.edu around February. You don't pay anything
for the federal return. Some states charge extra but the federal filing is covered. Make sure
you're using the nonresident version, not TurboTax — TurboTax will file you as a resident
which is wrong for most F-1 students in their first 5 years.
```

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` via `sentence-transformers`. This model runs entirely locally — no API key, no rate limits, and no per-query cost. It maps text to 384-dimensional vectors and performs well on short to medium passages.

**Production tradeoff reflection:** In a real deployment, I would weigh four tradeoffs. First, **multilingual support** — students may phrase questions mixing English with their native language; a model like `paraphrase-multilingual-MiniLM-L12-v2` would handle this better. Second, **domain accuracy** — immigration and tax language is jargon-heavy; a larger model like OpenAI's `text-embedding-3-large` would retrieve more precisely on domain-specific terminology. Third, **context length** — `all-MiniLM-L6-v2` silently truncates input beyond 256 tokens, which cuts off long Reddit comments; a model with a longer context window would encode full posts. Fourth, **latency** — a local model has zero network overhead but is slower on CPU; an API-hosted model adds a round-trip but offloads compute and scales with demand.

---

## Retrieval Test Results

**Query 1:** "Which documents do I need before filing taxes as an F-1 student?"

| Rank | Source | Distance | Chunk preview |
|------|--------|----------|---------------|
| 1 | `nu_oiss_tax_faq` | 0.395 | "...international student/scholar and I did not have job or any other earned income in the most recent tax year. Do I still need to file..." |
| 2 | `nu_oiss_tax_faq` | 0.419 | "...please reference our How to File U.S. Taxes pages to determine your residency status and how to file based on that determination..." |
| 3 | `nu_oiss_tax_faq` | 0.422 | "...need to file a federal tax return with the IRS. Depending on your individual circumstances, you may also need to file a state return..." |

All three results come from `nu_oiss_tax_faq`, which is directly relevant. The chunks address filing obligations and residency status. The specific document checklist (passport, I-20, W-2) lives in `nu_oiss_tax_resources` and did not make the top 3 — this is a meaningful retrieval limitation.

---

**Query 2:** "Do I need to pay for Sprintax at Northwestern?"

| Rank | Source | Distance | Chunk preview |
|------|--------|----------|---------------|
| 1 | `nu_oiss_tax_resources` | 0.485 | "...Northwestern's Office of International Student and Scholar Services (OISS) coordinates access to..." |
| 2 | `nu_oiss_tax_resources` | 0.528 | "...OISS distributes Sprintax access codes by email to eligible F-1 and J-1 students and scholars..." |
| 3 | `nu_oiss_tax_resources` | 0.529 | "...Tax & Income Documents (if applicable): For more information on which tax forms you may need for Sprintax..." |

All results from `nu_oiss_tax_resources`, the authoritative NU source for this question. Chunk 2 contains the exact answer. The results are tightly clustered (0.485–0.529), indicating high semantic relevance.

---

**Query 3:** "Can I open a US bank account without an SSN?"

| Rank | Source | Distance | Chunk preview |
|------|--------|----------|---------------|
| 1 | `wise_bank_account_guide` | 0.420 | "...the key requirements to know about include: a foreign passport, a US visa, proof of a US address, and an ITIN or SSN..." |
| 2 | `wise_bank_account_guide` | 0.453 | "...Foreign US residents and non-residents with a US address can open Chase checking accounts, subject to meeting any other requirements..." |
| 3 | `wise_bank_account_guide` | 0.477 | "...but the exact paperwork that can be accepted may vary based on your personal situation..." |

All results from `wise_bank_account_guide`. This source directly answers the question — ITIN can substitute for SSN. The retrieval correctly ignored the OISS sources which don't cover banking.

---

## Grounded Generation

**System prompt grounding instruction:** The system prompt opens by framing the assistant as "a knowledgeable friend who has already navigated life as an international student at Northwestern University." It then enforces four hard rules: (1) answer using ONLY the information inside `<context>` tags; (2) after each factual claim, cite the source in parentheses — e.g., `(source: nu_oiss_tax_faq)`; (3) if the context doesn't contain enough information, say so explicitly and direct the user to OISS; (4) do not use outside knowledge or guess. Temperature is set to 0.0 to prevent creative drift.

**How source attribution is surfaced in the response:** Source names are injected into a `<source>` tag inside each `<chunk>` block passed as context. The model is instructed to cite the source name after every factual claim. This means attribution is enforced at the prompt level — the model must label each claim or it violates instruction 2.

**Structural filtering:** Before generation, chunks with cosine distance ≥ 0.7 are filtered out. If all retrieved chunks exceed this threshold, the system returns a canned message directing the user to OISS rather than attempting to generate from weak context.

---

## Example Responses

**Example 1 — Accurate, grounded response**

> Query: "Do I need to pay for Sprintax as an F-1 student at Northwestern?"
>
> Response: "As an F-1 student at Northwestern, you don't need to pay for Sprintax because OISS distributes Sprintax access codes by email to eligible F-1 and J-1 students and scholars, which waives the federal tax preparation fee (source: nu_oiss_tax_resources)."

---

**Example 2 — Accurate, grounded response**

> Query: "Is it required to have an SSN before filing taxes?"
>
> Response: "No, it's not required to have an SSN to file taxes, specifically Form 8843 (source: sprintax_form8843). You will not need a Social Security Number or Individual Tax Identification Number unless you have been assigned one (source: sprintax_form8843). However, if you have been assigned an SSN or ITIN, you must include it on Form 8843 (source: sprintax_form8843)."

---

**Example 3 — Out-of-scope refusal**

> Query: "What are the best dining halls at Northwestern?"
>
> Response: "I don't have that information in my sources — check the OISS website or ask an OISS advisor directly."

The dining question has no relevant content in any of our 11 documents. All retrieved chunks exceed the 0.7 distance threshold, so the system returns the refusal message rather than generating a plausible-sounding answer from weak context.

---

## Query Interface

The interface is a Gradio web UI launched by running `python app.py`. It opens at `http://localhost:7860`.

**Input:** A freeform text box labeled with the placeholder "e.g. Do I need an SSN to open a bank account?" Eight example questions are pre-loaded as clickable buttons below the chat window.

**Output:** A chat response with factual claims cited by source name (e.g., `source: nu_oiss_tax_faq`). The right sidebar lists all 11 loaded sources so users know what the system covers.

**Sample interaction:**

```
User: How do I apply for an SSN as an F-1 student?

System: To apply for an SSN as an F-1 student, you must first be in Active SEVIS status,
which requires completing OISS check-in and being registered in classes at Northwestern
(source: nu_oiss_ssn_guide). You must also have qualifying employment — eligible categories
include on-campus employment, CPT, and OPT (source: nu_oiss_ssn_guide). Newly arrived
students in Initial SEVIS Status are not yet eligible and must wait until after both
registering for classes and completing OISS check-in (source: nu_oiss_ssn_guide).
```

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Which documents do I need before filing taxes as an F-1 student? | Passport, I-94, I-20, SSN/ITIN (if applicable), W-2, 1042-S, 1099 | Explained Form 8843 filing obligation and Sprintax access correctly, then admitted: "the context does not provide a specific list of documents required" (source: nu_oiss_tax_faq) | Partially relevant | Partially accurate |
| 2 | Do I need to pay for Sprintax as an F-1 student at Northwestern? | No — OISS provides free access codes | No, OISS distributes Sprintax access codes that waive the federal fee (source: nu_oiss_tax_resources) | Relevant | Accurate |
| 3 | Is it required to have an SSN before filing taxes? | No — ITIN works; Form 8843 needs neither | Not required; SSN/ITIN only needed if you have income or were already assigned one (source: sprintax_form8843) | Relevant | Accurate |
| 4 | What is the difference between CPT and OPT? | CPT = in-program off-campus work tied to curriculum; OPT = 12-month post-completion authorization | System acknowledged it lacked a direct comparison; noted CPT full-time use affects OPT eligibility (source: nu_oiss_opt_guide) | Partially relevant | Partially accurate |
| 5 | Can I open a US bank account without an SSN? | Yes — passport, visa, I-20, proof of address; ITIN accepted in lieu of SSN | Yes; Chase accepts ITIN as alternative to SSN; exact paperwork varies by situation (source: wise_bank_account_guide) | Relevant | Accurate |

---

## Failure Case Analysis

**Question that failed:** "What is the difference between CPT and OPT?"

**What the system returned:** The model acknowledged it lacked enough information for a direct comparison, then added a partial observation: that using more than one year of full-time CPT disqualifies you from OPT (source: nu_oiss_opt_guide). This is accurate but incomplete.

**Root cause (tied to a specific pipeline stage):** Retrieval failure at the chunking stage. Both the CPT guide and OPT guide are stored as separate documents. The top-5 retrieved chunks for this query all came from `nu_oiss_opt_guide` — the query's semantic similarity pulled heavily toward OPT content. No chunk from `nu_oiss_cpt_guide` made the top 5. Because the system only sees the retrieved chunks, it could not produce a comparison it was never given both sides of.

**What you would change to fix it:** Two options: (1) increase top-k further (e.g., to 8–10) so both documents have a chance to appear in the context window for comparison queries; (2) add a metadata filter that explicitly retrieves at least one chunk from each of the two relevant source documents when the query contains multiple named topics.

---

## Spec Reflection

**One way the spec helped you during implementation:** Writing the Chunking Strategy section before touching any code forced a specific decision — 500 chars, 75 overlap, 50 min — before implementation. When Claude was given that section as a prompt to implement `chunk_document()`, it produced the exact function needed on the first attempt without revision. Without the spec, the prompt would have been "write a chunking function" and the output would have required multiple rounds of correction to match the actual document structure.

**One way your implementation diverged from the spec, and why:** The original ingestion plan used `pdfplumber` to extract text from PDFs downloaded from Northwestern's website. This failed because browser-printed PDFs embed content as rendered image layers rather than selectable text — `pdfplumber` returned empty strings for every page. The implementation switched to `trafilatura`, which fetches the live HTML and strips boilerplate directly. The rest of the pipeline (chunking, embedding, retrieval, generation) was unaffected because the output format — clean plain text per source — stayed the same.

---

## AI Usage

**Instance 1**

- *What I gave the AI:* The Chunking Strategy section of planning.md (chunk_size=500, overlap=75, min_length=50, output format `{text, source, chunk_id}`) and the `read_all_documents()` return format.
- *What it produced:* A `chunk_document(text, source_name)` function using a character sliding window with the exact parameters specified.
- *What I changed or overrode:* Nothing — the spec was specific enough that the output matched without revision. Verified by printing chunk counts (1,915 total) and spot-checking 3 chunks from `nu_oiss_ssn_guide` to confirm complete sentences and correct source names.

**Instance 2**

- *What I gave the AI:* The Retrieval Approach section of planning.md, the chunk dict format from Instance 1, and the `retriever.py` pattern from the rulesbot-starter reference project as a structural reference.
- *What it produced:* `embed_and_store()` and `retrieve()` in `retriever.py` using ChromaDB with `all-MiniLM-L6-v2` and cosine similarity.
- *What I changed or overrode:* Bumped `N_RESULTS` from 3 to 5 after testing showed that comparison questions (e.g., CPT vs OPT) failed when the top 3 results came entirely from one document. The spec said top-k=3 but real evaluation revealed this was too narrow for multi-topic queries.
