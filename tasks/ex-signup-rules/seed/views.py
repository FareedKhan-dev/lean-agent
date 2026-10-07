from signup import validate_signup


def post_signup(form):
    errors = validate_signup(form)
    if errors:
        return 400, {"errors": errors}
    return 201, {"welcome": form["username"]}
