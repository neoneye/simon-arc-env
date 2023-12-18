# Idea: Available actions

Show a bit mask of the available actions in the right side of the 32x32 image.
- The editor page has several actions enabled.
- The non-editor pages has few actions enabled.
This way the RL knows what actions are available here. This prevents taking bad actions.

The 32x32 image is contained in an observation. The observation show what actions that can be taken in the next step.

This can be done by using the right-most column of the 32x32 grid, to show a 10 pixel tall column.
These pixels correspond to the available actions.
- Pixel 0 corresponds to action 0.
- Pixel 1 corresponds to action 1.
- Pixel `A` corresponds to action `A`.

Value of the pixel:
- If the pixel is turned off, `value=0`, then the action cannot be taken.
- If the pixel is turned on, `value=255`, then the action can be taken.
- If the pixel is neither on or off, `value=127`, then the action may be taken.
