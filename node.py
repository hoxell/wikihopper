class Node():
    def __init__(self, url, parent):
        self.url = url
        self.parent = parent

        if parent is None:
            self.depth = 0
        else:
            self.depth = parent.depth + 1