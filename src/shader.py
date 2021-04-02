def source(path):
    f = open(path, "r")
    src = f.read()
    f.close()
    return src