import libtmux
import argparse

# Take the input as arguments to the script
def main():
    parser = argparse.ArgumentParser(description='Broadcast a string to tmux panes with variable substitution.')
    parser.add_argument('-w','--window-name', type=str, help='Name of the tmux window')
    parser.add_argument('-s', '--starting-value', type=int, help='Starting value for N that increments for each pane')
    parser.add_argument('-r', '--fixed-repeat', type=int, help='Repeat the string (without incrementing N) for this number of panes, then increment N')
    parser.add_argument('-p', '--number-of-panes', type=int, help='Increment the starting value up to this number of panes')
    parser.add_argument('string_to_send', type=str, help='String to send to the panes')

    args = parser.parse_args()

    window_name = args.window_name
    string_to_send = args.string_to_send
    starting_value = args.starting_value
    npanes = args.number_of_panes
    fixed_repeat = args.fixed_repeat

    server = libtmux.Server()
    for session in server.attached_sessions:
        for window in session.windows:
            if window.name != window_name:
                continue
            # turn off synchronization
            sync = window.show_window_option('synchronize-panes')
            if sync == 'on':
                window.set_window_option('synchronize-panes', 'off')
            counter = starting_value
            i = 1
            for pane in window.panes:
                # find and replace N with the counter value
                output = string_to_send.replace('N', str(counter))
                pane.send_keys(output, enter=False)
                counter += 1 if not fixed_repeat else 0
                if i == npanes:
                    if fixed_repeat:
                        counter += 1
                    else:
                        counter = starting_value
                    i = 0
                else:
                    i += 1
            # restore synchronization
            if sync == 'on':
                window.set_window_option('synchronize-panes', 'on')
            break

if __name__ == '__main__':
    main()
