from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
    {"id": 3, "title": "Second post", "content": "This is the second post."},
]


# app.secret_key = os.environ.get("secret_key")

@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()
    new_title = data.get('title', '').strip()
    new_content = data.get('content', '').strip()

    if not new_title or not new_content:
        return jsonify({"error": "All fields must be filled in."}), 400

    new_id = max([post["id"] for post in POSTS], default=0) + 1
    new_post = {
        "id": new_id,
        "title": new_title,
        "content": new_content
    }
    POSTS.append(new_post)
    return jsonify(new_post), 201


@app.route('/api/posts/<id>', methods=['DELETE'])
def delete_post(id):
    for post in POSTS:
        if str(post['id']) == str(id):
            POSTS.remove(post)
            return jsonify({"message": f"Post with id: {id} has been deleted successfully."}), 200
    return jsonify({"message": f"Post with id: {id} does not exist!"}), 404




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
