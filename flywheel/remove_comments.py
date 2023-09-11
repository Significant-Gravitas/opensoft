import os
import ast

def remove_comments_from_code(code):
    lines = code.splitlines()
    tree = ast.parse(code)

    line_nos = {node.lineno for node in ast.walk(tree) if hasattr(node, 'lineno')}
    new_code = '\n'.join(line for idx, line in enumerate(lines, start=1) if idx in line_nos)

    return new_code

def process_directory(path):
    for root, dirs, files in os.walk(path):
        # Only process if 'flywheel' is part of the directory path
        if 'flywheel' in root:
            for file in files:
                if file.endswith('.py'):
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        content = f.read()
                    content_no_comments = remove_comments_from_code(content)
                    with open(os.path.join(root, file), 'w', encoding='utf-8') as f:
                        f.write(content_no_comments)

# Start the script from the root of your codebase

if __name__ == '__main__':
    process_directory('/path/to/your/codebase')
