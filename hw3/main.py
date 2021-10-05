import numpy as np
import scipy.stats
import time


def load_data(file_path):
    try:
        with open(file_path, "r") as f:
            return np.array([list(map(int, line.split())) for line in f.readlines()])
    except Exception as e:
        print('Error during parsing data: ', e)
        exit(1)


def validate_data(np_data):
    assert np_data.dtype == np.int64, "File content must contain only integers"
    assert (len(np_data.shape) == 2 and np_data.shape[1] == 2), "File format error: each lime must contain two integers"

    assert np_data.shape[0] >= 9, "At least 9 entries must be provided in input"


if __name__ == '__main__':
    start_time = time.time()
    current_time = time.time()

    data = load_data("in.txt")
    validate_data(data)

    print(f'Data loaded. Consumed time: {round(time.time() - current_time, 5)}', flush=True)
    current_time = time.time()

    n = data.shape[0]
    data = data[data[:, 0].argsort()]
    ranks = scipy.stats.rankdata(-data[:, 1])

    p = int(n / 3)
    diff = ranks[:p].sum() - ranks[-p:].sum()
    std = (n + 0.5) * (p / 6.) ** 0.5
    conj = diff / p / (n - p)

    print(f'Algorithm completed. Consumed time: {round(time.time() - current_time, 5)}', flush=True)

    with open("out.txt", "w") as f:
        f.write(f'{int(np.rint(diff))} {int(np.rint(std))} {round(conj, 2)}')

    print(f'Done! Total time: {round(time.time() - start_time, 5)}', flush=True)
