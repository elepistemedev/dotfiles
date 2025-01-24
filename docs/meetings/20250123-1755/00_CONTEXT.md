# Contexto del Proyecto github-project-manager

## Descripción General
Un paquete de Python para post-instalación de paquetes multiplataforma y administración de dotfiles personalizados.

## Estado Actual
- **Milestone:** 1 - Core Infraestructure
- **Issue Actual:** #1 - Setup initial project structure and Dependencias
- **Estado:** proyecto inicializado
- **Último Paso Completado:** 
SystemDetector Class Requirements

Must support detection of at least Windows, Linux, and macOS
Provide consistent interface for system information retrieval
Return structured/typed results for each detection method

Detection Method Specifications

OS Detection:
Accurately identify OS type (Windows/Linux/macOS)
Retrieve detailed distribution name (e.g., Ubuntu, CentOS)
Return OS version with semantic versioning support
Package Manager Detection:
Identify default package manager for each supported OS
Return package manager name and version
Handle scenarios with multiple package managers

Testing Requirements

100% code coverage for detection methods
Test cases for each supported operating system
Validate detection accuracy against known system configurations
Include edge cases and systems with minimal metadata

Performance and Reliability

Minimal system resource consumption
Fast detection methods (< 100ms execution time)
Graceful handling of detection failures
Thread-safe implementation

## Estructura del Proyecto
```
dotfiles/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   └── workflows/ci.yml
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── system_detector.py
│   │   ├── package_manager.py
│   │   └── config_manager.py
│   ├── installers/
│   │   ├── __init__.py
│   │   ├── base_installer.py
│   │   ├── phase1/
│   │   └── phase2/
│   └── utils/
│       ├── __init__.py
│       ├── logger.py
│       └── progress.py
├── tests/
│   ├── __init__.py
│   ├── test_system_detector.py
│   └── test_installers/
├── config/
│   ├── default_config.yaml
│   └── dependencies/
├── docs/
│   ├── installation.md
│   ├── development.md
│   └── meetings/
│       └── 20250122-0959/
│           ├── CONTEXT.md        # Estado actual y contexto
│           ├── SESSIONS.md       # Registro de sesiones
│           ├── PROGRESS.md       # Progreso general
│           └── DECISIONS.md      # Decisiones de diseño
├── logs/                    # Directorio para logs
│   └── .gitkeep            # Mantiene el directorio en git
├── scripts/
├── .gitignore
├── .pre-commit-config.yaml 
├── ruff.toml
├── pyproject.toml
├── README.md
└── requirements/
    ├── requirements.txt
    └── requirements-dev.txt
```

## Código Relevante Actual
[Espacio para añadir fragmentos de código relevantes para la sesión actual]

## Decisiones Clave Tomadas
1. Uso de la libreria click para la interfaz CLI
2. Estructura modular del proyecto
3. Patrones de diseño:
  - Factory Pattern para los instaladores
  - Strategy Pattern para diferentes sistemas operativos
  - Singleton para el logger y config manager
  - Observer para el sistema de progreso
4. Gestion de dependencias:
  - pyproject.toml para la configuración moderna de python
  - Gestión de versiones con uv
  - Requerimientos en la carpeta requirements/: 
    - requirements.txt
    - requirements-dev.txt
5. Code Style
  - Seguir PEP 8
  - Usar typing para anotaciones de tipo
  - Documentar usando docstrings (Google style)
  - Máximo 120 caracteres por línea
  - Usar nombres descriptivos en inglés
6. Testing
  - Pytest para testing
  - Coverage mínimo: 80%
  - Tests unitarios y de integración requeridos
7. Git Workflow
  - Feature branches desde `develop`
  - Conventional Commits
  - Rebase interactivo antes de PR
  - Squash commits en el merge
8. CI/CD Pipeline
  - GitHub Actions para:
    - Lint checking
    - Test execution
    - Build verification
    - Documentation generation

## Dependencias Principales
- "python-dotenv", "click", "rich", "InquirerPy", "typer", "tqdm", "gitlint", "textual", "uv", "pytest"

## Próximos Pasos:
1. Documentation

- Clear method signatures with type hints
- Comprehensive inline documentation
- Example usage Mkdocs
## Problemas Actuales / Blockers
[Espacio para documentar problemas actuales]

## Notas Importantes
Todo comentario debe contemplar el estilo docstring tipo google angular en idioma español
