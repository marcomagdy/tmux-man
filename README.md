To send a string like `ssh ncm-1.rsd`, `ssh ncm-2.rsd`, etc. up to 4 in all panes and wrap around:

```bash
uv run main.py -t <tmux window name> -s 1 "ssh ncm-N.rsd"
```

To send a fixed string to a group of 8 panes and then increment the number:

```bash
uv run main.py -t <tmux window name> -s 1 "ssh JN" -g 8
```
This will send the string "ssh J1" to the first 8 panes, then "ssh J2" to the next 8 panes, and so on.
