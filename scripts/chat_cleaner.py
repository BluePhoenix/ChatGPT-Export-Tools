"""ChatGPT Export Cleaner
Usage:
    python chat_cleaner.py <conversations.json>  # from OpenAI data export

Outputs:
    chats.csv  – one row per conversation with:
        id, title, created_time, last_activity, num_messages, preview
You can open the CSV in Excel/Sheets or import into Notion, then tag
columns like KEEP / DELETE or TOPIC to decide what to remove.
"""

import json, csv, sys, textwrap, datetime as dt, pathlib

def main(path):
    data = json.loads(pathlib.Path(path).read_text())
    # Handle both formats: direct list of conversations or dict with "conversations" key
    conversations = data if isinstance(data, list) else data.get("conversations", [])
    rows = []
    for chat in conversations:
        msgs = chat.get("mapping", {})
        # Convert any non-string content to string representation
        texts = []
        for n in msgs.values():
            if n.get("message"):
                parts = n.get("message", {}).get("content", {}).get("parts", [""])
                for part in parts:
                    if isinstance(part, str):
                        texts.append(part)
                    else:
                        texts.append(str(part))
        preview = textwrap.shorten(" ".join(texts), width=120)
        rows.append({
            "id": chat["id"],
            "title": chat.get("title", "")[:60],
            "created_time": ts(chat["create_time"]),
            "last_activity": ts(chat["update_time"]),
            "num_messages": len(texts),
            "preview": preview,
        })
    rows.sort(key=lambda r: r["created_time"], reverse=True)
    with open("chats.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    print("Wrote chats.csv with", len(rows), "rows")

def ts(epoch):
    return dt.datetime.fromtimestamp(epoch).isoformat() if epoch else ""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python chat_cleaner.py conversations.json")
    else:
        main(sys.argv[1])
