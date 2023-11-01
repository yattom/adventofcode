import pytest

def make_map(puzzle_input):
    height_map = {}
    x, y = 0, 0
    for c in puzzle_input:
        if c == '\n':
            y += 1
            x = 0
            continue
        height_map[f"{x},{y}"] = c
        x += 1
    return height_map


def find_start(marker, height_map):
    for k, v in height_map.items():
        if v == marker:
            return k
    raise ValueError("スタートが見つかりませんでした")


def test_2x1の地図を作る():
    puzzle_input = "SE"
    actual = make_map(puzzle_input)
    assert {"0,0": "S", "1,0": "E"} == actual


def p2i(pos):
    return tuple(map(int, pos.split(",")))


def height(c):
    if c == "S":
        return height('a')
    if c == "E":
        return height('z')
    return ord(c) - ord('a')


def move(pos, height_map, is_possible=lambda c, n: True):
    x, y = p2i(pos)
    four_dirs = [f"{x-1},{y}", f"{x+1},{y}", f"{x},{y-1}", f"{x},{y+1}"]
    within_map = filter(lambda d: d in height_map, four_dirs)
    next_pos = filter(lambda d: is_possible(height_map[pos], height_map[d]), within_map)
    return next_pos


def solve(puzzle_input, start_marker, goal_marker, is_possible):
    height_map = make_map(puzzle_input)
    start = find_start(start_marker, height_map)
    currents = [start]
    current_step = 0
    visited = {start}
    while currents:
        next_pos = set()
        # print(f"step: {current_step}, height: {height_map[list(currents)[0]]}, next possible steps: {len(currents)}, covered areas: {len(visited)} / {len(height_map)}")
        for pos in currents:
            for n in move(pos, height_map, is_possible):
                if n not in visited:
                    next_pos.add(n)

        for n in next_pos:
            if height_map[n] == goal_marker:
                return current_step + 1
            visited.add(n)

        current_step += 1
        currents = next_pos

    dump(height_map, visited)
    return -1


def one_step_higher_or_below(c, n):
    return height(n) - height(c) <= 1


def one_step_lower_or_above(c, n):
    return height(c) - height(n) <= 1


def dump(height_map, visited):
    x_max = max([p2i(pos)[0] for pos in height_map.keys()])
    y_max = max([p2i(pos)[1] for pos in height_map.keys()])
    for y in range(y_max + 1):
        for x in range(x_max + 1):
            pos = f"{x},{y}"
            if pos in visited:
                print("#", end="")
            elif pos in height_map:
                print(height_map[pos], end="")
            else:
                print(" ", end="")
        print()

@pytest.fixture
def decent_map():
    return make_map("""Sabcd
abcde
bcdef
cdefg
defgE
""")


def test_複数行の地図を作る():
    puzzle_input = """Sab
aba
bcE
"""
    actual = make_map(puzzle_input)
    assert actual["0,0"] == "S"
    assert actual["2,2"] == "E"


def test_スタートを見つける():
    assert "0,0" == find_start("S", make_map("S"))


def test_1歩進む(decent_map):
    actual = move("2,2", decent_map)
    assert set(actual) == {"2,1", "2,3", "1,2", "3,2"}


def test_地図の外には進めない():
    actual = move("0,0", make_map("S"))
    assert set(actual) == set()


def test_高さの差が1なら進める():
    actual = move("0,0", make_map("Sb"), is_possible=one_step_higher_or_below)
    assert set(actual) == {"1,0"}


def test_高さの差が2以上あると進めない():
    actual = move("0,0", make_map("Sc"), is_possible=one_step_higher_or_below)
    assert set(actual) == set()


def test_下れる():
    actual = move("0,0", make_map("ca"))
    assert set(actual) == {"1,0"}


def test_Eまでの歩数を数える():
    actual = solve("SabcdefghijklmnopqrstuvwxyzE", start_marker="S", goal_marker="E", is_possible=one_step_higher_or_below)
    assert actual == 27


