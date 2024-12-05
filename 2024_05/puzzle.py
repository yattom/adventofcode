def puzzle1(lines: list[str]):
    orders = []
    manuals = []
    for l in lines:
        if '|' in l:
            a, b = [int(v) for v in l.strip().split('|')]
            orders.append((a, b))
        elif ',' in l:
            vals = [int(v) for v in l.strip().split(',')]
            manuals.append(vals)

    print(orders)
    print(manuals)
    total = 0
    for update in manuals:
        for p, q in orders:
            if p in update and q in update:
                if not update.index(p) < update.index(q):
                    break
        else:
            total += update[len(update) // 2]

    return total


def is_in_order(update: list[int], orders: list[tuple[int, int]]):
    correct = True
    for p, q in orders:
        if p in update and q in update:
            if not update.index(p) < update.index(q):
                correct = False
    return correct


def puzzle2(lines: list[str]):
    orders = []
    manuals = []
    for l in lines:
        if '|' in l:
            a, b = [int(v) for v in l.strip().split('|')]
            orders.append((a, b))
        elif ',' in l:
            vals = [int(v) for v in l.strip().split(',')]
            manuals.append(vals)

    print(orders)
    print(manuals)
    total = 0
    for update in manuals:
        if is_in_order(update, orders):
            continue
        while not is_in_order(update, orders):
            print(f'before: {update}')
            for p, q in orders:
                if p in update and q in update:
                    if not update.index(p) < update.index(q):
                        i_p = update.index(p)
                        i_q = update.index(q)
                        update = update[:i_q] + [p] + update[i_q:i_p] + update[i_p + 1:]
                        print(
                            f'p: {p}, q: {q}, i_p: {i_p}, i_q: {i_q}, update: {update}')
            print(f'after: {update}')
        total += update[len(update) // 2]

    return total



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
