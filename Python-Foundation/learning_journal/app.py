from flask import Flask, render_template, abort, request, redirect, url_for
import os
import markdown

app = Flask(__name__)
POSTS_DIR = os.path.join(os.path.dirname(__file__), "posts")

# Ensure posts directory exists
os.makedirs(POSTS_DIR, exist_ok=True)


@app.route("/")
def index():
    posts = []
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith(".md"):
            slug = filename[:-3]
            # Create a clean title from filename
            title = slug.replace("-", " ").title()
            posts.append({"slug": slug, "title": title})
    return render_template("index.html", posts=posts)


@app.route("/post/<slug>")
def post(slug):
    filepath = os.path.join(POSTS_DIR, f"{slug}.md")
    if not os.path.exists(filepath):
        abort(404)

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    html_content = markdown.markdown(content, extensions=["fenced_code", "codehilite"])
    title = slug.replace("-", " ").title()
    return render_template("post.html", title=title, content=html_content)


@app.route("/new", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        if title and content:
            slug = title.lower().replace(" ", "-")
            filepath = os.path.join(POSTS_DIR, f"{slug}.md")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            return redirect(url_for("index"))
    return render_template("new.html")


if __name__ == "__main__":
    app.run(debug=True, port=5002)