def test_サンプル問題1():
    actual = solve("""Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
""", start_marker="S", goal_marker="E", is_possible=one_step_higher_or_below)
    assert actual == 31


def test_サンプル問題2():
    actual = solve("""Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
""", start_marker="E", goal_marker="a", is_possible=one_step_lower_or_above)
    assert actual == 29


def 本問題1():
    steps = solve("""abccccaaaaaaaaaaaaaccaaaaaaaacccccccccaaaaaaaaccccccccaaacaaacccccccaaaaaaccccccccccccccccccccccaaaacccccccccccacccccccccccccccccccccccccccccccccccccccccccccccaaaa
abccccaaaaacaaaaaaccccaaaaaaccccccccccaaaaaaacccccccccaaaaaaacccccaaaaaaaaaacccccccccccccccccccaaaaaacccccccccaaaaaaaaccccccccccccccccccccccccccccccccccccccccaaaaa
abcccaaaaaccaaaaaaccccaaaaaaccccccaacccaaaaaacccccccccaaaaaacccaaaaaaaaaaaaaaacaaccacccccccccccaaaaaaccccccccccaaaaaacccccccccccccccccccccccccccccccccccccccccaaaaa
abccccccaaccaaaaaaccaaaaaaaaccccccaaacaaaacaaacccccccaaaaaaaaccaaaaaaaaaaaaaaacaaaaacccccccccccccaaccccccccccccaaaaaaccccccccccccccccccccccccccccacccccccccccaaaaaa
abccccccccccaaccaaccaaaaccaacccccccaaaaaaaccccccccccaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaacccccccaaaaccccccccccccccccaaaaaaaacccccccccccccccccccccccccccaaccccccccccccccaa
abcccccccaaaaacccaaaaaaaacccaaccccaaaaaaccccccccccccaaaaaaaaaaaaaaaacaaaaaaaccaaaaaaccccccaaaaaccccccccccccccaaaaaaaaaaccaccccccccccccccccccccccccaccccccccccccccca
abcccccccaaaaacccaaaaaaaaccaaaaccaaaaaaaaccccccccccccccaaacaaaaaaaaacaaaaaacccccaaaacccccaaaaaaccccccccccccccaaaaaaaaaaaaacccccccccccccccllllllccccdccccccccccccccc
abccccccaaaaaacccccaaaaccccaaaaacaaaaaaaaccccccccccccccaaacccccaaaccccaaaaaacccaaccccccccaaaaaacccccccccccccccccaaaaaaaaaacccccccccccccklllllllllcddddccaccaaaccccc
abccccccaaaaaacccccaaaaaaaaaaaaaaaccaaccccccaacaacccccccaaccccccccccccaaacaacccccccccccccaaaaaacccccccccccccccccaaaaaaaaaacccccccccccckklllppllllcddddddddaaaaccccc
abccccccaaaaaaccccaaacaaaaaaaaaaaaccaaccccccaaaaaccccccccccccccccccccccccccccccccccccccccccaaccccccaaccccccccccccaacaaaaaaaccccccccccckklpppppplllmdddddddddacccccc
abccccccccaaacccccaacccaccaaaaaaccccccccccccaaaaaaccccccccccccccccccccccccccccccccccccccccccccccccaaaaccccccccccccaaaaaaaaaaccccccccckkkkppppppplmmmmmmddddddaacccc
abccccaaacaaacccccccccccccaaaaaaccccccccccccaaaaaacccccccccccccccccaaaccccccccccccccccccccccccccccaaaaccccccccccccaaaaaaaaaaccccccccckkkppppuppppmmmmmmmmddeeeacccc
abccccaaaaaaacccccccccccccaaaaaacccaccccccccaaaaaacccccccccccccccccaaaacccccccccccccccccccccaaacccaaaacccccccccccaaaacaaaccccccccccckkkpppuuuuuppqqmmmmmmmmeeeacccc
abcccccaaaaaaccccccccccccaaaaaaaacaaccccccccccaaaccccccccccccccccccaaaaccccccccccccccccccccaaaaccccccccccccccccccaaaaaaaacccccccccckkkkpppuuuuupqqqqqqqmmmmeeeccccc
abcccccaaaaaaaacccccccccccaccccaaaaacccccccccccccccccccccccccccccccaaaccccccccccccccaaaccccaaaacccccccccccccaaccaaaaaaaaccccccccckkkkkrrpuuuxuuuqqqqqqqqmmmmeeccccc
abccccaaaaaaaaaccccccccccccccaaaaaacccccccacaacccccccccccccccccccccccccccccccccccccaaaaaacccaaaccccccccccaaaaccaaaaaaacccccccccckkkkrrrrruuuxxuvvvvvvqqqqnnneeccccc
abcccaaaaaaaaaaccccccccccccccaaaaaaaacccccaaaaacccccccccccccccaaaaaccccccccccccccccaaaaaaccccccccccccccccaaaaaaaaaaaaacccccccccjjjkrrrrruuuxxxxvvvvvvvqqqnnneeccccc
abcaaaaacaaacccccccccccccccccaaaaaaaacccccaaaaaccaacccccccccccaaaaaccccccccccccccccaaaaaccccccccccccccccccaaaaaccaaaaaacccccccjjjrrrrruuuuuxxxyvyyyvvvqqqnneeeccccc
abcaaaaacaaaccaaccccccccccccccccaacccccccaaaaaaaaaaaccccccccccaaaaaaccccccccccccccccaaaaaccccccccccccccccaaaaacccaaaaaaaacaaacjjjrrrtttuuxxxxxyyyyyvvvqqnnneeeccccc
abaaaaaccaacccaaaccaacccaaccccccaccccccccaaaaaaaaaacccccccccccaaaaaaccccccccccccccccaacaacccccccccccccccccccaacccaaccccaaaaaacjjjrrrtttxxxxxxxyyyyyvvvrrnnneeeccccc
SbaaaaacccccccaaaaaaaccaaaacccccccccccccccaaaaaaaaacccccccccccaaaaaaccccccccccccccccccccccccccccccccccccccccccccccaacccaaaaaacjjjrrrtttxxxEzzzzyyyvvvrrnnneeecccccc
abcaaaaacccccccaaaaaaccaaaacccccccccccccccaaaaaaaaacccccccccccccaaccccccccccccccccccccccccccccaaccccccccccaaccccacaaaacaaaaaaajjjrrrtttxxxxxyyyyyvvvrrrnnnfffcccccc
abcaacccccccaaaaaaaacccaaaaccccccccccccccccaaaaaaaaaaccccccccccccccccccccccccccccccccccccccaaaaaccccccccccaaccccaaaaaaaaaaaaaajjjqqqttttxxxxyyyyyyvvrrrnnnfffcccccc
abccccccccccaaaaaaaaaccccccccccccccccccccaaaaaaaaaaaaacccccccccccccccccaacccccccccccccccccccaaaaaccccccaacaaaaaccaaaacaaaaaaaacjjjqqqqttttxxyywyyyywvrrnnnfffcccccc
abccccccccccaaaaaaaaaacccccccccccccccccccaaaaaaaaacaaacccccccccccccaaacaacccccccccccccccccccaaaaaccccccaaaaaaaaccaaaaccccaaacccjjjjqqqqtttxwywwwyywwwrrnnnfffcccccc
abcccccccccccccaaaaaaacccccccccccccccccccaaaaaaaaaaaaaaaacccccccccccaaaaaccccccccccccccccccaaaaacccaaccccaaaaccccaacaacccaaaccccjjjiqqqtttwwywwwwwwwwrrroofffcccccc
abcccccccccccccaaaccccccccccccccccccccccaaaaaaaaaaaaaaaaaccccccccccccaaaaaacccccccccccccccccccaaacaaaccccaaaaaccccccccccccccccccciiiiqqqttwwwwwswwwwrrrroofffcccccc
abcccccccccccccaaccccccccccccaaaacccccccaaaaaaaaccaaaaacccccccccccccaaaaaaacccccccccccccccccccaaaaaaacccaaacaacccccaaaaacccccccccciiiqqqttwwwwsssssrrrrroofffaccccc
abcccccccccccccccccccccccccccaaaaccccccccacaaacccaaaaaaccccccaaccccaaaaaaccccccccaacaaccccccccaaaaaaccccaaaacacccccaaaaacccccccccciiiqqqtsswsssssssrrrrooofffaccccc
abcccccccccccccccccccccccccccaaaaccccccccccaaaccaaaaaaaccccccaaaaccaacaaaccccccccaaaaacccccccccaaaaaaaaccaaacacccccaaaaaacccccccccciiqqqssssssspposrrroooofffaccccc
abccccaaacccccccccccccccccccccaaacccccccccccccccaaacaaaccccaaaaaacccccaaaccccccccaaaaaacccccccaaaaaaaaaaaaaaaaaccccaaaaaaccccccaccciiiqqpsssssppppooooooogffaaccccc
abccccaaaaaacccaaaccccccccccccccccccccccccccccccccccccaccccaaaaacccccccccccccccccaaaaaaccccccaaaaaaaaaaaaaaaaaaccccaaaaaacccaaaaccciiiqqppppppppppoooooogggfaaacccc
abcccaaaaaaacccaaaccccccccccccccccccccccccccccccccccccccccccaaaaaccccccccccccccccaaaaaaccccccaaacaaaccccaaaaaacccccccaacccccaaaaaacciiipppppppphgggggggggggaaaacccc
abccaaaaaaaacccaaacaaacccccccccccccccccccccaacccccccccccccccaacaacccccaacccccccccccaaacccccccccccaaacccccaaaaacccccccccccccccaaaaacciiihppppphhhhgggggggggaaccccccc
abccaaaaaaacaaaaaaaaaacccccccccccccccccccccaaaccccccacccccccccccccccccaaccccccccccccccccccccccccaaaaccccaaaaaaccccccccccccccaaaaacccciihhhhhhhhhhgggggggccaaccccccc
abccccaaaaaaaaaaaaaaacccccccccccccccccccaaaaaaaaccccaaacaaaccccccccccaaaaccaaccccccccaacaacccccaaaaaaacccaacccccccccccccccccaacaaccccchhhhhhhhhaaaacccccccccccccccc
abccccaaaaaacaaaaaaaccccccccccccccccccccaaaaaaaaccccaaaaaaaccccccccccaaaaaaaacaccccccaaaaaccccccaaaaacccccccccccccccccccccccccccccccccchhhhhhacaaaaaccccccccccccccc
abccccaaccccccaaaaaacccccccccccccaaccccccaaaaaacccccaaaaaaccccccaaaaaaaaaaaaaaaccccccaaaaaacccaaaaaaacccccccccccccccccccccccccccccccccccccaaaaccaaacccccccccccaaaca
abccccccccccccaaaaaaaccccccccccccaaccccccaaaaaacccaaaaaaaaccccccaaaaaaaaaaaaaacccccccaaaaaacccaaaaaaaaccccccaaacccccccccccccccccccccccccccaaaaccccccccccccccccaaaaa
abccaaacccccccaaacaaacccccccccaaaaaaaacccaaaaaacccaaaaaaaaacccccaaaaaaaaaaaaaacccccccaaaaaccccaaaaaaaaccccccaaaaccccccccccccccccccccccccccaaaccccccccccccccccccaaaa
abcaaaacccccccaaccccccccccccccaaaaaaaacccaaccaacccaaaaaaaaaaccccccccaaaaaaacaacccccccccaaaccccccaaacaaccccccaaaacccccccccccccccccccccccccccccccccccccccccccccaaaaaa
""", start_marker="S", goal_marker="E", is_possible=one_step_higher_or_below)
    return steps

