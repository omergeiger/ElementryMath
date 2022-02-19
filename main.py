from model import Model

if __name__ == '__main__':
    model = Model(max_a=5, max_b=10, random_swap=True, random_portion=0.75, timeout=25)
    model.study(num_exercises=10)

    # debug
    # print(sorted(model.history.items(), key=lambda ((a, b), (c, i)): (i, c), reverse=True))
