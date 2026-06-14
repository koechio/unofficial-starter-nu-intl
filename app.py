import gradio as gr
from ingest import read_all_documents, chunk_document
from retriever import embed_and_store, retrieve, get_collection
from generator import generate_response


def run_ingestion():
    """Load, chunk, embed, and store all documents. Skips if already populated."""
    collection = get_collection()
    if collection.count() > 0:
        print(f"Vector store already populated ({collection.count()} chunks). Skipping ingestion.")
        return

    print("Ingesting documents...")
    docs = read_all_documents()
    all_chunks = []
    for doc in docs:
        for text in doc["text"]:
            all_chunks.extend(chunk_document(text, doc["name"]))

    if all_chunks:
        embed_and_store(all_chunks)
        print(f"Ingestion complete. {len(all_chunks)} chunks stored.")
    else:
        print("No chunks produced — check that docs/ contains .txt files.")


def chat(message, history):
    if not message.strip():
        return ""
    chunks = retrieve(message)
    return generate_response(message, chunks)


with gr.Blocks(title="The Unofficial Guide") as demo:

    gr.HTML("""
        <div style="text-align:center; padding:1.25rem 0 0.5rem;">
            <h1 style="font-size:2rem; font-weight:700; color:#4f2d7f; margin:0;">
                The Unofficial Guide
            </h1>
            <p style="color:#6b7280; font-size:1rem; margin:0.4rem 0 0;">
                Answers for international students at Northwestern — SSN, taxes, CPT/OPT, banking, and more.
            </p>
        </div>
    """)

    with gr.Row():
        with gr.Column(scale=3):
            gr.ChatInterface(
                fn=chat,
                chatbot=gr.Chatbot(
                    height=460,
                    placeholder=(
                        "<div style='text-align:center; color:#9ca3af; margin-top:3rem;'>"
                        "Ask anything about life as an international student at Northwestern."
                        "</div>"
                    ),
                ),
                textbox=gr.Textbox(
                    placeholder='e.g. "Do I need an SSN to open a bank account?"',
                    container=False,
                    scale=7,
                ),
                examples=[
                    "Which documents do I need before filing taxes as an F-1 student?",
                    "Do I need to pay for Sprintax at Northwestern?",
                    "Is an SSN required to file taxes?",
                    "What is the difference between CPT and OPT?",
                    "Can I open a US bank account without an SSN?",
                    "How do I apply for an SSN as an F-1 student?",
                    "What are my reporting obligations while on OPT?",
                    "How do I get around Chicago from Evanston?",
                ],
                cache_examples=False,
            )

        with gr.Column(scale=1, min_width=200):
            gr.HTML("""
                <div style="background:#f5f0ff; border:1px solid #d8b4fe;
                            border-radius:10px; padding:1rem; margin-top:0.5rem;">
                    <p style="font-size:0.8rem; font-weight:700; color:#4f2d7f;
                               margin:0 0 0.5rem; letter-spacing:0.05em;">
                        SOURCES
                    </p>
                    <ul style="font-size:0.82rem; color:#5b21b6; list-style:none;
                                padding:0; margin:0; line-height:1.9;">
                        <li>NU OISS: SSN Guide</li>
                        <li>NU OISS: Tax Resources</li>
                        <li>NU OISS: Tax FAQ</li>
                        <li>NU OISS: CPT Guide</li>
                        <li>NU OISS: OPT Guide</li>
                        <li>NU OISS: While on OPT</li>
                        <li>NU OISS: Transportation</li>
                        <li>Sprintax: Form 8843</li>
                        <li>Wise: Bank Account Guide</li>
                        <li>r/f1visa: Tax Megathread</li>
                        <li>r/f1visa: SSN Threads</li>
                    </ul>
                    <hr style="border:none; border-top:1px solid #d8b4fe; margin:0.75rem 0;">
                    <p style="font-size:0.75rem; color:#7c3aed; margin:0; line-height:1.5;">
                        Answers are grounded in the loaded sources only.
                        Citations show which document each answer draws from.
                    </p>
                </div>
            """)


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  The Unofficial Guide — starting up")
    print("=" * 50 + "\n")
    run_ingestion()
    demo.launch(theme=gr.themes.Soft(primary_hue="purple"))
