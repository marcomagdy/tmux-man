# tmux-man

A tmux automation toolkit for broadcasting commands to multiple panes with variable substitution.

## Setup

First, install the package in editable mode:

```bash
uv pip install -e .
```

This creates the `tmux-man` command that you can use with `uv run`.

## Usage Examples

To send a string like `ssh ncm-1.rsd`, `ssh ncm-2.rsd`, etc. up to 4 in all panes and wrap around:

```bash
uv run tmux-man -t <tmux window name> -s 1 "ssh ncm-N.rsd"
```

To send a fixed string to a group of 8 panes and then increment the number:

```bash
uv run tmux-man -t <tmux window name> -s 1 "ssh JN" -g 8
```
This will send the string "ssh J1" to the first 8 panes, then "ssh J2" to the next 8 panes, and so on.

## Options

- `-t/--target`: Name of the tmux window to target
- `-s/--start`: Starting value for N counter
- `-c/--cycle`: Reset counter to starting value after this many panes
- `-g/--group`: Send same N value to this many panes before incrementing
- The string to send uses 'N' as a placeholder for variable substitution
