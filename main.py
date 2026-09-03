import argparse
import re
import sys

import libtmux
from libtmux import exc
from libtmux.constants import PaneDirection

# The layouts new-window.sh used to build, as (rows, columns).
PRESETS = {
    4: (2, 2),
    8: (2, 4),
    16: (2, 8),
    32: (4, 8),
}

SUBCOMMANDS = ['send', 'broadcast', 'new-window'] + [f'new-window{n}' for n in PRESETS]


def main():
    parser = argparse.ArgumentParser(description='tmux pane automation.')
    sub = parser.add_subparsers(dest='command', required=True)

    send = sub.add_parser('send', aliases=['broadcast'],
                          help='Broadcast a string to tmux panes with variable substitution.')
    send.add_argument('-t', '--target', type=str, help='Name of the tmux window')
    send.add_argument('-s', '--start', type=int, help='Starting value for N that increments for each pane')
    send.add_argument('-g', '--group', type=int, help='Repeat the string (without incrementing N) for this number of panes, then increment N')
    send.add_argument('-c', '--cycle', type=int, help='Increment the starting value up to this number of panes')
    send.add_argument('string_to_send', type=str, help='String to send to the panes. Use {N} as a placeholder for variable substitution.')

    grid = sub.add_parser('new-window', aliases=[f'new-window{n}' for n in PRESETS],
                          help='Create a new window tiled into a grid of panes.')
    grid.add_argument('panes', type=int, nargs='?', help=f'Total panes. Presets: {sorted(PRESETS)}')
    grid.add_argument('-r', '--rows', type=int, help='Number of rows')
    grid.add_argument('-c', '--cols', type=int, help='Number of panes per row')
    grid.add_argument('-n', '--name', type=str, help='Name for the new window')

    args = parser.parse_args(rewrite_argv())

    if args.command.startswith('new-window'):
        rows, cols = resolve_grid(args, parser)
        window = new_window(rows, cols, args.name)
        print(f'{window.name}: {rows}x{cols}')
    else:
        broadcast(args)


def rewrite_argv(argv=None):
    """Keep the old bare `tmux-man -t win "cmd"` form working."""
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] not in SUBCOMMANDS and argv[0] not in ('-h', '--help'):
        argv.insert(0, 'send')
    return argv


def resolve_grid(args, parser):
    count = args.panes
    suffix = re.fullmatch(r'new-window(\d*)', args.command).group(1)
    if suffix:
        count = int(suffix)

    if args.rows and args.cols:
        return args.rows, args.cols
    if count in PRESETS:
        return PRESETS[count]
    if count is None:
        parser.error(f'pass a pane count {sorted(PRESETS)}, or --rows and --cols')
    parser.error(f'no preset for {count} panes; pass --rows and --cols')


def new_window(rows, cols, name=None):
    server = libtmux.Server()
    sessions = server.attached_sessions
    if not sessions:
        raise SystemExit('no attached tmux session')
    return tile(sessions[0], rows, cols, name)


def tile(session, rows, cols, name=None):
    window = session.new_window(window_name=name, attach=True)
    try:
        for row in split_even(window.panes[0], rows, PaneDirection.Below):
            split_even(row, cols, PaneDirection.Right)
    except exc.LibTmuxException:
        # A half-tiled window is worse than none.
        window.kill()
        raise SystemExit(f'terminal too small for a {rows}x{cols} grid')
    for pane in window.panes:
        redraw(pane)
    window.panes[0].select()
    return window


def redraw(pane):
    """Wipe the prompt a resize left rewrapped, and the history behind it."""
    pane.cmd('send-keys', '-R', 'C-l')
    pane.cmd('clear-history')


def split_even(pane, count, direction):
    """Cut a pane into count equal panes, left to right or top to bottom."""
    if count < 2:
        return [pane]
    horizontal = direction in (PaneDirection.Right, PaneDirection.Left)
    total = int(pane.pane_width if horizontal else pane.pane_height)
    sizes = even_sizes(total, count)

    # Split off the tail panes at their final size, last one first. Each lands
    # right after `pane`, so only `pane` is ever resized. A shell that starts at
    # its final size never rewraps its prompt.
    panes = [pane]
    for size in reversed(sizes[1:]):
        panes.insert(1, pane.split(direction=direction, size=size, attach=False))
    return panes


def even_sizes(total, count):
    """Share total cells between count panes. Each divider eats one cell."""
    base, extra = divmod(total - (count - 1), count)
    return [base + (i < extra) for i in range(count)]


def broadcast(args):
    target_window = args.target
    string_to_send = args.string_to_send
    start_value = args.start
    cycle_at = args.cycle
    group_size = args.group

    server = libtmux.Server()
    for session in server.attached_sessions:
        for window in session.windows:
            if window.name != target_window:
                continue
            # turn off synchronization
            sync = window.show_option('synchronize-panes')
            print(f"Current pane synchronization is: {sync}")
            if sync == True:
                window.set_option('synchronize-panes', 'off')
            counter = start_value
            if group_size:
                broadcast_with_grouping(window.panes, string_to_send, start_value, group_size)
            else:
                i = 1
                for pane in window.panes:
                    # find and replace N with the counter value
                    output = string_to_send.replace('{N}', str(counter))
                    pane.send_keys(output, enter=False)
                    counter += 1
                    if i == cycle_at:
                        counter = start_value
                        i = 1
                    else:
                        i += 1
            # restore synchronization
            if sync == True:
                window.set_option('synchronize-panes', 'on')
            break


def broadcast_with_grouping(panes, string_to_send, start_value, group_size):
    i = 0
    counter = start_value
    for pane in panes:
        output = string_to_send.replace('{N}', str(counter))
        pane.send_keys(output, enter=False)
        i += 1
        if i == group_size:
            counter += 1
            i = 0


if __name__ == '__main__':
    main()
