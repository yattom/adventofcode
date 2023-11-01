with open("my.out", "r") as f:
    my = f.read().splitlines()

with open("ref.out", "r") as f:
    ref = f.read().splitlines()

if len(my) != len(ref):
    raise RuntimeError("count of length differ")

for i in range(len(my)):
    m = eval(my[i])
    r = eval(ref[i])
    zero_idx = r.index(0)
    r = r[zero_idx:] + r[:zero_idx]
    if m != r:
        print(f"differ #{i + 1}")
        for j in range(len(m)):
            if m[j] != r[j]:
                print(f"diff @{j} m[{j}]={m[j]} r[{j}]={r[j]}")
                for k in range(max(0, j - 2), min(j + 2, len(my))):
                    print(f"m[{k}]={m[k]} r[{k}]={r[k]}")
        # print(m)
        # print(r)
        raise RuntimeError(f"differ #{i + 1}")

