import trafilatura
from config import DOCS_PATH

SOURCES = [
    {"name": "nu_oiss_ssn_guide",        "url": "https://www.northwestern.edu/international/resources/social-security/how-to-apply-for-an-ssn.html"},
    {"name": "nu_oiss_tax_resources",    "url": "https://www.northwestern.edu/international/resources/taxes/oiss-tax-resources.html"},
    {"name": "nu_oiss_cpt_guide",        "url": "https://www.northwestern.edu/international/international-students/student-employment/cpt-for-f1-students.html"},
    {"name": "nu_oiss_opt_guide",        "url": "https://www.northwestern.edu/international/international-students/student-employment/opt-f1-students/"},
    {"name": "nu_oiss_tax_faq",          "url": "https://www.northwestern.edu/international/resources/taxes/tax-faqs.html"},
    {"name": "sprintax_form8843",        "url": "https://blog.sprintax.com/tax-form-8843-filing-instructions/"},
    {"name": "wise_bank_account_guide",  "url": "https://wise.com/us/blog/chase-open-account-non-resident"},
    {"name": "reddit_f1_visa_tax",       "url": None},  # pre-saved manually as docs/reddit_f1_visa_tax.txt
    {"name": "reddit_f1_visa_ssn",       "url": None},  # pre-saved manually as docs/reddit_f1_visa_ssn.txt
    {"name": "nu_oiss_transportation",   "url": "https://www.northwestern.edu/offcampus/resources/getting-around/public-trainbus-transportation.html"},
    {"name": "nu_oiss_while_on_opt",     "url": "https://www.northwestern.edu/international/international-students/student-employment/while-on-opt-stem-opt1/while-on-opt.html"},
]


def fetch_and_save(source):
    """Fetch a web source with trafilatura and write cleaned text to docs/<name>.txt."""
    downloaded = trafilatura.fetch_url(source["url"])
    text = trafilatura.extract(downloaded) or ""
    txt_path = f"{DOCS_PATH}/{source['name']}.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)
    return len(text)


def save_all_to_txt():
    """One-time fetch: download every web source and save it as a .txt file.
    Reddit sources are already saved manually and are skipped."""
    for source in SOURCES:
        if source["url"] is None:
            print(f"Skipping {source['name']} (pre-saved).")
            continue
        print(f"Fetching {source['name']}...")
        try:
            char_count = fetch_and_save(source)
            print(f"  -> {char_count:,} chars saved to docs/{source['name']}.txt")
        except Exception as e:
            print(f"  -> FAILED: {e}")


def read_document(source):
    """Read a source from its local .txt file."""
    txt_path = f"{DOCS_PATH}/{source['name']}.txt"
    with open(txt_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    return {"name": source["name"], "text": [text] if text.strip() else []}


def read_all_documents():
    """Load all sources from their saved .txt files."""
    documents = []
    for source in SOURCES:
        print(f"Reading {source['name']}...")
        try:
            doc = read_document(source)
            char_count = sum(len(t) for t in doc["text"])
            print(f"  -> {char_count:,} chars")
            documents.append(doc)
        except Exception as e:
            print(f"  -> FAILED: {e}")
    return documents


if __name__ == "__main__":
    save_all_to_txt()
    print("\nDone. All web sources saved to docs/.")
