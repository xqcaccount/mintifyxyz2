import os
import shutil
import subprocess

# === CONFIG ===
REPO_DIR = "/Users/Evan/Desktop/mintify-seo-content"
BATCH_DIR = os.path.join(REPO_DIR, "batch")
POSTS_DIR = os.path.join(REPO_DIR, "posts")
INDEX_FILE = os.path.join(REPO_DIR, "index.html")

# === MOVE FILES ===
def move_articles():
    new_files = []
    for fname in os.listdir(BATCH_DIR):
        if fname.endswith(".md"):
            src = os.path.join(BATCH_DIR, fname)
            dst = os.path.join(POSTS_DIR, fname)
            shutil.move(src, dst)
            new_files.append(fname)
    return new_files

# === UPDATE index.html ===
def update_index_html(files):
    with open(INDEX_FILE, "r") as f:
        content = f.read()

    insert_at = content.find("</ul>")
    if insert_at == -1:
        print("❌ Could not find <ul> in index.html")
        return

    new_links = ""
    for fname in files:
        title = fname.replace("-", " ").replace(".md", "").title()
        new_links += f'    <li><a href="posts/{fname}">{title}</a></li>\n'

    updated_content = content[:insert_at] + new_links + content[insert_at:]

    with open(INDEX_FILE, "w") as f:
        f.write(updated_content)

# === COMMIT AND PUSH ===
def push_to_git():
    os.chdir(REPO_DIR)
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "Bulk upload new SEO articles"])
    subprocess.run(["git", "push", "origin", "main"])

# === RUN ===
new_articles = move_articles()
if new_articles:
    update_index_html(new_articles)
    push_to_git()
    print(f"✅ Uploaded {len(new_articles)} new articles.")
else:
    print("No new articles found in /batch/")