
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/extract-seo', methods=['POST'])
def extract_seo():
    html = request.data.decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    # Meta title
    title = soup.title.string if soup.title else ""

    # Meta description
    description_tag = soup.find("meta", attrs={"name": "description"})
    description = description_tag["content"] if description_tag and description_tag.get("content") else ""

    # H1 to H6
    hn = {}
    for i in range(1, 7):
        tags = soup.find_all(f"h{i}")
        hn[f"h{i}"] = [tag.get_text(strip=True) for tag in tags]

    return jsonify({
        "meta_title": title,
        "meta_description": description,
        "hn": hn
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
