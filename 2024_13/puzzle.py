import re


def read_machines(lines: list[str]):
    machines = []
    for line in lines:
        match line.strip():
            case _ if line.startswith('Button A:'):
                machine = {}
                vals = re.search(r'Button A: X\+(\d+), Y\+(\d+)', line).groups()
                machine['A'] = (int(vals[0]), int(vals[1]))
            case _ if line.startswith('Button B:'):
                vals = re.search(r'Button B: X\+(\d+), Y\+(\d+)', line).groups()
                machine['B'] = (int(vals[0]), int(vals[1]))
            case _ if line.startswith('Prize:'):
                vals = re.search(r'Prize: X=(\d+), Y=(\d+)', line).groups()
                machine['prize'] = (int(vals[0]), int(vals[1]))
                machines.append(machine)
            case '':
                continue
    return machines


def puzzle1(lines: list[str]):
    machines = read_machines(lines)
    tokens = calc_tokens(machines)
    return tokens


def calc_tokens(machines):
    tokens = 0
    for yp in machines:
        xa, ya = yp['A']
        xb, yb = yp['B']
        xp, yp = yp['prize']
        if (xa * yp - xp * ya) / (xa * yb - xb * ya) == 0.0:
            print(f"A: {(xa, ya)}, B: {(xb, yb)}, {xp=}, {yp=}")
        else:
            a = round(xp / xa - xb * (xa * yp - xp * ya) / (xa * yb - xb * ya) / xa)
            # a = (xa * yp - xp * ya) / (xa * yb - xb * ya)
            b = round((xa * yp - xp * ya) / (xa * yb - xb * ya))
            # if a % 1 == 0 and b % 1 == 0:
            if (int(a * xa + b * xb) == xp and
                    int(a * ya + b * yb) == yp):
                tokens += int(a * 3 + b * 1)
            else:
                # print(f"{a=}, {b=}, xv-uy={xa*yb-xb*ya}, {xp=}, ax+bu={a*xa+b*xb}, {yp=}, ay+bv={a*ya+b*yb}")
                pass
    return tokens


def puzzle2(lines: list[str]):
    machines = read_machines(lines)
    for m in machines:
        m['prize'] = (m['prize'][0] + 10000000000000, m['prize'][1] + 10000000000000)
    tokens = calc_tokens(machines)
    return tokens


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
