import io
import os
import tokenize


def remove_comments_and_docstrings(source):

    io_obj = io.StringIO(source)
    out = ""
    prev_toktype = tokenize.INDENT
    last_lineno = -1
    last_col = 0
    for tok in tokenize.generate_tokens(io_obj.readline):
        token_type = tok[0]
        token_string = tok[1]
        start_line, start_col = tok[2]
        end_line, end_col = tok[3]
        ltext = tok[4]

        if start_line > last_lineno:
            last_col = 0
        if start_col > last_col:
            out += " " * (start_col - last_col)

        if token_type == tokenize.COMMENT:
            pass

        elif token_type == tokenize.STRING:
            if prev_toktype != tokenize.INDENT:

                if prev_toktype != tokenize.NEWLINE:

                    if start_col > 0:

                        out += token_string

        else:
            out += token_string
        prev_toktype = token_type
        last_col = end_col
        last_lineno = end_line
    return out


def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for fname in files:
            if fname.endswith(".py"):
                filepath = os.path.join(root, fname)
                with open(filepath, "r") as f:
                    content = f.read()
                stripped_content = remove_comments_and_docstrings(content)
                with open(filepath, "w") as f:
                    f.write(stripped_content)


if __name__ == "__main__":
    directory = "src"
    process_directory(directory)
