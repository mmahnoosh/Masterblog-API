from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This enables Cross-Origin Resource Sharing (CORS) for all routes

# Sample in-memory data store for blog posts
POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
    {"id": 3, "title": "alfa post", "content": "This is the salfa post."},
    {"id": 4, "title": "Apost", "content": "This is apost."},
    {"id": 5, "title": "Betapost", "content": "This is beta post."},
]

@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Retrieve all posts.

    Returns:
        JSON list of all posts with status code 200.
    """
    return jsonify(POSTS)

@app.route('/api/posts', methods=['POST'])
def add_post():
    """
    Add a new post.

    Expected JSON:
        {
            "title": "<string>",
            "content": "<string>"
        }

    Returns:
        JSON of the created post with status 201 on success,
        or error message with status 400 if validation fails.
    """
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
    """
    Delete a post by ID.

    Args:
        id (str): ID of the post to be deleted.

    Returns:
        Success message if found and deleted, 404 error if not found.
    """
    for post in POSTS:
        if str(post['id']) == str(id):
            POSTS.remove(post)
            return jsonify({"message": f"Post with id: {id} has been deleted successfully."}), 200
    return jsonify({"message": f"Post with id: {id} does not exist!"}), 404

@app.route('/api/posts/<id>', methods=['PUT'])
def update_post(id):
    """
    Update a post by ID.

    Args:
        id (str): ID of the post to update.

    Expected JSON (partial or full):
        {
            "title": "<string>",
            "content": "<string>"
        }

    Returns:
        Updated post with status 200, or error if the post does not exist or fields are missing.
    """
    data = request.get_json()
    post = next((post for post in POSTS if str(post['id']) == str(id)), None)
    if not post:
        return jsonify(f"Error: Post with ID {id} not exist.")

    title = data.get('title', post['title']).strip()
    content = data.get('content', post['content']).strip()

    if not title and not content:
        return jsonify("Error: title or content need to be present!")

    if title:
        post['title'] = title
    if content:
        post['content'] = content
    return jsonify(post), 200

@app.route('/api/posts/search', methods=['GET'])
def search_post():
    """
    Search posts by title or content (case-insensitive).

    Query Parameters:
        title (str, optional): Search term for title.
        content (str, optional): Search term for content.

    Returns:
        JSON list of matching posts with status 200.
    """
    new_post_list = []
    title = request.args.get('title', None)
    content = request.args.get('content', None)

    title = title.lower() if title else None
    content = content.lower() if content else None

    for post in POSTS:
        post_title = post['title'].lower()
        post_content = post['content'].lower()

        if (title and title in post_title) or (content and content in post_content):
            new_post_list.append(post)

    return jsonify(new_post_list), 200

@app.route('/api/posts/sort', methods=['GET'])
def sort_post():
    """
    Sort posts by a specified field and direction.

    Query Parameters:
        sort_item (str): Field to sort by (default is 'content').
        direction (str): 'asc' for ascending, 'desc' for descending (default is 'asc').

    Returns:
        JSON list of sorted posts or error if sort_item is invalid.
    """
    sort_item = request.args.get('sort_item', 'content')
    direction = request.args.get('direction', 'asc')

    reverse = direction.lower() == 'desc'
    try:
        sorted_posts = sorted(POSTS, key=lambda x: x.get(sort_item).lower(), reverse=reverse)
    except KeyError:
        return jsonify({'error': f'Invalid sort key: {sort_item}'}), 400

    return jsonify(sorted_posts)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
