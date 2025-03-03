import libtmux
import sys

#Take the input as arguments to the script
def main():
    if len(sys.argv) != 5:
        print("Usage: %s <window-name> <string with N> <starting N value> <max repeat>" % sys.argv[0])
        sys.exit(1)

    window_name = sys.argv[1]
    string = sys.argv[2]
    starting_value = int(sys.argv[3])
    max_repeat = int(sys.argv[4])

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
                output = string.replace('N', str(counter))
                pane.send_keys(output, enter=False)
                counter += 1
                if i == max_repeat:
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
