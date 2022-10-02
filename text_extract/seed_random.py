import numpy as np


class random:
    def __init__(self, seed):
        self.seed = seed

    def random(self):
        self.seed = (1013904223 + 1664525 * self.seed) % 4294967296
        return self.seed / 4294967296

    def choice(self, array):
        idx = round(self.random() * len(array) - 0.5)
        return array[idx]


def make_random_text(seed: int, text_len: int) -> np.ndarray:
    """주어진 길이만큼의 랜덤한 텍스트를 생성함

    Args:
        seed (int): 랜덤 시드
        text_len (int) 생성할 텍스트의 길이

    Returns:
        np.ndarray: 랜덤한 텍스트의 아스키코드들을 ndarray형태로 반환함
    """
    rnd = random(seed)
    char_list = [i - 0x21 for i in range(0x21, 0x7F)]

    rnd.random()  # 더 랜덤한 값을 위해 랜덤 함수를 한 번 실행해 줌
    random_text = []

    for i in range(text_len):
        random_text.append(rnd.choice(char_list))

    return np.asarray(random_text, dtype=np.int8)


if __name__ == "__main__":
    pass
