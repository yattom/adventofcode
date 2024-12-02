def read_input(lines: list[str]) -> tuple[dict[str, list[str]], str]:
    replacements = {}
    for a, _, b in [l.split() for l in lines[:-2]]:
        if a not in replacements:
            replacements[a] = []
        replacements[a].append(b)
    # print(replacements)
    molecule_str = lines[-1]

    return replacements, molecule_str


def parse_molecule(molecule_str, replacements):
    head_lengths = (
        min([len(k) for k in replacements.keys()]),
        max([len(k) for k in replacements.keys()]))
    molecule = []
    idx = 0
    while idx < len(molecule_str):
        for l in range(head_lengths[0], head_lengths[1] + 1):
            part = molecule_str[idx:idx + l]
            # print(part)
            if part in replacements:
                molecule.append(part)
                idx += l
                break
        else:
            molecule.append(molecule_str[idx])
            idx += 1
    return molecule


def puzzle1(lines: list[str]):
    replacements, original_str = read_input(lines)
    original = parse_molecule(original_str, replacements)

    all_results = set()
    original_idx = 0
    while original_idx < len(original):
        part = original[original_idx]
        if part in replacements:
            for r in replacements[part]:
                all_results.add(''.join(original[:original_idx] + [r] + original[original_idx + 1:]))
        original_idx += 1

    return len(all_results)


def puzzle2(lines: list[str]):
    replacements, target = read_input(lines)
    results = [(target, 0)]
    while True:
        current, steps = results.pop(0)
        # print(f'{len(results)=} {current=} {steps=}')
        if current == 'e':
            return steps
        for part, replaced in replacements.items():
            for r in replaced:
                if r in current:
                    idx = 0
                    while idx < len(current):
                        idx = current.find(r, idx)
                        if idx == -1:
                            break
                        results.append((current[:idx] + part + current[idx + len(r):], steps + 1))
                        # print(f'{part=} {r=} {idx=} {results[-1]}')
                        idx += 1
        results.sort(key=lambda x: len(x[0]))

def main():
    import sys
    if len(sys.argv) == 1:
        lines = sys.stdin.readlines()
    else:
        with open(sys.argv[1]) as f:
            lines = f.readlines()
    print(puzzle1(lines))
    print(puzzle2(lines))


if __name__ == "__main__":
    main()
