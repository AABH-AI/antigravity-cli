# Contributing to AntiGravity CLI

We welcome contributions! This document explains how to contribute.

## How to Contribute

### Report Bugs

1. Check if the bug has already been reported
2. Open an issue with:
   - Error message
   - Steps to reproduce
   - Device info: `antigravity info device`
   - Termux version

### Suggest Features

1. Check if the feature is already suggested
2. Open an issue with:
   - Use case description
   - Expected behavior
   - Examples

### Submit Changes

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Test your changes
5. Commit: `git commit -m 'Add feature description'`
6. Push: `git push origin feature/your-feature`
7. Open a Pull Request

## Development Setup

```bash
git clone https://github.com/AABH-AI/antigravity-cli.git
cd antigravity-cli
pip install -e .
```

## Code Style

- Follow PEP 8
- Add docstrings to functions
- Keep functions focused
- Add error handling

## Testing

Test your changes:

```bash
antigravity --help
antigravity info device
antigravity google --help
```

## License

All contributions are licensed under MIT License.

---

**Thank you for contributing!** 🚀
