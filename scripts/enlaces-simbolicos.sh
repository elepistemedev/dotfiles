#!/bin/bash

# Zsh
ln -sf ~/.dotfiles/zsh/zshrc $HOME/.zshrc

# Alacritty
rm -rf $HOME/.config/alacritty
ln -sf ~/.dotfiles/alacritty $HOME/.config/alacritty

# Neovim
rm -rf $HOME/.config/nvim
ln -s ~/.dotfiles/nvim $HOME/.config/nvim

# Kitty
rm -rf $HOME/.config/kitty
ln -s ~/.dotfiles/kitty $HOME/.config/kitty

# Tmux
ln -sf ~/.dotfiles/tmux/tmux.conf $HOME/.tmux.conf

# Git
ln -sf ~/.dotfiles/git/gitconfig $HOME/.gitconfig
ln -sf ~/.dotfiles/git/gitignore_global $HOME/.gitignore_global

# Phpactor
rm -rf $HOME/.config/phpactor
ln -s ~/.dotfiles/phpactor $HOME/.config/phpactor

# tmuxinator
rm -rf $HOME/.config/tmuxinator
ln -s ~/.dotfiles/tmuxinator $HOME/.config/tmuxinator

# Scripts
mkdir -p $HOME/.local/bin

ln -sf ~/.dotfiles/scripts/t $HOME/.local/bin/t
ln -sf ~/.dotfiles/scripts/deliver $HOME/.local/bin/deliver

# NVM (Node Version Manager)
mkdir -p $HOME/.nvm
ln -sf ~/.dotfiles/nvm/default-packages $HOME/.nvm/default-packages