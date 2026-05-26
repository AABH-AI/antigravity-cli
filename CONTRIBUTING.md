# Contributing to AntiGravity CLI

Thank you for your interest in contributing! This document provides guidelines and instructions.

## Code of Conduct

Be respectful, inclusive, and helpful to others in all interactions.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported
2. Provide a clear description of the issue
3. Include steps to reproduce
4. Specify your Termux version and Android version

### Suggesting Features

1. Check if the feature has already been suggested
2. Provide a clear use case
3. Explain the expected behavior
4. Link to similar features if applicable

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/antigravity-cli.git
cd antigravity-cli

# Install in development mode
pip install -e .

# Verify
antigravity --version
```

## Development Guidelines

- Write clear, readable code
- Add comprehensive error handling
- Test on actual Termux environment
- Update documentation as needed
- Follow PEP 8 style guide
- Add docstrings to functions

## Testing

```bash
# Test locally
python -m antigravity tasks --help
python -m antigravity system health

# Check logs
cat ~/.antigravity/logs/*

# Check errors
cat ~/.antigravity/errors.log
```

## Code Style

- Use type hints where possible
- Keep functions focused and small
- Error messages should be clear and helpful
- Always provide recovery suggestions

## Questions?

Open an issue or start a discussion in the GitHub repository.

## License

By contributing, you agree to license your contributions under the MIT License.
