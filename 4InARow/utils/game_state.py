class GameState():
    def __init__(self):
        self.quit = 0
        self.main = 1
        self.pvp = 2
        self.pve = 3
        self.state = self.main
        self.q = []

    def put(self, state):
        while state in self.q:
            self.q.remove(state)
        self.q.append(self.state)
        self.state = state

    def get(self, state):
        while state in self.q:
            self.q.remove(state)
        val = self.q[-1]
        while val in self.q:
            self.q.remove(val)
        if val == state:
            val = self.q[-1]
            while val in self.q:
                self.q.remove(val)
        self.state = val
