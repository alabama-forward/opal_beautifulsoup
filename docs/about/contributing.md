# Contributing to OPAL

We welcome contributions to OPAL! This guide will help you get started.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/yourusername/opal.git
   cd opal
   ```
3. Create a new branch for your feature:
   ```bash
   git checkout -b feature-name
   ```

## Development Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

3. Install development dependencies:
   ```bash
   pip install pytest black flake8
   ```

## Contribution Guidelines

### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep lines under 88 characters (Black's default)

### Testing

- Write tests for new features
- Ensure all tests pass before submitting
- Run tests with: `pytest tests/`

### Documentation

- Update documentation for new features
- Include docstrings in your code
- Update README if needed

## Submitting Changes

1. Commit your changes:
   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

2. Push to your fork:
   ```bash
   git push origin feature-name
   ```

3. Create a Pull Request on GitHub

## Pull Request Process

1. Ensure your code follows the style guidelines
2. Update documentation as needed
3. Add tests for new functionality
4. Ensure all tests pass
5. Update the CHANGELOG.md with your changes

## Adding New Parsers

When contributing a new parser:

1. Follow the BaseParser structure
2. Include comprehensive error handling
3. Add documentation to the parser class
4. Create an example in the documentation
5. Test with various edge cases

## Reporting Issues

- Use GitHub Issues to report bugs
- Include detailed reproduction steps
- Provide error messages and logs
- Specify your Python version and OS

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive criticism
- Respect differing viewpoints

## Questions?

Feel free to open an issue for any questions about contributing!