"""Evolutionary update: x_next = x + 0.05 * x(1-x)(fC - fH).
fC = 4x ; fH = (6 - F)x + (1 - F)(1 - x). Start x=0.5, 30 updates, F in {0, 2}.
First no-fee step must give 0.48125 (fC=2, fH=3.5).
"""


def step(x, fee):
    f_c = 4 * x
    f_h = (6 - fee) * x + (1 - fee) * (1 - x)
    return x + 0.05 * x * (1 - x) * (f_c - f_h)


def path(fee, x0=0.5, n=30):
    xs = [x0]
    for _ in range(n):
        xs.append(step(xs[-1], fee))
    return xs


if __name__ == "__main__":
    print(step(0.5, 0))
