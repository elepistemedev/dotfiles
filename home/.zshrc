#  █▀ █▀▀ █▄░█ ▀█▀ █░█  ┎┤  Ingeniería de Datos & Data Science  ├┒
#  ▄█ ██▄ █░▀█ ░█░ █▄█  ┖┤              en Python               ├┚
#              .studio en

# ▀█ █▀ █░█ █▀█ █▀▀   █▀▀ █▀█ █▄░█ █▀▀ █ █▀▀  - @elepistemedev
# █▄ ▄█ █▀█ █▀▄ █▄▄   █▄▄ █▄█ █░▀█ █▀░ █ █▄█  - https://github.com/elepistemedev/dotfiles

# Starship
export STARSHIP_CONFIG="$HOME/.config/starship/starship.toml"

# █▀█ █░░ █░█ █▀▀ █ █▄░█ █▀
# █▀▀ █▄▄ █▄█ █▄█ █ █░▀█ ▄█

[ -f "${XDG_DATA_HOME:-$HOME/.local/share}/zap/zap.zsh" ] && source "${XDG_DATA_HOME:-$HOME/.local/share}/zap/zap.zsh"
plug "zsh-users/zsh-autosuggestions"
plug "zap-zsh/supercharge"
plug "zap-zsh/zap-prompt"
plug "zsh-users/zsh-syntax-highlighting"
plug "wintermi/zsh-starship"
plug "conda-incubator/conda-zsh-completion"

# Load and initialise completion system
autoload -Uz compinit
compinit

# █░█ █ █▀ ▀█▀ █▀█ █▀█ █▄█
# █▀█ █ ▄█ ░█░ █▄█ █▀▄ ░█░

HISTFILE=~/.config/zsh/zhistory
HISTSIZE=50000
SAVEHIST=50000

# ▄▀█ █░░ █ ▄▀█ █▀
# █▀█ █▄▄ █ █▀█ ▄█

# alias mirrors="sudo reflector --verbose --latest 5 --country 'United States' --age 6 --sort rate --save /etc/pacman.d/mirrorlist"

alias grub-update="sudo grub-mkconfig -o /boot/grub/grub.cfg"
# alias mantenimiento="yay -Sc && sudo pacman -Scc"
# alias purga="sudo pacman -Rns $(pacman -Qtdq) ; sudo fstrim -av"
# alias update="paru -Syu --nocombinedupgrade"

alias vm-on="sudo systemctl start libvirtd.service"
alias vm-off="sudo systemctl stop libvirtd.service"

alias musica="ncmpcpp"

alias ls='lsd -a --group-directories-first'
alias ll='lsd -la --group-directories-first'

alias clear='~/.config/sentu/logo.sh'

# alias sentu-data='cookiecutter https://github.com/SENTUstudio/cookiecutter-ciencia-datos --checkout main'

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

