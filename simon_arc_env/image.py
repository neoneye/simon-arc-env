from typing import Optional
from collections import Counter
import numpy as np

class Image:
    def __init__(self, pixels: np.ndarray):
        self.pixels = pixels

    @classmethod
    def from_1d_array(cls, width: int, height: int, pixels_1d: np.ndarray) -> 'Image':
        if pixels_1d.size != width * height:
            raise ValueError("The size of the 1D array does not match the specified width and height.")
        pixels_1d = pixels_1d.astype(np.uint8)
        pixels_2d = pixels_1d.reshape((height, width))
        return cls(pixels_2d)

    @classmethod
    def color(cls, width: int, height: int, color: int) -> 'Image':
        rows = []
        for _ in range(height):
            columns = [color] * width
            rows.append(columns)
        pixels = np.array(rows, np.uint8)
        return cls(pixels)
    
    @property
    def width(self) -> int:
        return self.pixels.shape[1]

    @property
    def height(self) -> int:
        return self.pixels.shape[0]
    
    def pixels_1d(self) -> np.ndarray:
        return self.pixels.flatten()

    def get(self, x: int, y: int) -> Optional[int]:
        if x < 0 or y < 0:
            return None
        if x >= self.width or y >= self.height:
            return None
        return self.pixels[y][x]

    def set(self, x: int, y: int, value: int):
        if x < 0 or y < 0:
            return
        if x >= self.width or y >= self.height:
            return            
        self.pixels[y][x] = value

    def crop(self, x: int, y: int, width: int, height: int) -> Optional['Image']:
        if width <= 0 or height <= 0:
            return None
        if x < 0 or y < 0:
            return None
        if x > self.width - width or y > self.height - height:
            return None
        pixels = self.pixels[y:y+height, x:x+width]
        return Image(pixels)
    
    def equals(self, other_image: 'Image') -> bool:
        """Check if this image is identical to another image."""
        if not isinstance(other_image, Image):
            return False
        return np.array_equal(self.pixels, other_image.pixels)

    def count_pixels_with_value(self, value: int) -> int:
        """Count the number of pixels in the image that have the specified value."""
        return np.sum(self.pixels == value)

    def histogram(self) -> Counter:
        """ Extracts the histogram of the image. """
        flat_pixels = self.pixels_1d()
        histogram = Counter(flat_pixels)
        return histogram
