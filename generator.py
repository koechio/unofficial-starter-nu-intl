from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY)


def generate_response(query, retrieved_chunks):
    """Generate a grounded answer from retrieved chunks using Groq."""
    if not retrieved_chunks:
        return (
            "I couldn't find anything relevant in my sources. "
            "Try rephrasing your question."
        )

    # Filter out weak matches (cosine distance >= 0.7 is too far to be reliable)
    chunks = [c for c in retrieved_chunks if c.get("distance", 1) < 0.7]
    if not chunks:
        return (
            "I don't have enough reliable information in my sources to answer that. "
            "Try asking about SSN, taxes, CPT/OPT, banking, or transportation."
        )

    # Format chunks into a labeled context block
    context = "\n\n".join(
        f"<chunk id='{i}'>\n"
        f"  <source>{c['source']}</source>\n"
        f"  <text>{c['text']}</text>\n"
        f"</chunk>"
        for i, c in enumerate(chunks, 1)
    )

    system_prompt = (
        "You are a knowledgeable friend who has already navigated life as an "
        "international student at Northwestern University. You answer questions "
        "about SSNs, taxes, CPT/OPT work authorization, banking, and campus "
        "transportation based strictly on the provided sources.\n\n"
        "RULES:\n"
        "1. Answer using ONLY the information inside the <context> tags below.\n"
        "2. After each factual claim, cite the source in parentheses, "
        "e.g. (source: nu_oiss_tax_faq).\n"
        "3. If the context does not contain enough information to answer, say: "
        "'I don't have that information in my sources — check the OISS website "
        "or ask an OISS advisor directly.'\n"
        "4. Do not use any outside knowledge. Do not guess.\n"
        "5. Be direct and conversational — answer the question first, then add "
        "any important caveats.\n\n"
        f"<context>\n{context}\n</context>"
    )

    try:
        completion = _client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query},
            ],
            temperature=0.0,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error calling Groq API: {e}"
