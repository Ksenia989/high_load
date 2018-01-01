class Visit:
    def __init__(self, id, location, user, visited_at, mark):
        self.id = id
        self.location = location
        self.user = user
        self.visited_at = visited_at
        self.mark = mark

    def __str__(self):
        return '[Sigthseen is: %s, located in %s, user is %s, he visited it in %s, mark is %s' % (
        self.id, self.location, self.user, self.visited_at, self.mark)

