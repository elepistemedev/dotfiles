#!/usr/bin/env sh

sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo

sudo dnf install https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm

sudo dnf install -y \
    util-linux-user \
    anacron \
    cargo \
    cmus \
    clementine \
    gnome-tweaks \
    gnome-extensions-app \
    neovim \
    python3-neovim \
    git \
    kitty \
    zsh \
    g++ \
    lua-devel \
    luarocks \
    php \
    php-bcmath \
    php-mysqlnd \
    php-pecl-zip \
    php-pgsql \
    php-posix \
    php-soap \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-compose-plugin \
    bat \
    fzf \
    httpie \
    ripgrep \
    tmux \
    ruby \
    python3 \
    htop \
    proselint \
    lm_sensors \
    discord \
    alacritty

flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install flathub org.telegram.desktop
flatpak install flathub com.slack.Slack
sudo gem install lolcat

pip install gitlint

sudo luarocks install luacheck

cargo install stylua

# Composer
sh ~/.dotfiles/scripts/install-composer.sh
composer global require laravel/installer

# Node
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
# nvm install node 

sudo dnf groupinstall "Development Tools" "Development Libraries"

# Docker machine
curl -L https://github.com/docker/machine/releases/download/v0.16.2/docker-machine-`uname -s`-`uname -m` >/tmp/docker-machine &&
    chmod +x /tmp/docker-machine &&
    sudo cp /tmp/docker-machine /usr/local/bin/docker-machine

# Docker setup
sudo groupadd docker
sudo usermod -aG docker $USER
sudo systemctl enable docker.service
sudo systemctl enable containerd.service
sudo systemctl start docker

echo "Don't forget to copy over your .ssh and .gnupg directories!"


