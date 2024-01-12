# Simon ARC Env

<p align="center">
    <img src="https://raw.githubusercontent.com/neoneye/simon-arc-env/main/simon-arc-env.gif"
        alt="simon arc env"/>
</p>

<table>
    <tbody>
        <tr>
            <td>Action Space</td>
            <td>Discrete(10)</td>
        </tr>
        <tr>
            <td>Observation Shape</td>
            <td>(32, 32)</td>
        </tr>
        <tr>
            <td>Observation High</td>
            <td>255</td>
        </tr>
        <tr>
            <td>Observation Low</td>
            <td>0</td>
        </tr>
        <tr>
            <td>Import</td>
            <td>import simon_arc_env<br/>gymnasium.make("SimonARC-v0")</td>
        </tr>
    </tbody>
</table>

## Description

[Abstraction and Reasoning Corpus](https://github.com/fchollet/ARC) as a [Farama Gymnasium](https://github.com/Farama-Foundation/Gymnasium) environment.

Related project: [ARCLE - ARC Learning Environment](https://github.com/ConfeitoHS/arcle).

### Installation

```bash
pip install simon-arc-env
```

### Usage

1. Play it by running

```bash
python examples/play.py
```

Press `space` to draw a pixel.

2. Import it to train your RL model

```python
import simon_arc_env
env = gymnasium.make("SimonARC-v0")
```

The package relies on ```import``` side-effects to register the environment
name so, even though the package is never explicitly used, its import is
necessary to access the environment.

## Action Space

`SimonARC` has the action space `Discrete(10)`.

| Value | Key         | Meaning               |
|-------|-------------|-----------------------|
| 0     | TAB         | Next page             |
| 1     | Return      | Submit drawing        |
| 2     | Space       | Set pixel             |
| 3     | Arrow up    | Move `cursor_y` up    |
| 4     | Arrow down  | Move `cursor_y` down  |
| 5     | Arrow left  | Move `cursor_x` left  |
| 6     | Arrow right | Move `cursor_x` right |
| 7     | m           | Increment color       |
| 8     | n           | Decrement color       |
| 9     | s           | Adjust canvas size    |
| N/A   | Escape      | Exit game             |
| N/A   | i           | Print info to console |

## Observation Space

Observation space `Box(low=0, high=255, shape=(32, 32), dtype=np.uint8)`.

### Rewards

If you solve the task you get `10000` in reward.

If you predict the `width` correct you get `100` in reward.

If you predict the `height` correct you get `100` in reward.

If your prediction have the correct histogram you get `100` in reward.

## Run tests

```bash
make test
```

## Version History

- v0: initial version release
