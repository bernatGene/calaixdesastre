#!/bin/bash

# Function to check if tmux session exists
session_exists() {
    tmux has-session -t "$1" 2>/dev/null
}

# Parameters with defaults
session_name=$1
virtualenv_name=$2
path=${3:-$HOME}
total_panes=6

# Check if session exists
if session_exists "$session_name"; then
    echo "Session $session_name already exists. Attaching..."
else
    echo "Creating new session: $session_name"
    tmux new-session -d -s "$session_name" -c "$path"
    
    # Layout with 4 panes in the left and two main in the right
    tmux split-window -h -t "$session_name:0" -c "$path"
    tmux split-window -v -t "$session_name:0.1" -c "$path"
    tmux select-pane -t "$session_name:0.1" -T "server"
    tmux select-pane -t "$session_name:0.2" -T "git"

    tmux split-window -v -t "$session_name:0.0" -c "$path"
    tmux split-window -v -t "$session_name:0.0" -c "$path"
    tmux split-window -v -t "$session_name:0.2" -c "$path"

    tmux select-pane -t "$session_name:0.0" -T "celery"
    tmux select-pane -t "$session_name:0.1" -T "uberwatch"
    tmux select-pane -t "$session_name:0.2" -T "misc1"
    tmux select-pane -t "$session_name:0.3" -T "misc2"

    # Set up each pane with virtualenv 
    for ((i = 0; i < total_panes; i++)); do
        tmux send-keys -t "$session_name:0.$i" "workon $virtualenv_name" C-m
    done

    tmux send-keys -t "$session_name:0.0" "./celerydev.sh" C-m
    tmux send-keys -t "$session_name:0.1" "uberwatch 1 'git fetch'" C-m

    # SSH agent on last pane
    tmux send-keys -t "$session_name:0.$(total_panes - 1)" "eval \$(ssh-agent) && ssh-add" C-m
fi

# Attach to the session
tmux attach-session -t "$session_name"


