# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

tmux-man is a tmux automation toolkit. Everything is driven from one command,
`tmux-man`, with two subcommands:
1. **`send`** - broadcasts commands to tmux panes with variable substitution
2. **`new-window`** - creates a window tiled into a grid of panes

`new-window.sh` holds the original bash implementation of the tiling. It is kept
for reference; `new-window` supersedes it.

## Running the Project

This project uses `uv` for dependency management. First, install the package in editable mode:

```bash
uv pip install -e .
```

Then run the command with:

```bash
uv run tmux-man <subcommand> [options]
```

## Architecture

All code lives in `main.py`.

### Tiling (`new-window`)
- `split_even()` cuts a pane into N equal panes, recursively. It reads the
  pane's current width/height and passes an absolute size to `split-window -l`,
  accounting for the one cell each divider eats.
- `tile()` splits the window into rows, then splits each row into columns.
- Splits target Pane objects (stable `%id`), so no `select-pane` bookkeeping is
  needed - unlike the bash version, which juggles pane indexes by hand.
- Resulting panes are indexed left to right, top to bottom, matching the order
  `send` walks them in.

### Broadcasting (`send`)
- Uses `libtmux` Python library for tmux interaction
- Operates on currently attached tmux sessions only
- Temporarily disables pane synchronization during broadcast, then restores original state
- Supports two broadcasting modes:
  - **Incremental mode** (default): Substitutes `{N}` with incrementing counter for each pane
  - **Group mode** (`-g`): Sends same `{N}` value to a group of panes before incrementing

### CLI Arguments

`new-window` (aliases `new-window4`, `new-window8`, `new-window16`, `new-window32`
select the matching preset):
- `panes`: Total panes; must be a preset (4, 8, 16, 32)
- `-r/--rows`: Number of rows
- `-c/--cols`: Number of panes per row
- `-n/--name`: Name for the new window

`send` (alias `broadcast`; the subcommand may be omitted for backwards
compatibility with the old bare form):
- `-t/--target`: Name of the tmux window to target
- `-s/--start`: Starting value for `{N}` counter
- `-c/--cycle`: Reset counter to starting value after this many panes
- `-g/--group`: Send same `{N}` value to this many panes before incrementing
- `string_to_send`: String to broadcast (use `{N}` as placeholder for variable substitution)

### new-window.sh (superseded)
Bash functions for the same grid layouts: `new-window4()` (2x2),
`new-window8()` (2x4), `new-window16()` (2x8), `new-window32()` (4x8). Each uses
tmux's `split-window` and `select-pane` commands to construct the layout.

## Key Functionality

### Tiling
```bash
uv run tmux-man new-window32 -n ensemble
uv run tmux-man new-window --rows 3 --cols 5
```

### Broadcasting with Variable Substitution
The script replaces `{N}` in the input string with numeric values. Examples:

**Incremental mode with cycling:**
```bash
uv run tmux-man send -t mywindow -s 1 -c 4 "ssh ncm-{N}.rsd"
```
Sends `ssh ncm-1.rsd`, `ssh ncm-2.rsd`, `ssh ncm-3.rsd`, `ssh ncm-4.rsd`, then wraps back to `ssh ncm-1.rsd`

**Group mode:**
```bash
uv run tmux-man send -t mywindow -s 1 -g 8 "ssh J{N}"
```
Sends `ssh J1` to first 8 panes, `ssh J2` to next 8 panes, etc.

## Dependencies

- Python 3.12+
- `uv` package manager
- `libtmux` library (managed by uv)
- tmux (system dependency)
