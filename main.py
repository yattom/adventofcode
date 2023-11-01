def main(solve_puzzle1, solve_puzzle2):
    with open("puzzle_input.txt") as f:
        puzzle_input = f.read().splitlines()
    solve_puzzle1(puzzle_input)
    solve_puzzle2(puzzle_input)
