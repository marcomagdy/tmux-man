function new-window16() {
# Create a new tmux window split into 16-panes; 8 at the top and 8 at the bottom
    tmux new-window \; \
        split-window -v \; \
        split-window -h \; \
        split-window -h \; \
        split-window -h \; \
        select-pane -t 1\; \
        split-window -h \; \
        split-window -h \; \
        select-pane -t 1\; \
        split-window -h \; \
        select-pane -t 5\; \
        split-window -h \; \
        select-pane -t 0\; \
        split-window -h \; \
        split-window -h \; \
        split-window -h \; \
        select-pane -t 1\; \
        split-window -h \; \
        select-pane -t 0\; \
        split-window -h \; \
        split-window -h \; \
        select-pane -t 0\; \
        split-window -h \;
}

function new-window8() {
# Create a new tmux window split into 8-panes; 4 at the top and 4 at the bottom
    tmux new-window \; \
        split-window -v \; \
        split-window -h\; \
        split-window -h\; \
        select-pane -t 1\; \
            split-window -h\;\
            select-pane -t 0\;\
                split-window -h\;\
                split-window -h\;\
                select-pane -t 0 \;\
                    split-window -h\;\
                    select-pane -t 0\;
}

function new-window4() {
# Create a new tmux window split into 8-panes; 4 at the top and 4 at the bottom
    tmux new-window \; \
        split-window -v \; \
        split-window -h\; \
        select-pane -t 0\; \
            split-window -h\;
}

