# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

tmux-man is a tmux automation toolkit with two main utilities:
1. **main.py** - Python script for broadcasting commands to tmux panes with variable substitution
2. **new-window.sh** - Shell functions for creating tmux windows with predefined pane layouts

## Running the Project

This project uses `uv` for dependency management. First, install the package in editable mode:

```bash
uv pip install -e .
```

Then run the command with:

```bash
uv run tmux-man [options] <string_to_send>
```

## Architecture

### main.py (Broadcast Script)
- Uses `libtmux` Python library for tmux interaction
- Uses `argparse` for command-line argument parsing
- Operates on currently attached tmux sessions only
- Temporarily disables pane synchronization during broadcast, then restores original state
- Supports two broadcasting modes:
  - **Incremental mode** (default): Substitutes 'N' with incrementing counter for each pane
  - **Group mode** (`-g`): Sends same N value to a group of panes before incrementing

### CLI Arguments
- `-t/--target`: Name of the tmux window to target
- `-s/--start`: Starting value for N counter
- `-c/--cycle`: Reset counter to starting value after this many panes
- `-g/--group`: Send same N value to this many panes before incrementing
- `string_to_send`: String to broadcast (use 'N' as placeholder for variable substitution)

### new-window.sh
Provides bash functions for creating tmux windows with predefined grid layouts:
- `new-window4()`: Creates 2x2 grid (4 panes)
- `new-window8()`: Creates 2x4 grid (8 panes)
- `new-window16()`: Creates 2x8 grid (16 panes)
- `new-window32()`: Creates 4x8 grid (32 panes)

Each uses tmux's `split-window` and `select-pane` commands to construct the layout.

## Key Functionality

### Broadcasting with Variable Substitution
The script replaces 'N' in the input string with numeric values. Examples:

**Incremental mode with cycling:**
```bash
uv run tmux-man -t mywindow -s 1 -c 4 "ssh ncm-N.rsd"
```
Sends `ssh ncm-1.rsd`, `ssh ncm-2.rsd`, `ssh ncm-3.rsd`, `ssh ncm-4.rsd`, then wraps back to `ssh ncm-1.rsd`

**Group mode:**
```bash
uv run tmux-man -t mywindow -s 1 -g 8 "ssh JN"
```
Sends `ssh J1` to first 8 panes, `ssh J2` to next 8 panes, etc.

## Dependencies

- Python 3.12+
- `uv` package manager
- `libtmux` library (managed by uv)
- tmux (system dependency)
