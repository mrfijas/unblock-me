from sys import argv


class Board:
    width: int
    height: int

    bricks = []
    positions = []
    history = []
    hashmap = set()

    def __init__(self, width: int = 6, height: int = 6):
        self.width = width
        self.height = height
        self.init_bricks()

    def init_bricks(self):
        for i, (x, y, type, length) in enumerate(argv[1].split(',')):
            self.bricks.append({
                'id': i,
                'type': type,
                'length': int(length)
            })
            self.positions.append((int(x), int(y)))

    def get_fields(self, positions):
        fields = [[None] * self.width for _ in range(self.height)]
        for i, brick in enumerate(self.bricks):
            x, y = positions[i]
            for l in range(brick['length']):
                if brick['type'] == 'h':
                    fields[y][x + l] = brick
                else:
                    fields[y + l][x] = brick
        return fields

    @staticmethod
    def print(fields):
        def hex_name(n):
            return hex(n)[2:]

        for row in fields:
            for cell in row:
                x = hex_name(cell['id']) if cell else '_'
                print(f' {x} ', end='')
            print()

    def get_new_position(self, positions, i, move):
        position = positions[i]
        brick = self.bricks[i]
        if brick['type'] == 'h':
            return position[0] + move, position[1]
        else:
            return position[0], position[1] + move

    def is_move_valid(self, i, positions, fields, move_type):
        position = positions[i]
        brick = self.bricks[i]

        if brick['type'] == 'h':
            for x in range(0, abs(move_type)):
                new_x = position[0] + (brick['length'] + x if move_type > 0 else -1 - x)

                if not 0 <= new_x < self.width or fields[position[1]][new_x] is not None:
                    return False
        elif brick['type'] == 'v':
            for y in range(0, abs(move_type)):
                new_y = position[1] + (brick['length'] + y if move_type > 0 else -1 - y)

                if not 0 <= new_y < self.height or fields[new_y][position[0]] is not None:
                    return False
        return True

    def is_solved(self, positions):
        return positions[0][0] + self.bricks[0]['length'] == self.width and \
               positions[0][1] == self.height // 2 - 1

    def print_solution(self, i):
        steps = []
        while i > 0:
            steps.append(i)

            i = self.history[i][0]

        print(f'Moves: {len(steps) + 1} (history: {len(self.history)})\n')
        for step in reversed(steps):
            self.print(self.get_fields(self.history[step][1]))
            print()

    @staticmethod
    def hash_positions(positions):
        return ' '.join([f'{x}.{y}' for (x,y) in positions])

    def solve(self):
        def get_nth_move(n):
            return (n // 2 + 1) * (1 if n % 2 else -1)

        current = 0
        self.history.append((current, self.positions))
        self.hashmap.add(self.hash_positions(self.positions))

        while len(self.history) < 1000000:
            positions = self.history[current][1]
            fields = self.get_fields(positions)

            for i in range(len(self.bricks)):
                for move in [get_nth_move(n) for n in range(8)]:
                    if self.is_move_valid(i, positions, fields, move):
                        new_positions = positions.copy()
                        new_positions[i] = self.get_new_position(positions, i, move)

                        if self.is_solved(new_positions):
                            self.print_solution(current)

                            return

                        hash_positions = self.hash_positions(new_positions)
                        if not hash_positions in self.hashmap:
                            self.hashmap.add(hash_positions)
                            self.history.append((current, new_positions))
            current += 1

            if current > len(self.history):
                print('no solution')
                return

board = Board()
board.print(board.get_fields(board.positions))
print()
board.solve()
