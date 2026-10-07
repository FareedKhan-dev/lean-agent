from people.names import display_name

STAFF = [("grace", "hopper", "Compilers"), ("alan", "turing", "Research")]


def staff_list():
    return [f"{display_name(first, last)} ({team})" for first, last, team in STAFF]
