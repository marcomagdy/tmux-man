import libtmux
import argparse

# Take the input as arguments to the script
def main():
    parser = argparse.ArgumentParser(description='Broadcast a string to tmux panes with variable substitution.')
    parser.add_argument('-t','--target', type=str, help='Name of the tmux window')
    parser.add_argument('-s', '--start', type=int, help='Starting value for N that increments for each pane')
    parser.add_argument('-g', '--group', type=int, help='Repeat the string (without incrementing N) for this number of panes, then increment N')
    parser.add_argument('-c', '--cycle', type=int, help='Increment the starting value up to this number of panes')
    parser.add_argument('string_to_send', type=str, help='String to send to the panes')

    args = parser.parse_args()

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
            sync = window.show_window_option('synchronize-panes')
            if sync == 'on':
                window.set_window_option('synchronize-panes', 'off')
            counter = start_value
            if group_size:
                broadcast_with_grouping(window.panes, string_to_send, start_value, group_size)
            else: 
                i = 1
                for pane in window.panes:
                    # find and replace N with the counter value
                    output = string_to_send.replace('N', str(counter))
                    pane.send_keys(output, enter=False)
                    counter += 1
                    if i == cycle_at:
                        counter = start_value
                        i = 1
                    else:
                        i += 1
            # restore synchronization
            if sync == 'on':
                window.set_window_option('synchronize-panes', 'on')
            break


def broadcast_with_grouping(panes, string_to_send, start_value, group_size):
    i = 0
    counter = start_value
    for pane in panes:
        output = string_to_send.replace('N', str(counter))
        pane.send_keys(output, enter=False)
        i += 1
        if i == group_size:
            counter += 1
            i = 0
    pass

if __name__ == '__main__':
    main()
