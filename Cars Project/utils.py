def removeSpaces(string):
    if isinstance(string, str):
        return string.replace("\n", "").replace("\t", "").replace(" ", "")
    else:
        raise ValueError("The object that was passed was not a string")
