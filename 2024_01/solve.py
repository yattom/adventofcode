import sys

list1 = []
list2 = []

for line in sys.stdin.readlines():
    if not line.strip():
        break
    line = line.strip()
    v1, v2 = line.split()
    list1.append(int(v1))
    list2.append(int(v2))

list1.sort()
list2.sort()


def puzzle1(list1, list2):
    total_distance = 0
    for z in zip(list1, list2):
        total_distance += abs(z[1] - z[0])

    print(total_distance)


def puzzle2(list1, list2):
    appearance_count2 = {}
    for v in list2:
        if v not in appearance_count2:
            appearance_count2[v] = 0
        appearance_count2[v] += 1

    total_similarity = sum({v * appearance_count2.get(v, 0) for v in list1})
    print(total_similarity)


def main():
    puzzle1(list1, list2)
    puzzle2(list1, list2)


if __name__ == "__main__":
    main()
