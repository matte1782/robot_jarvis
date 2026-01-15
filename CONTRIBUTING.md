# Contributing to Robot Projects Repository

Thank you for your interest in contributing to the OpenDuck Mini V3 quadruped robot project!

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Testing Requirements](#testing-requirements)
- [Documentation](#documentation)

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

## How Can I Contribute?

### Reporting Bugs

- **Use the issue tracker** - Check if the bug has already been reported
- **Use the bug report template** - Fill in all required sections
- **Provide details** - Include error messages, logs, hardware specs, and steps to reproduce
- **Be specific** - Include component versions (Raspberry Pi model, servo types, etc.)

### Suggesting Enhancements

- **Check existing issues** - Someone may have suggested it already
- **Explain the use case** - Why would this enhancement be useful?
- **Provide examples** - Show how it would work
- **Consider alternatives** - What other approaches did you consider?

### Code Contributions

We welcome contributions in these areas:
- **Firmware improvements** - Servo control, kinematics, sensor integration
- **Hardware validation** - Testing with different components
- **Documentation** - Tutorials, guides, troubleshooting
- **Testing** - Unit tests, integration tests, hardware tests
- **CAD models** - 3D printable parts improvements
- **Safety features** - Battery monitoring, emergency stops, thermal protection

## Development Setup

### Prerequisites

- Python 3.9+ (firmware development)
- Git for version control
- Raspberry Pi 4 Model B (4GB recommended) for hardware testing
- Optional: 3D printer for mechanical parts

### Setup Steps

1. **Fork and clone the repository**
   ```bash
   # Fork the repo on GitHub first, then clone your fork
   git clone https://github.com/YOUR_GITHUB_USERNAME/robot_jarvis.git
   cd robot_jarvis
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   cd firmware
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Run tests**
   ```bash
   pytest tests/
   ```

## Coding Standards

### Python Code Style

- **Follow PEP 8** - Use `black` for formatting (line length: 100)
- **Type hints** - Use type annotations for function signatures
- **Docstrings** - Google-style docstrings for all public functions/classes
- **Comments** - Explain "why", not "what"

Example:
```python
def calculate_servo_angle(position: float, min_angle: float = 0.0, max_angle: float = 180.0) -> float:
    """Calculate servo angle from normalized position.

    Args:
        position: Normalized position (0.0 to 1.0)
        min_angle: Minimum servo angle in degrees
        max_angle: Maximum servo angle in degrees

    Returns:
        Calculated angle in degrees

    Raises:
        ValueError: If position is out of range [0.0, 1.0]
    """
    if not 0.0 <= position <= 1.0:
        raise ValueError(f"Position {position} out of range [0.0, 1.0]")
    return min_angle + position * (max_angle - min_angle)
```

### Hardware Code Guidelines

- **Safety first** - Always include safety checks for voltage, current, temperature
- **Error handling** - Handle I2C failures, GPIO errors gracefully
- **Resource cleanup** - Use context managers for GPIO/I2C resources
- **Hardware validation** - Test on real hardware before submitting

### CAD Model Standards

- **FreeCAD format** - Primary source files in `.FCStd` format
- **STL exports** - Include optimized STL files for 3D printing
- **Documentation** - Add comments in CAD file explaining design decisions
- **Print settings** - Document recommended print settings in README

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, no logic change)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Examples

```
feat(servo): Add emergency stop functionality

Implement hardware-level emergency stop using GPIO 26 interrupt.
Stops all servo commands and cuts power to PCA9685.

Closes #42
```

```
fix(power): Correct UBEC voltage calculation

Fixed voltage divider calculation that was causing incorrect
battery voltage readings. Changed resistor values from 10k/10k
to 10k/4.7k for proper 2S battery monitoring.

Fixes #58
```

## Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write code
   - Add tests
   - Update documentation

3. **Run tests and linting**
   ```bash
   pytest tests/
   black firmware/src/
   mypy firmware/src/
   ```

4. **Commit your changes**
   - Follow commit guidelines
   - Make atomic commits (one logical change per commit)

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a pull request**
   - Use the pull request template
   - Reference related issues
   - Provide clear description of changes
   - Add screenshots/videos for hardware changes

7. **Address review feedback**
   - Be responsive to comments
   - Make requested changes
   - Keep discussions professional and constructive

### Pull Request Checklist

- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages follow guidelines
- [ ] No merge conflicts
- [ ] Hardware changes tested on real hardware (if applicable)
- [ ] Safety features validated (if applicable)

## Testing Requirements

### Unit Tests

- **Coverage target**: 80% minimum
- **Mock hardware**: Use mocks for GPIO/I2C in unit tests
- **Fast execution**: Unit tests should run in <5 seconds

### Integration Tests

- **Hardware simulation**: Test with simulated hardware when possible
- **Real hardware**: Mark tests that require real hardware with `@pytest.mark.hardware`
- **Cleanup**: Ensure GPIO/I2C resources are properly cleaned up

### Hardware Tests

- **Safety first**: Include safety checks in all hardware tests
- **Documentation**: Document required hardware setup
- **Expected behavior**: Document expected outputs (LED patterns, servo movements)

### Running Tests

```bash
# All tests (mock hardware only)
pytest tests/

# Hardware tests (requires real Raspberry Pi + hardware)
pytest tests/ -m hardware

# With coverage report
pytest tests/ --cov=src --cov-report=html
```

## Documentation

### Required Documentation

- **Code documentation**: Docstrings for all public APIs
- **README updates**: Update relevant README files
- **CHANGELOG**: Add entry to CHANGELOG.md
- **Hardware guides**: Document wiring diagrams for hardware changes
- **Safety warnings**: Update SAFETY_WARNINGS.md if relevant

### Documentation Style

- **Clear and concise**: Use simple language
- **Examples**: Provide code examples where helpful
- **Diagrams**: Include wiring diagrams, flowcharts, or photos
- **Safety notes**: Highlight safety concerns prominently

## Questions?

- **Open an issue**: For questions about contributing
- **Check existing docs**: See [firmware/README.md](firmware/README.md) and [docs/](docs/)
- **Hardware questions**: Check hardware-specific documentation in [electronics/](electronics/)

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

**Thank you for contributing!** Every improvement, no matter how small, helps make this project better.

**Last Updated:** 15 January 2026