def 本問題2():
    steps = solve("""abccccaaaaaaaaaaaaaccaaaaaaaacccccccccaaaaaaaaccccccccaaacaaacccccccaaaaaaccccccccccccccccccccccaaaacccccccccccacccccccccccccccccccccccccccccccccccccccccccccccaaaa
abccccaaaaacaaaaaaccccaaaaaaccccccccccaaaaaaacccccccccaaaaaaacccccaaaaaaaaaacccccccccccccccccccaaaaaacccccccccaaaaaaaaccccccccccccccccccccccccccccccccccccccccaaaaa
abcccaaaaaccaaaaaaccccaaaaaaccccccaacccaaaaaacccccccccaaaaaacccaaaaaaaaaaaaaaacaaccacccccccccccaaaaaaccccccccccaaaaaacccccccccccccccccccccccccccccccccccccccccaaaaa
abccccccaaccaaaaaaccaaaaaaaaccccccaaacaaaacaaacccccccaaaaaaaaccaaaaaaaaaaaaaaacaaaaacccccccccccccaaccccccccccccaaaaaaccccccccccccccccccccccccccccacccccccccccaaaaaa
abccccccccccaaccaaccaaaaccaacccccccaaaaaaaccccccccccaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaacccccccaaaaccccccccccccccccaaaaaaaacccccccccccccccccccccccccccaaccccccccccccccaa
abcccccccaaaaacccaaaaaaaacccaaccccaaaaaaccccccccccccaaaaaaaaaaaaaaaacaaaaaaaccaaaaaaccccccaaaaaccccccccccccccaaaaaaaaaaccaccccccccccccccccccccccccaccccccccccccccca
abcccccccaaaaacccaaaaaaaaccaaaaccaaaaaaaaccccccccccccccaaacaaaaaaaaacaaaaaacccccaaaacccccaaaaaaccccccccccccccaaaaaaaaaaaaacccccccccccccccllllllccccdccccccccccccccc
abccccccaaaaaacccccaaaaccccaaaaacaaaaaaaaccccccccccccccaaacccccaaaccccaaaaaacccaaccccccccaaaaaacccccccccccccccccaaaaaaaaaacccccccccccccklllllllllcddddccaccaaaccccc
abccccccaaaaaacccccaaaaaaaaaaaaaaaccaaccccccaacaacccccccaaccccccccccccaaacaacccccccccccccaaaaaacccccccccccccccccaaaaaaaaaacccccccccccckklllppllllcddddddddaaaaccccc
abccccccaaaaaaccccaaacaaaaaaaaaaaaccaaccccccaaaaaccccccccccccccccccccccccccccccccccccccccccaaccccccaaccccccccccccaacaaaaaaaccccccccccckklpppppplllmdddddddddacccccc
abccccccccaaacccccaacccaccaaaaaaccccccccccccaaaaaaccccccccccccccccccccccccccccccccccccccccccccccccaaaaccccccccccccaaaaaaaaaaccccccccckkkkppppppplmmmmmmddddddaacccc
abccccaaacaaacccccccccccccaaaaaaccccccccccccaaaaaacccccccccccccccccaaaccccccccccccccccccccccccccccaaaaccccccccccccaaaaaaaaaaccccccccckkkppppuppppmmmmmmmmddeeeacccc
abccccaaaaaaacccccccccccccaaaaaacccaccccccccaaaaaacccccccccccccccccaaaacccccccccccccccccccccaaacccaaaacccccccccccaaaacaaaccccccccccckkkpppuuuuuppqqmmmmmmmmeeeacccc
abcccccaaaaaaccccccccccccaaaaaaaacaaccccccccccaaaccccccccccccccccccaaaaccccccccccccccccccccaaaaccccccccccccccccccaaaaaaaacccccccccckkkkpppuuuuupqqqqqqqmmmmeeeccccc
abcccccaaaaaaaacccccccccccaccccaaaaacccccccccccccccccccccccccccccccaaaccccccccccccccaaaccccaaaacccccccccccccaaccaaaaaaaaccccccccckkkkkrrpuuuxuuuqqqqqqqqmmmmeeccccc
abccccaaaaaaaaaccccccccccccccaaaaaacccccccacaacccccccccccccccccccccccccccccccccccccaaaaaacccaaaccccccccccaaaaccaaaaaaacccccccccckkkkrrrrruuuxxuvvvvvvqqqqnnneeccccc
abcccaaaaaaaaaaccccccccccccccaaaaaaaacccccaaaaacccccccccccccccaaaaaccccccccccccccccaaaaaaccccccccccccccccaaaaaaaaaaaaacccccccccjjjkrrrrruuuxxxxvvvvvvvqqqnnneeccccc
abcaaaaacaaacccccccccccccccccaaaaaaaacccccaaaaaccaacccccccccccaaaaaccccccccccccccccaaaaaccccccccccccccccccaaaaaccaaaaaacccccccjjjrrrrruuuuuxxxyvyyyvvvqqqnneeeccccc
abcaaaaacaaaccaaccccccccccccccccaacccccccaaaaaaaaaaaccccccccccaaaaaaccccccccccccccccaaaaaccccccccccccccccaaaaacccaaaaaaaacaaacjjjrrrtttuuxxxxxyyyyyvvvqqnnneeeccccc
abaaaaaccaacccaaaccaacccaaccccccaccccccccaaaaaaaaaacccccccccccaaaaaaccccccccccccccccaacaacccccccccccccccccccaacccaaccccaaaaaacjjjrrrtttxxxxxxxyyyyyvvvrrnnneeeccccc
SbaaaaacccccccaaaaaaaccaaaacccccccccccccccaaaaaaaaacccccccccccaaaaaaccccccccccccccccccccccccccccccccccccccccccccccaacccaaaaaacjjjrrrtttxxxEzzzzyyyvvvrrnnneeecccccc
abcaaaaacccccccaaaaaaccaaaacccccccccccccccaaaaaaaaacccccccccccccaaccccccccccccccccccccccccccccaaccccccccccaaccccacaaaacaaaaaaajjjrrrtttxxxxxyyyyyvvvrrrnnnfffcccccc
abcaacccccccaaaaaaaacccaaaaccccccccccccccccaaaaaaaaaaccccccccccccccccccccccccccccccccccccccaaaaaccccccccccaaccccaaaaaaaaaaaaaajjjqqqttttxxxxyyyyyyvvrrrnnnfffcccccc
abccccccccccaaaaaaaaaccccccccccccccccccccaaaaaaaaaaaaacccccccccccccccccaacccccccccccccccccccaaaaaccccccaacaaaaaccaaaacaaaaaaaacjjjqqqqttttxxyywyyyywvrrnnnfffcccccc
abccccccccccaaaaaaaaaacccccccccccccccccccaaaaaaaaacaaacccccccccccccaaacaacccccccccccccccccccaaaaaccccccaaaaaaaaccaaaaccccaaacccjjjjqqqqtttxwywwwyywwwrrnnnfffcccccc
abcccccccccccccaaaaaaacccccccccccccccccccaaaaaaaaaaaaaaaacccccccccccaaaaaccccccccccccccccccaaaaacccaaccccaaaaccccaacaacccaaaccccjjjiqqqtttwwywwwwwwwwrrroofffcccccc
abcccccccccccccaaaccccccccccccccccccccccaaaaaaaaaaaaaaaaaccccccccccccaaaaaacccccccccccccccccccaaacaaaccccaaaaaccccccccccccccccccciiiiqqqttwwwwwswwwwrrrroofffcccccc
abcccccccccccccaaccccccccccccaaaacccccccaaaaaaaaccaaaaacccccccccccccaaaaaaacccccccccccccccccccaaaaaaacccaaacaacccccaaaaacccccccccciiiqqqttwwwwsssssrrrrroofffaccccc
abcccccccccccccccccccccccccccaaaaccccccccacaaacccaaaaaaccccccaaccccaaaaaaccccccccaacaaccccccccaaaaaaccccaaaacacccccaaaaacccccccccciiiqqqtsswsssssssrrrrooofffaccccc
abcccccccccccccccccccccccccccaaaaccccccccccaaaccaaaaaaaccccccaaaaccaacaaaccccccccaaaaacccccccccaaaaaaaaccaaacacccccaaaaaacccccccccciiqqqssssssspposrrroooofffaccccc
abccccaaacccccccccccccccccccccaaacccccccccccccccaaacaaaccccaaaaaacccccaaaccccccccaaaaaacccccccaaaaaaaaaaaaaaaaaccccaaaaaaccccccaccciiiqqpsssssppppooooooogffaaccccc
abccccaaaaaacccaaaccccccccccccccccccccccccccccccccccccaccccaaaaacccccccccccccccccaaaaaaccccccaaaaaaaaaaaaaaaaaaccccaaaaaacccaaaaccciiiqqppppppppppoooooogggfaaacccc
abcccaaaaaaacccaaaccccccccccccccccccccccccccccccccccccccccccaaaaaccccccccccccccccaaaaaaccccccaaacaaaccccaaaaaacccccccaacccccaaaaaacciiipppppppphgggggggggggaaaacccc
abccaaaaaaaacccaaacaaacccccccccccccccccccccaacccccccccccccccaacaacccccaacccccccccccaaacccccccccccaaacccccaaaaacccccccccccccccaaaaacciiihppppphhhhgggggggggaaccccccc
abccaaaaaaacaaaaaaaaaacccccccccccccccccccccaaaccccccacccccccccccccccccaaccccccccccccccccccccccccaaaaccccaaaaaaccccccccccccccaaaaacccciihhhhhhhhhhgggggggccaaccccccc
abccccaaaaaaaaaaaaaaacccccccccccccccccccaaaaaaaaccccaaacaaaccccccccccaaaaccaaccccccccaacaacccccaaaaaaacccaacccccccccccccccccaacaaccccchhhhhhhhhaaaacccccccccccccccc
abccccaaaaaacaaaaaaaccccccccccccccccccccaaaaaaaaccccaaaaaaaccccccccccaaaaaaaacaccccccaaaaaccccccaaaaacccccccccccccccccccccccccccccccccchhhhhhacaaaaaccccccccccccccc
abccccaaccccccaaaaaacccccccccccccaaccccccaaaaaacccccaaaaaaccccccaaaaaaaaaaaaaaaccccccaaaaaacccaaaaaaacccccccccccccccccccccccccccccccccccccaaaaccaaacccccccccccaaaca
abccccccccccccaaaaaaaccccccccccccaaccccccaaaaaacccaaaaaaaaccccccaaaaaaaaaaaaaacccccccaaaaaacccaaaaaaaaccccccaaacccccccccccccccccccccccccccaaaaccccccccccccccccaaaaa
abccaaacccccccaaacaaacccccccccaaaaaaaacccaaaaaacccaaaaaaaaacccccaaaaaaaaaaaaaacccccccaaaaaccccaaaaaaaaccccccaaaaccccccccccccccccccccccccccaaaccccccccccccccccccaaaa
abcaaaacccccccaaccccccccccccccaaaaaaaacccaaccaacccaaaaaaaaaaccccccccaaaaaaacaacccccccccaaaccccccaaacaaccccccaaaacccccccccccccccccccccccccccccccccccccccccccccaaaaaa
""", start_marker="E", goal_marker="a", is_possible=one_step_lower_or_above)
    return steps

if __name__=='__main__':
    print(本問題1())
    print(本問題2())
