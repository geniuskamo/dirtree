# Contributing to Dirtree

Thank you for considering contributing to Dirtree! We welcome contributions from the community to help improve this project.

## How to Contribute

### Reporting Bugs

If you find a bug, please report it by opening an issue on the [GitHub Issues](https://github.com/yourusername/dirtree/issues) page. Include as much detail as possible to help us understand and reproduce the issue.

### Feature Requests

If you have an idea for a new feature, please open an issue on the [GitHub Issues](https://github.com/yourusername/dirtree/issues) page. Describe the feature in detail and explain why it would be useful.

### Submitting Changes

1. Fork the repository on GitHub.
2. Clone your fork to your local machine:
   ```bash
   git clone https://github.com/yourusername/dirtree.git
   cd dirtree
   ```
3. Create a new branch for your changes:
   ```bash
   git checkout -b my-feature-branch
   ```
4. Make your changes and commit them with a clear and descriptive commit message:
   ```bash
   git commit -am "Add new feature"
   ```
5. Push your changes to your fork:
   ```bash
   git push origin my-feature-branch
   ```
6. Open a pull request on the original repository. Provide a clear description of your changes and the problem they solve.

### Code Style

Please follow the existing code style and conventions used in the project. We use `flake8` and `black` for linting and formatting. You can run these tools locally before submitting your changes:

```bash
make lint
make format
```

### Running Tests

Ensure that all tests pass before submitting your changes. You can run the tests using `pytest`:

```bash
make test
```

### Documentation

If your changes affect the documentation, please update the relevant sections in the `README.md` file.

## Code of Conduct

Please be respectful and considerate in your interactions with others. We follow the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/0/code_of_conduct/).

Thank you for contributing to Dirtree!
