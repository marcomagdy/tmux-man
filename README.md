# tmux-man

A tmux automation toolkit: tile a window into a grid of panes, then broadcast
commands to those panes with variable substitution.

## Setup

First, install the package in editable mode:

```bash
uv pip install -e .
```

This creates the `tmux-man` command that you can use with `uv run`.

## Creating a tiled window

```bash
uv run tmux-man new-window8
uv run tmux-man new-window32 -n ensemble
uv run tmux-man new-window --rows 3 --cols 5 -n custom
```

Presets: `new-window4` (2x2), `new-window8` (2x4), `new-window16` (2x8),
`new-window32` (4x8). Panes are numbered left to right, top to bottom, which is
the order `send` walks them in.

This replaces the bash functions in `new-window.sh`.

### Options

- `-r/--rows`: Number of rows
- `-c/--cols`: Number of panes per row
- `-n/--name`: Name for the new window

## Broadcasting to panes

To send a string like `ssh ncm-1.rsd`, `ssh ncm-2.rsd`, etc. up to 4 in all panes and wrap around:

```bash
uv run tmux-man send -t <tmux window name> -s 1 -c 4 "ssh ncm-{N}.rsd"
```

To send a fixed string to a group of 8 panes and then increment the number:

```bash
uv run tmux-man send -t <tmux window name> -s 1 -g 8 "ssh J{N}"
```
This will send the string "ssh J1" to the first 8 panes, then "ssh J2" to the next 8 panes, and so on.

The `send` keyword is optional; the old form without it still works.

### Options

- `-t/--target`: Name of the tmux window to target
- `-s/--start`: Starting value for the `{N}` counter
- `-c/--cycle`: Reset counter to starting value after this many panes
- `-g/--group`: Send same `{N}` value to this many panes before incrementing
- The string to send uses `{N}` as a placeholder for variable substitution
