def validate_sorting(sort, direction, allowed_fields):
    """
    Validate sorting parameters for POST queries.
    :param sort: Parameter to sort by.
    :param direction: Sorting direction (ascending 'asc' or descending 'desc')
    :param allowed_fields: Allowed fields for post data
    :return: tuple: (is_valid: bool, errors: list)
    """
    errors = []
    valid_directions = {"asc", "desc"}

    if direction and not sort:
        errors.append("Direction parameter requires sort parameter.")

    if sort:
        if sort not in allowed_fields:
            errors.append(f"Invalid sort parameter: {sort}. "
                                     f"Valid options are '{', '.join(allowed_fields)}'")
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


def validate_post_data(data, required_fields):
    """
    Validates post data. Checks for required fields and data type.
    :param data: Post data to validate.
    :param required_fields:
    :return: tuple: (is_valid: bool, errors: list)
    """
    errors = []
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
            continue

        if not isinstance(data[field], str):
            errors.append(f"{field} must be a string.")

        elif not data[field].strip():
            errors.append(f"{field} can not be empty.")

    return len(errors) == 0, errors
