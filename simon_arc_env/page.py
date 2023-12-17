from typing import SupportsFloat
from .image import Image
from . import arc_json_model as ajm

class Page:
    def __init__(self, image: Image, width: int, height: int, pair_type: ajm.PairType, is_output: bool, is_editor: bool, expected_test_output: Image | None) -> None:
        self.number_of_changes_image = Image.color(image.width, image.height, 0)
        self.image = image
        self.width = width
        self.height = height
        self.pair_type = pair_type
        self.is_output = is_output
        self.is_editor = is_editor
        self.expected_test_output = expected_test_output

    @classmethod
    def create(cls, pair: ajm.Pair, is_output: bool) -> 'Page':
        image = Image.color(30, 30, 11)
        source = pair.input
        if is_output:
            source = pair.output
        pixels = source.pixels
        for row_index, rows in enumerate(pixels):
            for column_index, pixel in enumerate(rows):
                image.set(column_index, row_index, pixel)
        return cls(image, pixels.shape[1], pixels.shape[0], pair.pair_type, is_output, False, None)

    @classmethod
    def create_test_output_editor(cls, pair: ajm.Pair, is_output: bool) -> 'Page':
        expected_test_output = None
        if pair.output.is_empty == False:
            shape = pair.output.pixels.shape
            expected_test_output = Image.color(shape[1], shape[0], 255)
            for row_index, rows in enumerate(pair.output.pixels):
                for column_index, pixel in enumerate(rows):
                    expected_test_output.set(column_index, row_index, pixel)

        image = Image.color(30, 30, 11)
        return cls(image, 30, 30, pair.pair_type, is_output, True, expected_test_output)

    @classmethod
    def create_pages(cls, task: ajm.Task) -> ['Page']:
        pages = []
        for pair in task.pairs:
            if pair.pair_type == ajm.PairType.TRAIN:
                pages.append(Page.create(pair, False))
                pages.append(Page.create(pair, True))
            if pair.pair_type == ajm.PairType.TEST:
                pages.append(Page.create(pair, False))
                pages.append(Page.create_test_output_editor(pair, True))
        return pages

    def handle_set_pixel(self, x: int, y: int, color: int) -> SupportsFloat:
        if not self.is_editor:
            return 0.0
        
        self.image.set(x, y, color)
        count = self.number_of_changes_image.get(x, y)
        if count < 6:
            count += 1
            self.number_of_changes_image.set(x, y, count)
        
        rewards = {
            1: 1.0,
            2: 0.5,
            3: 0.25,
            4: -0.25,
            5: -0.5,
            6: -1.0
        }
        return rewards.get(count, -5.0)

    def cropped_image(self) -> Image:
        return self.image.crop(0, 0, self.width, self.height)
