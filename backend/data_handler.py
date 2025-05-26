"""
Data handling for Masterblog API
"""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
BLOGPOSTS = os.path.join(DATA_DIR, 'posts.json')


def load_blog_posts(filepath = BLOGPOSTS):
    """
    Load blog posts from JSON file.
    :param filepath: Path to the JSON file (defaults to BLOGPOSTS constant).
    :return: List of blog posts (list of dicts), or empty list if an error occurs.
    """
    try:
        with open(filepath, "r") as handle:
            return json.load(handle)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading blog posts from {filepath}: {e}")
        return []


def save_blog_posts(posts, filepath = BLOGPOSTS):
    """
    Save blog posts to JSON file.
    :param posts: List of blog posts to save (list of dicts).
    :param filepath: Path to the JSON file (defaults to BLOGPOSTS constant).
    :return: None
    """
    try:
        with open(filepath, "w") as handle:
            json.dump(posts, handle, indent=4)
    except (OSError, IOError) as e:
        raise RuntimeError(f"Failed to save blog posts to {filepath}: {e}") from e


def get_all_fields():
    """
    Retrieves all unique fields in the posts data, excluding 'id'.
    :return: Set of field names excluding 'id'.
    """
    posts = load_blog_posts()
    return {key for post in posts for key in post if key != "id"}


def create_post(title, content):
    """
    Creates a new post and assigns unique post id.
    :param title: Title of the new post.
    :param content: Content of the new post.
    :return: New post as dict.
    """
    posts = load_blog_posts()

    new_post_id = 1
    if posts:
        new_post_id = max(post["id"] for post in posts) + 1

    new_post = {
        "id": new_post_id,
        "title": title,
        "content": content
    }

    posts.append(new_post)
    save_blog_posts(posts)

    return new_post


def updating_post(post, data_for_update):
    """
    Updates a post with the provided data to update.
    :param post: Post to update.
    :param data_for_update: Data tu be updated.
    :return: tuple:
        - if successful: (is_successful: bool, error: str)
        - if unsuccessful: (error message, status code)
    """
    allowed_fields = get_all_fields()
    for field in data_for_update:
        if field in allowed_fields:
            post[field] = data_for_update[field]
        else:
            return False, f"'{field}' is no allowed Field."
    return True, None