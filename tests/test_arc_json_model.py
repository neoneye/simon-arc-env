import os
import unittest
import simon_arc_env.arc_json_model as ajm

class TestArcJsonModel(unittest.TestCase):
    def test_load(self):
        # Arrange
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets", "62c24649.json")
        # Act
        task = ajm.Task.load(path)
        # Assert
        self.assertEqual(len(task.pairs), 4)
        self.assertEqual(task.train_test(), (3, 1))
        pair0 = task.pairs[0]
        self.assertEqual(pair0.input.pixels.shape, (3, 3))
        self.assertEqual(pair0.output.pixels.shape, (6, 6))
        pair3 = task.pairs[3]
        self.assertEqual(pair3.pair_type, ajm.PairType.TEST)
        self.assertEqual(pair3.output.is_empty, False)

    def test_image_is_empty(self):
        # Arrange
        json = {
            "input": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            "output": []
        }
        # Act
        pair = ajm.Pair.create_from_json(json, ajm.PairType.TEST, 0)
        # Assert
        self.assertEqual(pair.input.pixels.shape, (3, 3))
        self.assertEqual(pair.output.pixels.shape, (0,))
        self.assertEqual(pair.output.pixels.size, 0)
        self.assertEqual(pair.output.is_empty, True)
