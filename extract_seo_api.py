
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/extract-seo", methods=["POST"])
def extract_seo():
    html = request.data.decode("utf-8", errors="replace")
    soup = BeautifulSoup(html, "html.parser")

    # Meta Title
    title_tag = soup.find("title")
    meta_title = title_tag.get_text(strip=True) if title_tag else ""

    # Meta Description
    desc_tag = soup.find("meta", attrs={"name": "description"})
    meta_description = desc_tag["content"].strip() if desc_tag and desc_tag.get("content") else ""

    # H1 to H6
    hn = {}
    for i in range(1, 7):
        tags = soup.find_all(f"h{i}")
        hn[f"h{i}"] = [tag.get_text(" ", strip=True) for tag in tags if tag.get_text(strip=True)]

    return jsonify({
        "meta_title": meta_title,
        "meta_description": meta_description,
        "hn": hn
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
