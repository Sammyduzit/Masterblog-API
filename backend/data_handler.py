"""
Data handling for Masterblog API
"""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), 'static')
BLOGPOSTS = os.path.join(DATA_DIR, 'posts.json')


def load_json(filepath):
    """
    Load blog posts from JSON file.
    :param filepath: Path to the JSON file.
    :return: Parsed JSON data as a Python object, or empty list if an error occurs.
    """
    try:
        with open(filepath, "r") as handle:
            return json.load(handle)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_json(filepath, data):
    """
    Save blog posts to JSON file.
    :param filepath: Path to the JSON file.
    :param data: Data to be saved.
    :return: None
    """
    with open(filepath, "w") as handle:
        json.dump(data, handle, indent=4)


def get_all_posts():
    """
    Retrieve all posts from json file.
    :return: List of all posts (list of dicts), or empty list if no posts are found.
    """
    return load_json(BLOGPOSTS)


def save_all_posts(posts):
    """
    Saves a list of posts to json file.
    :param posts: List of posts to save.
    :return: None
    """
    save_json(BLOGPOSTS, posts)


def get_all_fields():
    """
    Retrieves all unique fields in the posts data, excluding 'id'.
    :return: Set of field names excluding 'id'.
    """
    posts = get_all_posts()
    return {key for post in posts for key in post if key != "id"}


def validate_sorting(sort, direction):
    """
    Validate sorting parameters for POST queries.
    :param sort: Parameter to sort by.
    :param direction: Sorting direction (ascending 'asc' or descending 'desc')
    :return: tuple: (is_valid: bool, errors: list)
    """
    errors = []
    valid_sorts = get_all_fields()
    valid_directions = {"asc", "desc"}

    if direction and not sort:
        errors.append("Direction parameter requires sort parameter.")

    if sort:
        if sort not in valid_sorts:
            errors.append(f"Invalid sort parameter: {sort}. "
                                     f"Valid options are '{', '.join(valid_sorts)}'")
        if direction and direction not in valid_directions:
            errors.append(f"Invalid direction parameter: {direction}. "
                                     f"Valid options are '{', '.join(valid_directions)}'")

    return len(errors) == 0, errors


def sort_posts(posts, sort_key, direction):
    """
    Sorts a list of posts by given sort key and direction.
    :param posts: List of posts to sort.
    :param sort_key: Key to sort by.
    :param direction: Sorting direction (ascending 'asc' or descending 'desc')
    :return: Sorted list of posts.
    """
    reverse = (direction == "desc")
    return sorted(posts, key=lambda x: x[sort_key].lower(), reverse=reverse)


def validate_post_data(data):
    """
    Validates post data. Checks for required fields and data type.
    :param data: Post data to validate.
    :return: tuple: (is_valid: bool, errors: list)
    """
    errors = []
    required_fields = get_all_fields()
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
            continue

        if not isinstance(data[field], str):
            errors.append(f"{field} must be a string.")

        elif not data[field].strip():
            errors.append(f"{field} can not be empty.")

    return len(errors) == 0, errors


def create_post(title, content):
    """
    Creates a new post and assigns unique post id.
    :param title: Title of the new post.
    :param content: Content of the new post.
    :return: New post as dict.
    """
    posts = get_all_posts()

    new_post_id = 1
    if posts:
        new_post_id = max(post["id"] for post in posts) + 1

    new_post = {
        "id": new_post_id,
        "title": title,
        "content": content
    }

    posts.append(new_post)
    save_all_posts(posts)

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