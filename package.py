class Package:
    def __init__(self, id, source, destination):
        self.id = id
        self.source = source
        self.destination = destination
        self.taken = False
        self.done = False
