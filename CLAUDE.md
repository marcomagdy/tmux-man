# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

tmux-man is a tmux automation toolkit with two main utilities:
1. **tmux-broadcast.py** - Python script for broadcasting commands to tmux panes with variable substitution
2. **new-window.sh** - Shell functions for creating tmux windows with predefined pane layouts

## Architecture

### tmux-broadcast.py
- Uses `libtmux` Python library for tmux interaction
- Uses `argparse` for command-line argument parsing
- Operates on the currently attached tmux session
- Temporarily disables pane synchronization during broadcast, then restores it
- Supports two broadcasting modes:
  - **Incremental mode**: Substitutes 'N' with incrementing counter for each pane
  - **Fixed repetition mode** (`-r`): Sends same value to multiple panes before incrementing

### new-window.sh
- Provides three bash functions: `new-window4()`, `new-window8()`, `new-window16()`
- Each creates a tmux window with a specific grid layout (4, 8, or 16 panes)
- Uses tmux's `split-window` and `select-pane` commands to construct layouts

## Key Functionality

### Broadcasting with Variable Substitution
The broadcast script replaces 'N' in the input string with numeric values:
- `-s/--starting-value`: Initial value for N
- `-p/--number-of-panes`: After this many panes, reset counter to starting value
- `-r/--fixed-repeat`: Send same N value to this many panes before incrementing
- `-w/--window-name`: Target window by name

Example: `python tmux-broadcast.py -w mywindow -s 0 -p 4 "export PORT=300N"`
- Sends `export PORT=3000` to pane 1, `export PORT=3001` to pane 2, etc.
- After 4 panes, resets to starting value 0

## Dependencies

- Python 3 with `libtmux` library
- tmux (for both scripts)
