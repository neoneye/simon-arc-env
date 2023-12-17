# Weakness:
# Cannot deal with tasks that have 2 or more test pairs.
# the ARC dataset has several tasks with 2 or more test pairs.
# Rework the Page.create_pages() so it can deal with tasks that have 2 or more test pairs.
#
# Available actions on every page:
# Show a bit mask of the available actions in the right side of the 32x32 image.
# The editor page has several actions enabled.
# The non-editor pages has few actions enabled.
# This way the RL knows what actions are available here.
from typing import Any, Dict, List, SupportsFloat, Tuple
from gymnasium.core import ActType, ObsType, RenderFrame
import os
import gymnasium as gym
import numpy as np
import pygame
from gymnasium.spaces import Box, Discrete
from .colors import *
from .cursors import Cursors
from .image import Image
from .page import Page
from .actions import Actions
from . import arc_json_model as ajm

class SimonARCEnv(gym.Env):
    action_space = Discrete(Actions.number_of_actions())
    observation_space = Box(low=0, high=255, shape=(32, 32), dtype=np.uint8)

    metadata = {"render_modes": ["human"], "render_fps": 60}

    def __init__(self, render_mode: str | None = None, path_to_task_dir: str | None = None):
        super().__init__()
        self.render_mode = render_mode

        self._surface = None
        self._cursors = None

        self.assign_default_values()

        scale = 20
        width = 32 * scale
        height = 32 * scale
        self._width = width
        self._height = height
        self._scale = scale

        tasks = []
        if path_to_task_dir is None:
            path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets", "68b67ca3.json")
            task = ajm.Task.load(path)
            tasks.append(task)
        else:
            all_filenames_unordered = os.listdir(path_to_task_dir)
            json_filenames_unordered = [f for f in all_filenames_unordered if f.endswith(".json")]
            json_filenames_sorted = sorted(json_filenames_unordered)
            # print(f"Loading {len(json_filenames_sorted)} tasks from {path_to_task_dir}")
            for json_filename in json_filenames_sorted:
                path = os.path.join(path_to_task_dir, json_filename)
                task = ajm.Task.load(path)
                _, test = task.train_test()
                if test >= 2:
                    print(f"Skipping task with 2 or more test pairs. filename: {json_filename}")
                    continue
                tasks.append(task)

        assert len(tasks) > 0, "Unable to load any tasks from the given directory."

        self._tasks = tasks
        self._task = self._tasks[0]
        self._pages = Page.create_pages(self._task)
        self._page = self._pages[self._page_index]

    def assign_default_values(self) -> None:
        self._cursor_x = 0
        self._cursor_y = 0
        self._color = 0
        self._page_index = 0
        self._count_set_pixel = 0
        self._count_step = 0
        self._last_action = 0
        self._previous_score = 0.0
        self._total_score = 0.0
        self._count_set_pixel = 0
        self._running = True

    @property
    def observation(self) -> ObsType:
        image = self.render_image()
        assert image.width == 32
        assert image.height == 32
        return image.pixels

    def is_terminated(self) -> bool:
        return False

    def is_truncated(self) -> bool:
        if self._count_set_pixel > 30 * 30 * 120 / 100:
            # kill the agent if it spends too much time on drawing redundant pixels.
            print("Truncated because of too many pixels.")
            return True
        if self._count_step > 200:
            # kill the agent if it spends on interacting without making progress.
            print("Truncated because of too many steps.")
            return True
        return False

    @property
    def info(self) -> Dict[str, Any]:
        return {
            "cursor_x": self._cursor_x,
            "cursor_y": self._cursor_y,
            "color": self._color,
            "page_index": self._page_index,
            "last_action": self._last_action
        }

    def step(self, action: ActType) -> \
            tuple[ObsType, SupportsFloat, bool, bool, Dict[str, Any]]:

        assert self._running, "You must reset the environment before calling step() again."

        self._count_step += 1

        terminated = self.is_terminated()
        truncated = self.is_truncated()

        if action == Actions.NEXT_PAGE.value:
            # print("Action - next page / submit.")
            if self._page.is_editor:
                # self._total_score += 0.01
                pass
            else:
                self._total_score -= 1.0

            self._page_index = (self._page_index + 1) % len(self._pages)
            self._page = self._pages[self._page_index]

        if action == Actions.SUBMIT_DRAWING.value:
            # print("Action - submit drawing.")
            if self._page.is_editor:
                self._total_score += 1.0
                predicted_image = self._page.cropped_image()

                # reward 1000 minus the number of unassigned pixels
                unassigned_pixels = predicted_image.count_pixels_with_value(11)
                self._total_score += 1000.0 - unassigned_pixels
                # print(f"predicted size: {predicted_image.width}x{predicted_image.height}")
                # print(predicted_image.pixels)

                if self._page.expected_test_output is not None:
                    expected_image = self._page.expected_test_output
                    # print("Expected output:")
                    # print(f"expected size: {expected_image.width}x{expected_image.height}")
                    # print(expected_image.pixels)
                    if predicted_image.width == expected_image.width:
                        self._total_score += 100.0
                    if predicted_image.height == expected_image.height:
                        self._total_score += 100.0
                    if predicted_image.histogram() == expected_image.histogram():
                        # Reward when the predicted histogram is correct.
                        self._total_score += 100.0
                    if predicted_image.equals(expected_image):
                        # High reward when the prediction is correct.
                        self._total_score += 10000.0

                terminated = True # ends the game the correct way
            else:
                # self._total_score -= 1000.0
                # self._total_score -= 1.0
                # self._total_score = 0.0
                truncated = True # aborts the game prematurely

        if action == Actions.SET_PIXEL.value:
            self._total_score += self._page.handle_set_pixel(self._cursor_x, self._cursor_y, self._color)
            self._count_set_pixel += 1

        if action == Actions.MOVE_UP.value:
            # print("Action - move up.")
            if self._page.is_editor:
                self._cursor_y = (self._cursor_y - 1) % 30
                self._total_score += 0.01
            else:
                # self._total_score -= 1.0
                pass

        if action == Actions.MOVE_DOWN.value:
            # print("Action - move down.")
            if self._page.is_editor:
                self._cursor_y = (self._cursor_y + 1) % 30
                self._total_score += 0.01
            else:
                # self._total_score -= 1.0
                pass

        if action == Actions.MOVE_LEFT.value:
            # print("Action - move left.")
            if self._page.is_editor:
                self._cursor_x = (self._cursor_x - 1) % 30
                self._total_score += 0.01
            else:
                # self._total_score -= 1.0
                pass

        if action == Actions.MOVE_RIGHT.value:
            # print("Action - move right.")
            if self._page.is_editor:
                self._cursor_x = (self._cursor_x + 1) % 30
                self._total_score += 0.01
            else:
                # self._total_score -= 1.0
                pass

        if action == Actions.INCREMENT_COLOR.value:
            # print("Action - increment color.")
            if self._page.is_editor:
                self._color = (self._color + 1) % 10
                self._total_score += 0.01
            else:
                # self._total_score -= 1.0
                pass

        if action == Actions.DECREMENT_COLOR.value:
            # print("Action - decrement color.")
            if self._page.is_editor:
                self._color = (self._color - 1) % 10
                self._total_score += 0.01
            else:
                # self._total_score -= 1.0
                pass

        if action == Actions.ADJUST_CANVAS_SIZE.value:
            if self._page.is_editor:
                new_width = (self._cursor_x + 1) % 31
                new_height = (self._cursor_y + 1) % 31
                # print("Action - adjust canvas size. Width: " + str(new_width) + ", Height: " + str(new_height))
                if new_width == self._page.width and new_height == self._page.height:
                    # Adjusting output size to the same size as it already has.
                    self._total_score -= 1.0
                else:
                    self._total_score += 0.01
                    self._page.width = new_width
                    self._page.height = new_height
            else:
                # self._total_score -= 1.0
                pass

        if self.render_mode is not None:
            self.render()

        reward = self._total_score - self._previous_score
        self._previous_score = self._total_score

        self._last_action = action

        if terminated or truncated:
            self._running = False

        return self.observation, reward, terminated, truncated, self.info

    def reset(self, *, seed: int | None = None,
              options: Dict[str, Any] | None = None) \
            -> Tuple[ObsType, Dict[str, Any]]:

        super().reset(seed=seed)
        # print(f"Resetting the environment. steps: {self._count_step} score: {self._total_score}")

        self._surface = None
        self._cursors = None

        self.assign_default_values()

        self._task = self.np_random.choice(self._tasks)
        self._pages = Page.create_pages(self._task)    
        self._page = self._pages[self._page_index]

        if self.render_mode is not None:
            self.render()

        return self.observation, self.info
    
    def render_image(self) -> Image:
        image = Image.color(32, 32, 255)
        for row_index, rows in enumerate(self._page.image.pixels):
            for column_index, pixel in enumerate(rows):
                x = (column_index + 1) * self._scale
                y = (row_index + 1) * self._scale
                image.set(x, y, pixel)

        if self._page.is_editor:
            image.set(0, 0, self._color)
            image.set(self._cursor_x + 1, 0, 254)
            image.set(0, self._cursor_y + 1, 254)

        # Indicate if the image is input or output.
        if self._page.is_output:
            image.set(1, 31, 254)
        else:
            image.set(0, 31, 254)

        # Indicate if the image is train or test.
        if self._page.pair_type == ajm.PairType.TRAIN:
            image.set(2, 31, 254)
        else:
            image.set(3, 31, 254)

        return image

    def render(self) -> RenderFrame | List[RenderFrame] | None:
        if self.render_mode != "human":
            return None
        
        if self._surface is None:
            pygame.init()
            pygame.display.init()
            pygame.display.set_caption("SimonARC")
            size = (self._width, self._height)
            self._surface = pygame.display.set_mode(size)

        assert self._surface is not None, \
            "Something went wrong with pygame. This should never happen."

        if self._cursors is None:
            self._cursors = Cursors(self._scale)

        color = COLOR_PALETTE[min(max(11, 0), 11)]
        pygame.draw.rect(self._surface, color, pygame.Rect(0, 0, self._width, self._height))

        show_grid = False
        if self._scale > 5:
            show_grid = True

        cell_size = self._scale
        if show_grid:
            cell_size = cell_size - 1

        if self._page.is_editor:
            color = COLOR_PALETTE[min(max(self._color, 0), 11)]
            pygame.draw.rect(self._surface, color, pygame.Rect(0, 0, cell_size, cell_size))

        page_width = self._page.width
        page_height = self._page.height

        if show_grid:
            pygame.draw.rect(self._surface, (200, 200, 200), pygame.Rect(self._scale - 1, self._scale - 1, self._page.image.width * self._scale + 1, self._page.image.height * self._scale + 1))
            pygame.draw.rect(self._surface, (40, 40, 40), pygame.Rect(self._scale - 1, self._scale - 1, page_width * self._scale + 1, page_height * self._scale + 1))

        for row_index, rows in enumerate(self._page.image.pixels):
            for column_index, pixel in enumerate(rows):
                x = (column_index + 1) * self._scale
                y = (row_index + 1) * self._scale
                color = COLOR_PALETTE[min(max(pixel, 0), 11)]
                if column_index >= page_width or row_index >= page_height:
                    r = int(color[0] * 0.5 + 127)
                    g = int(color[1] * 0.5 + 127)
                    b = int(color[2] * 0.5 + 127)
                    color = (r, g, b)
                pygame.draw.rect(self._surface, color, pygame.Rect(x, y, cell_size, cell_size))

        if self._page.is_editor:
            self._cursors.draw(self._surface, self._cursor_x, self._cursor_y)

        # Indicate if the image is input or output.
        if self._page.is_output:
            pygame.draw.rect(self._surface, (0, 0, 0), pygame.Rect(self._scale, 31 * self._scale, cell_size, cell_size))
        else:
            pygame.draw.rect(self._surface, (0, 0, 0), pygame.Rect(0, 31 * self._scale, cell_size, cell_size))

        # Indicate if the image is train or test.
        if self._page.pair_type == ajm.PairType.TRAIN:
            pygame.draw.rect(self._surface, (0, 0, 0), pygame.Rect(self._scale * 2, 31 * self._scale, cell_size, cell_size))
        else:
            pygame.draw.rect(self._surface, (0, 0, 0), pygame.Rect(self._scale * 3, 31 * self._scale, cell_size, cell_size))

        pygame.event.pump()
        pygame.display.update()
        return None

    def close(self) -> None:
        if self._surface is not None:
            pygame.display.quit()
            pygame.quit()

    def keys_to_action(cls) -> Dict[int, int]:
        return Actions.keys_to_action()
