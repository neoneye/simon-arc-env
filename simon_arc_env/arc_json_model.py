import json
import numpy as np
from enum import Enum

class PairType(Enum):
    TRAIN = 0
    TEST = 1

class Image:
    def __init__(self, pixels: np.ndarray, id: str):
        self.pixels = pixels
        self.id = id

    @classmethod
    def create_from_json(cls, pixels_json, id: str) -> 'Image':
        pixels = np.array(pixels_json, np.uint8)
        return Image(pixels, id)
    
    @property
    def is_empty(self) -> bool:
        return self.pixels.size == 0

class Pair:
    def __init__(self, input: Image, output: Image, pair_type: PairType, pair_index: int):
        self.input = input
        self.output = output
        self.pair_type = pair_type
        self.pair_index = pair_index

    @classmethod
    def create_from_json(cls, pair_json, pair_type: PairType, pair_index: int) -> 'Pair':
        pair_type_name = 'train'
        if pair_type == PairType.TEST:
            pair_type_name = "test"
        input = Image.create_from_json(pair_json['input'], f'{pair_type_name} {pair_index} in')
        output = Image.create_from_json(pair_json['output'], f'{pair_type_name} {pair_index} out')
        return Pair(input, output, pair_type, pair_index)

class Task:
    def __init__(self, pairs: [Pair]):
        self.pairs = pairs
  
    @classmethod
    def load(cls, path) -> 'Task':
        with open(path) as f:
            json_data = json.load(f)

        pairs = []
        for pair_index, json_pair in enumerate(json_data['train']):
            pair = Pair.create_from_json(json_pair, PairType.TRAIN, pair_index)
            pairs.append(pair)
        for pair_index, json_pair in enumerate(json_data['test']):
            pair = Pair.create_from_json(json_pair, PairType.TEST, pair_index)
            pairs.append(pair)
        return Task(pairs)

    def train_test(self) -> (int, int):
        count_train = 0
        count_test = 0
        for pair in self.pairs:
            if pair.pair_type == PairType.TRAIN:
                count_train += 1
            else:
                count_test += 1
        return (count_train, count_test)

if __name__ == '__main__':
    path = 'assets/0b17323b.json'
    task = Task.load(path)
    print(task)
