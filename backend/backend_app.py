from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    sort_field = request.args.get("sort")
    direction = request.args.get("direction", "asc")

    # Liste kopieren, damit die Originaldaten unverändert bleiben
    results = POSTS.copy()

    # Wenn kein Sortierfeld angegeben wurde → originale Reihenfolge behalten
    if sort_field is None:
        return jsonify(results), 200

    # Erlaubte Sortierfelder
    if sort_field not in ["title", "content"]:
        return jsonify({"error": "Invalid sort field. Allowed: 'title', 'content'."}), 400

    # Erlaubte Richtungen
    if direction not in ["asc", "desc"]:
        return jsonify({"error": "Invalid direction. Allowed: 'asc', 'desc'."}), 400

    reverse = (direction == "desc")

    # Sortieren
    results.sort(key=lambda p: p[sort_field].lower(), reverse=reverse)

    return jsonify(results), 200



@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()

    # Fehler: Kein JSON
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    title = data.get("title")
    content = data.get("content")

    # Fehler: Titel fehlt
    if not title:
        return jsonify({"error": "Field 'title' is required"}), 400

    # Fehler: Inhalt fehlt
    if not content:
        return jsonify({"error": "Field 'content' is required"}), 400

    # Neue eindeutige ID generieren
    new_id = max([p["id"] for p in POSTS]) + 1 if POSTS else 1

    new_post = {
        "id": new_id,
        "title": title,
        "content": content
    }

    POSTS.append(new_post)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    # Passenden Post finden
    post = next((p for p in POSTS if p["id"] == post_id), None)

    # Fehlerfall: ID existiert nicht
    if post is None:
        return jsonify({"error": f"Post with id {post_id} not found"}), 404

    # Beitrag löschen
    POSTS.remove(post)

    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200


# Update a post by ID
@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    post = next((p for p in POSTS if p["id"] == id), None)
    if post is None:
        return jsonify({"message": f"Post with id {id} not found."}), 404

    data = request.get_json()

    # title/content sind optional → nur aktualisieren, wenn vorhanden
    post["title"] = data.get("title", post["title"])
    post["content"] = data.get("content", post["content"])

    return jsonify({
        "id": post["id"],
        "title": post["title"],
        "content": post["content"]
    }), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_query = request.args.get("title", "").lower()
    content_query = request.args.get("content", "").lower()

    # Filter posts
    results = [
        post for post in POSTS
        if (title_query in post["title"].lower() if title_query else True)
           and (content_query in post["content"].lower() if content_query else True)
    ]

    return jsonify(results), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
