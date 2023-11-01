def build_files(puzzle_input):
    pwd = ROOT = ('/',)
    files = {('d', ROOT): 0}
    for cmdline in puzzle_input:
        cmd = cmdline.strip().split(' ')
        match cmd:
            case ['$', 'cd', path]:
                if path == '/':
                    pwd = ROOT
                elif path == '..':
                    pwd = pwd[:-1]
                else:
                    pwd = pwd + (path,)
                    if ('d', pwd) not in files:
                        files[('d', pwd)] = 0
            case ['$', 'ls']:
                continue
            case [info, pathname]:
                fullpath = pwd + (pathname,)
                if info == 'dir':
                    if ('d', fullpath) not in files:
                        files[('d', fullpath)] = 0
                else:
                    size_ = int(info)
                    if ('f', fullpath) not in files:
                        files[('f', fullpath)] = size_
                        while fullpath != ROOT:
                            fullpath = fullpath[:-1]
                            files[('d', fullpath)] += size_

    return files


def test_build_files():
    puzzle_input = [
        "$ cd /",
        "$ ls",
        "dir a",
        "14848514 b.txt",
        "8504156 c.dat",
        "dir d",
        "$ cd a",
        "$ ls",
        "dir e",
        "29116 f",
        "2557 g",
        "62596 h.lst",
        "$ cd e",
        "$ ls",
        "584 i",
        "$ cd ..",
        "$ cd ..",
        "$ cd d",
        "$ ls",
        "4060174 j",
        "8033020 d.log",
        "5626152 d.ext",
        "7214296 k",
    ]
    files = build_files(puzzle_input)
    expected = {('d', ('/',)): 48381165,
                ('d', ('/', 'a')): 94853,
                ('d', ('/', 'a', 'e')): 584,
                ('d', ('/', 'd')): 24933642,
                ('f', ('/', 'a', 'e', 'i')): 584,
                ('f', ('/', 'a', 'f')): 29116,
                ('f', ('/', 'a', 'g')): 2557,
                ('f', ('/', 'a', 'h.lst')): 62596,
                ('f', ('/', 'b.txt')): 14848514,
                ('f', ('/', 'c.dat')): 8504156,
                ('f', ('/', 'd', 'd.ext')): 5626152,
                ('f', ('/', 'd', 'd.log')): 8033020,
                ('f', ('/', 'd', 'j')): 4060174,
                ('f', ('/', 'd', 'k')): 7214296}
    assert files == expected


def test_solve2():
    puzzle_input = [
        "$ cd /",
        "$ ls",
        "dir a",
        "14848514 b.txt",
        "8504156 c.dat",
        "dir d",
        "$ cd a",
        "$ ls",
        "dir e",
        "29116 f",
        "2557 g",
        "62596 h.lst",
        "$ cd e",
        "$ ls",
        "584 i",
        "$ cd ..",
        "$ cd ..",
        "$ cd d",
        "$ ls",
        "4060174 j",
        "8033020 d.log",
        "5626152 d.ext",
        "7214296 k",
    ]
    assert solve2(puzzle_input) == 24933642


def solve(puzzle_input):
    files = build_files(puzzle_input)
    total = 0
    for (type_, fullpath), size_ in files.items():
        if type_ == 'd' and size_ <= 100000:
            total += size_
    return total


def solve2(puzzle_input):
    files = build_files(puzzle_input)
    free = 70000000 - files[('d', ('/',))]
    dirs = [(fullpath, size_) for (type_, fullpath), size_ in files.items() if type_ == 'd']
    for f, s in sorted(dirs, key=lambda v: v[1]):
        if free + s >= 30000000:
            return s



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
