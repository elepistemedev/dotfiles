#  █▀ █▀▀ █▄░█ ▀█▀ █░█  ┎┤  Ingeniería de Datos & Data Science  ├┒
#  ▄█ ██▄ █░▀█ ░█░ █▄█  ┖┤              en Python               ├┚
#              .studio en

# ▀█ █▀ █░█ █▀█ █▀▀   █▀▀ █▀█ █▄░█ █▀▀ █ █▀▀  - @elepistemedev
# █▄ ▄█ █▀█ █▀▄ █▄▄   █▄▄ █▄█ █░▀█ █▀░ █ █▄█  - https://github.com/elepistemedev/dotfiles

# █▀█ █░░ █░█ █▀▀ █ █▄░█ █▀
# █▀▀ █▄▄ █▄█ █▄█ █ █░▀█ ▄█

[ -f "${XDG_DATA_HOME:-$HOME/.local/share}/zap/zap.zsh" ] && source "${XDG_DATA_HOME:-$HOME/.local/share}/zap/zap.zsh"
plug "zsh-users/zsh-autosuggestions"
plug "zap-zsh/supercharge"
plug "zap-zsh/zap-prompt"
plug "zsh-users/zsh-syntax-highlighting"
plug "wintermi/zsh-starship"

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

alias mirrors="sudo reflector --verbose --latest 5 --country 'United States' --age 6 --sort rate --save /etc/pacman.d/mirrorlist"

alias grub-update="sudo grub-mkconfig -o /boot/grub/grub.cfg"
# alias mantenimiento="yay -Sc && sudo pacman -Scc"
# alias purga="sudo pacman -Rns $(pacman -Qtdq) ; sudo fstrim -av"
# alias update="paru -Syu --nocombinedupgrade"

alias vm-on="sudo systemctl start libvirtd.service"
alias vm-off="sudo systemctl stop libvirtd.service"

alias musica="ncmpcpp"

alias ls='lsd -a --group-directories-first'
alias ll='lsd -la --group-directories-first'

alias clear='~/./.local/share/asciiart/SENTU'

# alias sentu-data='cookiecutter https://github.com/SENTUstudio/cookiecutter-ciencia-datos --checkout main'

# ▄▀█ █░█ ▀█▀ █▀█   █▀ ▀█▀ ▄▀█ █▀█ ▀█▀
# █▀█ █▄█ ░█░ █▄█   ▄█ ░█░ █▀█ █▀▄ ░█░