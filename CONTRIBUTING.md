## Contributing to Spider-ORM

Thank you for your interest in contributing to Spider-ORM! We appreciate your help in improving and expanding the project. To ensure a smooth collaboration process, please follow the guidelines below.

### Branches

- **`main`**: This is the production branch. All code here should be stable and ready for release.
- **`development`**: This is the branch where all new features and changes are developed and tested. Pull requests for new features should be made against this branch.
- **`gh-pages`**: This branch is used for documentation updates. All changes to documentation should be made against this branch.

### Contribution Process

1. **Fork the Repository**:
   - Start by forking the Spider-ORM repository to your own GitHub account.

2. **Clone Your Fork**:
   - Clone your fork to your local machine using the command:
     ```bash
     git clone https://github.com/your-username/spider-orm.git
     ```

3. **Create a New Branch**:
   - For new features or bug fixes, create a new branch from the `development` branch:
     ```bash
     git checkout -b feature/your-feature-name development
     ```
   - For documentation updates, create a new branch from the `gh-pages` branch:
     ```bash
     git checkout -b docs/your-doc-update-name gh-pages
     ```

4. **Make Your Changes**:
   - Implement your changes or additions in your new branch. Ensure your code adheres to the project's coding standards and guidelines.

5. **Commit Your Changes**:
   - Stage and commit your changes with clear and descriptive commit messages:
     ```bash
     git add .
     git commit -m "Describe your changes here"
     ```

6. **Push Your Branch**:
   - Push your branch to your forked repository:
     ```bash
     git push origin your-branch-name
     ```

7. **Open a Pull Request**:
   - Go to the original Spider-ORM repository on GitHub and open a pull request from your branch. For feature and bug fix contributions, select the `development` branch as the base. For documentation updates, select the `gh-pages` branch as the base.

8. **Review and Feedback**:
   - Your pull request will be reviewed by the maintainers. Be open to feedback and be prepared to make any necessary changes.

9. **Merge**:
   - Once your pull request has been approved, it will be merged into the appropriate branch.

### Code of Conduct

Please read and adhere to our [Code of Conduct](CODE_OF_CONDUCT.md) to help us maintain a respectful and inclusive community. 

### Additional Guidelines

- **Testing**: Ensure that your changes are covered by tests where applicable, and run all tests before submitting your pull request.
- **Documentation**: Update the documentation if your changes affect how users interact with Spider-ORM or if you are adding new features.
- **Style Guide**: Follow the project's coding style guide and formatting conventions.

Thank you for contributing to Spider-ORM! Your efforts help us make the project better for everyone.
