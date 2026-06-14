# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain
The domain I chose is practical life navigation for international students at Northwestern University —specifically SSN applications, federal tax filing as an F-1/J-1 student, work authorization (CPT/OPT), and opening a US bank account without an established credit history or SSN.These are Some of the topics that most international have questions about

Accessing this knowledge is frustrating in practice: it takes multiple Google searches just to land on the right page, and once you're there, the answer to your specific question is buried several paragraphs down. The information is also scattered across the OISS website, IRS publications, Sprintax guides, and community forums. Having to do all this just for a simple question is really annoying

My goal was to simulate a very knowledgeable international friend, someone who has already been through the process and can give you a direct answer to your specific question, explain how different pieces connect, and point you to the right official resource if you need more
detail.
c

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

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

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

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
