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
    return jsonify(POSTS)


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
    post = next((p for p in posts if p["id"] == id), None)
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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
