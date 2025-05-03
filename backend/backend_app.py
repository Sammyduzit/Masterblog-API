from flask import Flask, jsonify, request
from flask_cors import CORS
import data_handler

app = Flask(__name__)
CORS(app)


def error_response(message, status_code, details=None):
    """
    Generate error response JSON.
    :param message: Main error message.
    :param status_code: HTTP status code.
    :param details: Additional details about the error. Default=None
    :return: tuple: (JSON response, status code)
    """
    response = {
        "error": {
            "message": message,
            "status": status_code,
            "details": details or []
        }
    }
    return jsonify(response), status_code


def success_response(data, status_code=200):
    """
    Generate success response JSON.
    :param data: Data to return.
    :param status_code: HTTP status code.
    :return: tuple: ( JSON response, status code)
    """
    return jsonify(data), status_code


@app.route("/api/posts", methods=["GET"])
def list_posts():
    """
    Lists all posts, optionally sorted by given parameters.
    :return: tuple:
        - if successful: (sorted list as JSON, status code)
        - if unsuccessful: (error message, status code)
    """
    posts = data_handler.get_all_posts()
    sort = request.args.get("sort")
    direction = request.args.get("direction")

    if not sort:
        return success_response(posts)

    is_valid, errors = data_handler.validate_sorting(sort, direction)
    if not is_valid:
        return error_response("Invalid sorting parameters", 400, errors)

    try:
        sorted_posts = data_handler.sort_posts(posts, sort, direction)
        return success_response(sorted_posts)
    except KeyError as e:
        return error_response(f"Missing key in post data {e}", 500)
    except Exception as e:
        return  error_response(f"Server error while sorting", 500, f"error: {e}")


@app.route("/api/posts", methods=["POST"])
def add_post():
    """
    Adds a new post. Uses validate_post_data function for validation and create_post for post creation.
    :return: tuple:
        - if successful: (added post as JSON, status code)
        - if unsuccessful: (error message, status code)
    """
    if not request.is_json:
        return error_response("Request must be JSON", 400)

    data = request.get_json()
    is_valid, errors = data_handler.validate_post_data(data)

    if not is_valid:
        return error_response("Invalid post data", 400, errors)

    try:
        new_post = data_handler.create_post(data["title"], data["content"])
        return success_response(new_post, 201)
    except Exception as e:
        return error_response("Server error while adding post", 500, f"error: {e}")


@app.route("/api/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    """
    Deletes a post by ID. Checks if post was deleted.
    :param post_id: ID of post to be deleted.
    :return: tuple:
        - if successful: (success message as JSON, status code)
        - if unsuccessful: (error message, status code)
    """
    posts = data_handler.get_all_posts()
    initial_number_of_posts = len(posts)

    posts = [post for post in posts if post["id"] != post_id]

    if len(posts) < initial_number_of_posts:
        data_handler.save_all_posts(posts)
        return success_response({"message": f"Post with id '{post_id}' has been deleted successfully."})

    else:
        return error_response(f"No post with id <{post_id}> found.", 404)



@app.route("/api/posts/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    """
    Updates a post by ID.
    :param post_id: ID of post to be updated.
    :return: tuple:
        - if successful: (updated post as JSON, status code)
        - if unsuccessful: (error message, status code)
    """
    if not request.is_json:
        return error_response("Request must be JSON", 400)

    posts = data_handler.get_all_posts()
    post = next((post for post in posts if post["id"] == post_id), None)

    if not post:
        return error_response("Post not found.", 404)

    data_for_update = request.get_json()

    is_successful, error = data_handler.updating_post(post, data_for_update)

    if not is_successful:
        return error_response("Invalid update data", 400, error)

    data_handler.save_all_posts(posts)
    return success_response(post)



@app.route("/api/posts/search", methods=["GET"])
def search_post():
    """
    Searches for posts by title or content.
    :return: tuple:
        - if successful: (list of matching posts as JSON, status code)
        - if unsuccessful: (error message, status code)
    """
    posts = data_handler.get_all_posts()
    title = request.args.get("title")
    content = request.args.get("content")

    if not (title or content):
        return error_response("Search must have at least one parameter", 400)

    match_list = [post for post in posts
                  if (not title or title.lower() in post["title"].lower())
                  and (not content or content.lower() in post["content"].lower())]

    return success_response(match_list)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
