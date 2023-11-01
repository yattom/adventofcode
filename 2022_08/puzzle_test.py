def solve(puzzle_input: list[str]):
    tree_height = puzzle_input
    w, h = len(tree_height[0]), len(tree_height)
    visiblility = {(x, y): False for y in range(w) for x in range(h)}

    # left to right
    for x in range(h):
        max_height = None
        for y in range(w):
            if max_height is None or tree_height[y][x] > max_height:
                max_height = tree_height[y][x]
                visiblility[(x, y)] = True

    # right to left
    for x in range(h):
        max_height = None
        for y in range(w - 1, -1, -1):
            if max_height is None or tree_height[y][x] > max_height:
                max_height = tree_height[y][x]
                visiblility[(x, y)] = True

    # top to bottom
    for y in range(w):
        max_height = None
        for x in range(h):
            if max_height is None or tree_height[y][x] > max_height:
                max_height = tree_height[y][x]
                visiblility[(x, y)] = True

    # bottom to top
    for y in range(w):
        max_height = None
        for x in range(h - 1, -1, -1):
            if max_height is None or tree_height[y][x] > max_height:
                max_height = tree_height[y][x]
                visiblility[(x, y)] = True

    return sum([1 for v in visiblility.values() if v])


class View:
    def __init__(self, x, y, dx, dy, tree_height):
        self.x = self.start_x = x
        self.y = self.start_y = y
        self.dx = dx
        self.dy = dy
        self.tree_height = tree_height

    def __iter__(self):
        return self

    def __next__(self):
        if self.y < 0 or self.x < 0:
            raise StopIteration
        if self.y >= len(self.tree_height) or self.x >= len(self.tree_height[0]):
            raise StopIteration
        val = self.tree_height[self.y][self.x]
        self.y += self.dy
        self.x += self.dx
        return val


def test_view():
    tree_height = [
        '30373',
        '25512',
        '65332',
        '33549',
        '35390',
    ]
    view = View(0, 0, 1, 0, tree_height)
    assert list(view) == ['3', '0', '3', '7', '3']
    view = View(2, 2, 0, -1, tree_height)
    assert list(view) == ['3', '5', '3']
    view = View(2, 1, 0, 1, tree_height)
    assert list(view) == ['5', '3', '5', '3']
    view = View(4, 4, -1, 0, tree_height)
    assert list(view) == ['0', '9', '3', '5', '3']


def count_visible_trees(view: View):
    count = 0
    it = iter(view)
    start_height = next(it)
    for tree_height in it:
        count += 1
        if tree_height >= start_height:
            break
    return count


def test_count_visible_trees():
    assert 1 == count_visible_trees('35')
    assert 3 == count_visible_trees('321321')
    assert 3 == count_visible_trees(['3','2','1','3','2','1'])
    assert 3 == count_visible_trees(View(0, 0, 1, 0, ['321321']))


def solve2(puzzle_input: list[str]):
    tree_height = puzzle_input
    w, h = len(tree_height[0]), len(tree_height)
    max_score = 0
    for y in range(1, w - 1):
        for x in range(1, h - 1):
            up = View(x, y, 0, -1, tree_height)
            count_up = count_visible_trees(up)
            down = View(x, y, 0, 1, tree_height)
            count_down = count_visible_trees(down)
            left = View(x, y, -1, 0, tree_height)
            count_left = count_visible_trees(left)
            right = View(x, y, 1, 0, tree_height)
            count_right = count_visible_trees(right)
            score = count_up * count_down * count_left * count_right
            if score > max_score:
                max_score = score
    return max_score


def test_solve():
    assert solve([
        '30373',
        '25512',
        '65332',
        '33549',
        '35390',
    ]) == 21


def 問題1(puzzle_input: list[str]):
    print(solve(puzzle_input))


def 問題2(puzzle_input: list[str]):
    print(solve2(puzzle_input))


def main(solve_puzzle1, solve_puzzle2):
    with open("puzzle_input.txt") as f:
        puzzle_input = f.read().splitlines()
    solve_puzzle1(puzzle_input)
    solve_puzzle2(puzzle_input)


if __name__ == "__main__":
    main(問題1, 問題2)
