"""ChatGPT Conversation Splitter
Convert conversations.json (from OpenAI export) into one Markdown
file per chat, plus a lightweight SQLite full‑text index (optional).

Usage:
    python split_chats.py conversations.json [--fts]

Outputs:
    out/                                    # folder
        YYYY‑MM‑DD_title‑slug.md            # one per conversation
    chats.db  (if --fts)                    # SQLite DB with FTS5 table
"""

import argparse, json, re, os, pathlib, datetime as dt, sqlite3, unicodedata

def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode()
    text = re.sub(r'[^a-zA-Z0-9]+', '-', text).strip('-').lower()
    return text[:60] or "chat"

def ts(epoch):
    return dt.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d')

def main(source, use_fts=False):
    data = json.loads(pathlib.Path(source).read_text())
    # Handle both direct list of conversations and {"conversations": [...]} format
    conversations = data if isinstance(data, list) else data.get("conversations", [])
    out = pathlib.Path("out")
    out.mkdir(exist_ok=True)
    docs = []
    for conv in conversations:
        title = conv.get("title", "Conversation")
        date = ts(conv["create_time"])
        slug = slugify(title)
        path = out / f"{date}_{slug}.md"
        messages = []
        for node in conv.get("mapping", {}).values():
            msg = node.get("message")
            if not msg:
                continue
            role = msg.get("author", {}).get("role", "unknown").upper()
            parts = msg.get("content", {}).get("parts", [""])
            # Handle both string and dictionary parts
            text_parts = []
            for part in parts:
                if isinstance(part, dict):
                    # If it's a dictionary, try to get the text content
                    text = part.get("text", str(part))
                else:
                    text = str(part)
                text_parts.append(text)
            text = "\n".join(text_parts)
            messages.append(f"**{role}:**\n\n{text}\n")
        body = f"# {title}\n\n*Created*: {date}\n\n" + "\n---\n\n".join(messages)
        path.write_text(body, encoding="utf-8")
        docs.append((title, body))
    print("Wrote", len(docs), "markdown files to", out)
    if use_fts:
        db = sqlite3.connect("chats.db")
        db.executescript("""
        DROP TABLE IF EXISTS chats;
        CREATE VIRTUAL TABLE chats USING fts5(title, body, tokenize='porter');
        """)
        db.executemany("INSERT INTO chats (title, body) VALUES (?,?)", docs)
        db.commit()
        db.close()
        print("Created chats.db with FTS index")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("conversations_json")
    p.add_argument("--fts", action="store_true", help="create SQLite FTS index")
    args = p.parse_args()
    main(args.conversations_json, args.fts)
