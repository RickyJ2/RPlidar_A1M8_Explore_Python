class hexGrid:
    def __init__(self, q, r):
        self.q = q
        self.r = r
        self.s = -q - r
    def __eq__(self, other):
        if isinstance(other, hexGrid):
            return self.q == other.q and self.r == other.r and self.s == other.s
    def __ne__(self, other):
        return not self.__eq__(other)
    def __add__(self, other):
        if isinstance(other, hexGrid):
            return hexGrid(self.q + other.q, self.r + other.r)
        raise TypeError("Unsupported operand type for +: 'hex' and '{}'".format(type(other)))
    def __sub__(self, other):
        if isinstance(other, hexGrid):
            return hexGrid(self.q - other.q, self.r - other.r)
        raise TypeError("Unsupported operand type for -: 'hex' and '{}'".format(type(other)))
    def __mul__(self, other):
        if isinstance(other, int):
            return hexGrid(self.q * other, self.r * other)
        raise TypeError("Unsupported operand type for *: 'hex' and '{}'".format(type(other)))
    def __str__(self):
        return "q: {} r: {} s: {}".format(self.q, self.r, self.s)
    def length(self):
        return (abs(self.q) + abs(self.r) + abs(self.s)) // 2
    def distance(self, other):
        return (self - other).length()
    def direction(self, direction):
        return self + hexDirections[direction]
    def neighbor(self, direction):
        return self + hexDirections[direction]
    def neighbors(self):
        return [self.neighbor(direction) for direction in range(6)]
    def round(self):
        q = round(self.q)
        r = round(self.r)
        s = round(self.s)
        q_diff = abs(q - self.q)
        r_diff = abs(r - self.r)
        s_diff = abs(s - self.s)
        if q_diff > r_diff and q_diff > s_diff:
            q = -r - s
        elif r_diff > s_diff:
            r = -q - s
        else:
            s = -q - r
        return hexGrid(q, r)
    def lerp(self, other, t):
        return hexGrid(self.q + (other.q - self.q) * t, self.r + (other.r - self.r) * t)
    def linedraw(self, other):
        N = self.distance(other)
        results = []
        step = 1.0 / max(N, 1)
        for i in range(N + 1):
            results.append(self.lerp(other, step * i).round())
        return results
    
hexDirections = [
    hexGrid(1, 0), hexGrid(1, -1), hexGrid(0, -1),
    hexGrid(-1, 0), hexGrid(-1, 1), hexGrid(0, 1),
]