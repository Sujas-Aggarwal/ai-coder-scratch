def read_file(x):
    """
    Call this function to read a file with name x.
    Args:
        x (str): The name of the file to read including its extension.
    Returns:
        str: The content of the file.
    """
    try:
        with open(f"files/{x}", "r") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return f"File {x} not found."
