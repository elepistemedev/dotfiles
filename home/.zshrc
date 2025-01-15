#  █▀ █▀▀ █▄░█ ▀█▀ █░█  ┎┤  Ingeniería de Datos & Data Science  ├┒
#  ▄█ ██▄ █░▀█ ░█░ █▄█  ┖┤              en Python               ├┚
#              .studio en

# ▀█ █▀ █░█ █▀█ █▀▀   █▀▀ █▀█ █▄░█ █▀▀ █ █▀▀  - @elepistemedev
# █▄ ▄█ █▀█ █▀▄ █▄▄   █▄▄ █▄█ █░▀█ █▀░ █ █▄█  - https://github.com/elepistemedev/dotfiles


if [[ -f "/opt/homebrew/bin/brew" ]] then
  # If you're using macOS, you'll want this enabled
  eval "$(/opt/homebrew/bin/brew shellenv)"
fi
# Path
# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/bin" ] ; then
    PATH="$HOME/bin:$PATH"
fi

# Set the directory we want to store zinit and plugins
ZINIT_HOME="${XDG_DATA_HOME:-${HOME}/.local/share}/zinit/zinit.git"

# Download Zinit, if it's not there yet
if [ ! -d "$ZINIT_HOME" ]; then
   mkdir -p "$(dirname $ZINIT_HOME)"
   git clone https://github.com/zdharma-continuum/zinit.git "$ZINIT_HOME"
fi

# Source/Load zinit
source "${ZINIT_HOME}/zinit.zsh"

# █▀█ █░░ █░█ █▀▀ █ █▄░█ █▀
# █▀▀ █▄▄ █▄█ █▄█ █ █░▀█ ▄█

# Add in zsh plugins
zinit light zsh-users/zsh-syntax-highlighting
zinit light zsh-users/zsh-completions
zinit light zsh-users/zsh-autosuggestions
zinit light Aloxaf/fzf-tab

# Add in snippets
zinit snippet OMZL::git.zsh
zinit snippet OMZP::git
zinit snippet OMZP::sudo
zinit snippet OMZP::archlinux
zinit snippet OMZP::aws
zinit snippet OMZP::kubectl
zinit snippet OMZP::kubectx
zinit snippet OMZP::command-not-found

# Load completions
autoload -Uz compinit && compinit

zinit cdreplay -q

# Prompt
eval "$(oh-my-posh init zsh --config $HOME/.config/ohmyposh/negligible.omp.json)"

# Keybindings
bindkey -e
bindkey '^p' history-search-backward
bindkey '^n' history-search-forward
bindkey '^[w' kill-region

# █░█ █ █▀ ▀█▀ █▀█ █▀█ █▄█
# █▀█ █ ▄█ ░█░ █▄█ █▀▄ ░█░

# History
HISTSIZE=5000
HISTFILE=~/.zsh_history
SAVEHIST=$HISTSIZE
HISTDUP=erase
setopt appendhistory
setopt sharehistory
setopt hist_ignore_space
setopt hist_ignore_all_dups
setopt hist_save_no_dups
setopt hist_ignore_dups
setopt hist_find_no_dups

# Completion styling
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Za-z}'
zstyle ':completion:*' list-colors "${(s.:.)LS_COLORS}"
zstyle ':completion:*' menu no
zstyle ':fzf-tab:complete:cd:*' fzf-preview 'ls --color $realpath'
zstyle ':fzf-tab:complete:__zoxide_z:*' fzf-preview 'ls --color $realpath'

# ▄▀█ █░░ █ ▄▀█ █▀
# █▀█ █▄▄ █ █▀█ ▄█

# Aliases
alias ls='ls --color'
alias vim='nvim'
alias c='clear'
alias ls='lsd -a --group-directories-first'
alias ll='lsd -la --group-directories-first'

alias clear='~/.config/sentu/logo.sh'

# Shell integrations
eval "$(fzf --zsh)"
eval "$(zoxide init --cmd cd zsh)"

# ▄▀█ █░█ ▀█▀ █▀█   █▀ ▀█▀ ▄▀█ █▀█ ▀█▀
# █▀█ █▄█ ░█░ █▄█   ▄█ ░█░ █▀█ █▀▄ ░█░

~/.config/sentu/logo.sh
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/el/anaconda3/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/el/anaconda3/etc/profile.d/conda.sh" ]; then
        . "/home/el/anaconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/el/anaconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<


