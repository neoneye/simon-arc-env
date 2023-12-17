from collections import Counter
import unittest
import numpy as np
import numpy.testing as npt
from simon_arc_env.image import Image

class TestImage(unittest.TestCase):
    def test_color(self):
        # Arrange + Act
        image = Image.color(3, 4, 5)
        # Assert
        self.assertEqual(image.pixels.shape, (4, 3))
        self.assertEqual(image.width, 3)
        self.assertEqual(image.height, 4)

    def test_from_1d_array_and_get(self):
        # Arrange
        pixels_1d = np.array([1, 2, 3, 4, 5, 6])
        # Act
        image = Image.from_1d_array(2, 3, pixels_1d)
        # Assert
        self.assertEqual(image.width, 2)
        self.assertEqual(image.height, 3)
        self.assertEqual(image.get(0, 0), 1)
        self.assertEqual(image.get(1, 0), 2)
        self.assertEqual(image.get(0, 1), 3)
        self.assertEqual(image.get(1, 1), 4)
        self.assertEqual(image.get(0, 2), 5)
        self.assertEqual(image.get(1, 2), 6)
        self.assertEqual(image.get(-1, -1), None)

    def test_set_and_pixels_1d(self):
        # Arrange
        image = Image.color(3, 4, 5)
        # Act
        image.set(1, 2, 42)
        # Assert
        pixels_1d = np.array([5, 5, 5, 5, 5, 5, 5, 42, 5, 5, 5, 5])
        npt.assert_array_equal(image.pixels_1d(), pixels_1d)

    def test_crop_success1(self):
        # Arrange
        pixels_1d = np.array([1, 2, 3, 4, 5, 6])
        image = Image.from_1d_array(2, 3, pixels_1d)
        # Act
        cropped = image.crop(0, 0, 2, 2)
        # Assert
        pixels_1d = np.array([1, 2, 3, 4])
        npt.assert_array_equal(cropped.pixels_1d(), pixels_1d)

    def test_crop_success2(self):
        # Arrange
        pixels_1d = np.array([1, 2, 3, 4, 5, 6])
        image = Image.from_1d_array(2, 3, pixels_1d)
        # Act
        cropped = image.crop(0, 1, 2, 2)
        # Assert
        pixels_1d = np.array([3, 4, 5, 6])
        npt.assert_array_equal(cropped.pixels_1d(), pixels_1d)

    def test_crop_success3(self):
        # Arrange
        pixels_1d = np.array([1, 2, 3, 4, 5, 6])
        image = Image.from_1d_array(3, 2, pixels_1d)
        # Act
        cropped = image.crop(1, 0, 2, 2)
        # Assert
        pixels_1d = np.array([2, 3, 5, 6])
        npt.assert_array_equal(cropped.pixels_1d(), pixels_1d)

    def test_crop_over_the_edge1(self):
        # Arrange
        pixels_1d = np.array([1, 2, 3, 4, 5, 6])
        image = Image.from_1d_array(3, 2, pixels_1d)
        # Act
        cropped = image.crop(-1, 0, 2, 2)
        # Assert
        self.assertEqual(cropped, None)

    def test_crop_over_the_edge2(self):
        # Arrange
        pixels_1d = np.array([1, 2, 3, 4, 5, 6])
        image = Image.from_1d_array(3, 2, pixels_1d)
        # Act
        cropped = image.crop(2, 0, 2, 2)
        # Assert
        self.assertEqual(cropped, None)

    def test_crop_over_the_edge3(self):
        # Arrange
        pixels_1d = np.array([1, 2, 3, 4, 5, 6])
        image = Image.from_1d_array(3, 2, pixels_1d)
        # Act
        cropped = image.crop(0, 1, 2, 2)
        # Assert
        self.assertEqual(cropped, None)

    def test_crop_empty(self):
        # Arrange
        pixels_1d = np.array([1, 2, 3, 4, 5, 6])
        image = Image.from_1d_array(3, 2, pixels_1d)
        # Act
        cropped = image.crop(0, 0, 0, 1)
        # Assert
        self.assertEqual(cropped, None)

    def test_equals(self):
        # Arrange
        image0 = Image.color(3, 4, 5)
        image1 = Image.color(3, 4, 5)
        image2 = Image.color(3, 4, 42)
        # Act
        self.assertEqual(image0.equals(image1), True)
        self.assertEqual(image0.equals(image0), True)
        self.assertEqual(image1.equals(image1), True)
        self.assertEqual(image2.equals(image2), True)
        self.assertEqual(image0.equals(image2), False)
        self.assertEqual(image1.equals(image2), False)

    def test_count_pixels_with_value(self):
        # Arrange
        pixels_1d = np.array([1, 2, 2, 3, 3, 3, 0, 0, 0])
        image = Image.from_1d_array(3, 3, pixels_1d)
        # Act + Assert
        self.assertEqual(image.count_pixels_with_value(0), 3)
        self.assertEqual(image.count_pixels_with_value(1), 1)
        self.assertEqual(image.count_pixels_with_value(2), 2)
        self.assertEqual(image.count_pixels_with_value(3), 3)
        self.assertEqual(image.count_pixels_with_value(4), 0)

    def test_histogram(self):
        # Arrange
        pixels_1d = np.array([1, 2, 2, 3, 3, 3, 0, 0, 0])
        image = Image.from_1d_array(3, 3, pixels_1d)
        # Act
        actual = image.histogram()
        # Assert
        expected = Counter({0: 3, 1: 1, 2: 2, 3: 3})
        self.assertEqual(actual, expected)
