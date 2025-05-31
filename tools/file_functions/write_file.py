def write_file(x,y):
    """
    Creates a new file with x name and y content where x and y are strings.
    Args:
        x (str): The name of the file to create along with file extension. [.txt, .json, .py, .csv, .cpp , .java, .js, .html, .css, .xml, .md, .yaml, .yml, .sh, .bat]
        y (str): The content to write into the file.
    """
    # validate file extension
    valid_extensions = ['.txt', '.json', '.py', '.csv', '.cpp', '.java', '.js', '.html', '.css', '.xml', '.md', '.yaml', '.yml', '.sh', '.bat']
    if not any(x.endswith(ext) for ext in valid_extensions):
        raise ValueError(f"Invalid file extension. Supported extensions are: {', '.join(valid_extensions)}")
    with open(f"files/{x}","w") as f:
        f.write(y)
