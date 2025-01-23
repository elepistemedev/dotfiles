```
█▀ █▀▀ █▄░█ ▀█▀ █░█  ┎┤ DATA ENGINEER                                       ├┒
▄█ ██▄ █░▀█ ░█░ █▄█  ┖┤ Obteniendo datos para empresas, personas... para ti ├┚
                STUDIO
```

# dotfiles
Respaldo de mis archivos de configuración para linux. Optimizado para la distro de linux Fedora.

# 🚀 System Post-Installer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests](https://github.com/elepistemedev/dotfiles/actions/workflows/tests.yml/badge.svg)](https://github.com/elepistemedev/dotfiles/actions)
[![CI Status](https://github.com/elepistemedev/dotfiles/actions/workflows/ci.yml/badge.svg)](https://github.com/elepistemedev/dotfiles/actions)

A powerful and flexible post-installation system configurator and dotfiles manager. Automate your system setup across different Linux distributions with ease.

## ✨ Features

- 🔍 Automatic system detection and configuration
- 🔄 Seamless system updates and package installation
- 🐚 ZSH setup and configuration
- 🐍 Python environment setup with Anaconda
- 🚢 Docker environment configuration
- ⚡ Oh my posh prompt integration
- 🎨 Custom fonts installation
- 📁 Dotfiles management
- 📊 Progress tracking and reporting

## 🏗️ Current Status

MVP development focusing on Fedora Linux support. Additional distributions planned for future releases.

## 🔧 Installation

```bash
curl -s https://raw.githubusercontent.com/elepistemedev/dotfiles/refs/heads/dev/sentu_install.py | python3
```

### For development

```bash
# Clone the repository
git clone https://github.com/yourusername/system-post-installer.git
cd system-post-installer

# Install using Poetry (recommended)
poetry install

# Or using pip
pip install -r requirements.txt
```

## 🚀 Quick Start

```bash
# Run the installer
python -m system_post_installer --phase 1

# Or run specific components
python -m system_post_installer --components zsh,anaconda

# Install dotfiles only
python -m system_post_installer --dotfiles
```

## 📋 Requirements

- Python 3.10 or higher
- Git
- Internet connection
- sudo privileges

## 🗺️ Roadmap

### Phase 1 (Current)
- [ ] System detection
- [ ] Basic system updates
- [ ] ZSH installation
- [ ] Anaconda setup
- [ ] Python packages
- [ ] Starship prompt
- [ ] Font installation

### Phase 2 (Planned)
- [ ] Lua environment
- [ ] Docker setup
- [ ] Custom post-installations
- [ ] Dotfiles management

## 🤝 Contributing

We love your input! We want to make contributing as easy and transparent as possible. Please check our [Contributing Guidelines](CONTRIBUTING.md) for details on:

- Code of Conduct
- Development process
- Pull Request process
- Coding standards

## 🧪 Development

```bash
# Setup development environment
poetry install

# Run tests
poetry run pytest

# Run linting
poetry run pre-commit run --all-files
```

## 📝 Configuration

Configuration is handled through YAML files:

```yaml
# config/default_config.yaml
system:
  update: true
  packages:
    - git
    - curl
    - wget
zsh:
  theme: "robbyrussell"
  plugins:
    - git
    - python
```

## 📚 Documentation

Detailed documentation is available in the [docs](./docs) directory:
- [Installation Guide](docs/installation.md)
- [Configuration Guide](docs/configuration.md)
- [Development Guide](docs/development.md)

## 🐛 Bug Reports

Please use the [GitHub Issue Tracker](https://github.com/yourusername/system-post-installer/issues) to report bugs. Before creating a new issue, please search to ensure it hasn't already been reported.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Starship](https://starship.rs/) for the amazing prompt
- [Oh My Zsh](https://ohmyz.sh/) for ZSH configuration framework
- All our [contributors](https://github.com/yourusername/system-post-installer/graphs/contributors)

## 📞 Contact

- Create an issue for bug reports or feature requests
- Star the project if you find it useful
- Follow the repository for updates

---
Made with ❤️ by [elepistemedev/SENTUstudio]

