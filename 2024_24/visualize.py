import sys
from puzzle import Puzzle


def visualize(puzzle):
    seq_no = 0
    created_objects = set()
    print('@startuml')
    print('hide empty members')
    for label, gate in puzzle.gates.items():
        logic = f'logic{seq_no}'
        seq_no += 1
        if gate.ins[0] not in created_objects:
            print(f'object {gate.ins[0]}')
        if gate.ins[1] not in created_objects:
            print(f'object {gate.ins[1]}')
        if gate.out not in created_objects:
            print(f'object {gate.out}')
        print(f'object "{gate.logic}" as {logic}')
        print(f'{gate.ins[0]} -d-> {logic}')
        print(f'{gate.ins[1]} -d-> {logic}')
        print(f'{logic} -d-> {gate.out}')
        print()

        created_objects |= {gate.ins[0], gate.ins[1], gate.out}

    for obj in created_objects:
        if obj.startswith('x'):
            num = int(obj[1:])
            next_obj = f'y{num:02d}'
            if next_obj in created_objects:
                print(f'{obj} -r[hidden]-> {next_obj}')
        if obj.startswith('y'):
            num = int(obj[1:])
            next_obj = f'x{num + 1:02d}'
            if next_obj in created_objects:
                print(f'{obj} -r[hidden]-> {next_obj}')
        if obj.startswith('z'):
            num = int(obj[1:])
            next_obj = f'z{num + 1:02d}'
            if next_obj in created_objects:
                print(f'{obj} -r[hidden]-> {next_obj}')
    print('@enduml')


def main():
    lines = sys.stdin.readlines()
    puzzle = Puzzle.build_puzzle(lines)
    visualize(puzzle)


if __name__ == "__main__":
    main()
