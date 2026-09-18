# Contributing to Fluxterprise Skills

Thank you for your interest in contributing to Fluxterprise Skills. This document outlines the process for contributing to this project.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

When creating a bug report, include:

- A clear, descriptive title
- Steps to reproduce the behavior
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Environment details (OS, agent version, Flutter version)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- A clear, descriptive title
- A detailed description of the proposed enhancement
- Why this enhancement would be useful
- Examples of how it would be used

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development Setup

### Prerequisites

- Git
- A text editor or IDE
- (Optional) Flutter SDK for testing Flutter-specific skills

### Getting Started

```bash
# Clone the repository
git clone https://github.com/candraprasetya/fluxterprise-skills.git
cd fluxterprise-skills

# Create a branch
git checkout -b feature/your-feature

# Make your changes
# ...

# Test your changes
# Load the skills in your AI agent and verify they work correctly

# Commit and push
git add .
git commit -m "feat: describe your change"
git push origin feature/your-feature
```

## Commit Convention

This project follows [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` — New feature
- `fix:` — Bug fix
- `docs:` — Documentation changes
- `style:` — Code style changes (formatting, etc.)
- `refactor:` — Code refactoring
- `test:` — Adding or updating tests
- `chore:` — Maintenance tasks

Examples:
```
feat: add fluxterprise-perf skill for performance auditing
fix: correct R-XX to FG-XX aliasing in fluxterprise-ui
docs: update README with new installation methods
```

## Skill Development Guidelines

### Creating a New Skill

1. Create a directory: `skills/fluxterprise-<name>/`
2. Create `SKILL.md` with frontmatter:
   ```yaml
   ---
   name: fluxterprise-<name>
   description: "Brief description of what this skill covers."
   allowed-tools: Read Write Edit Glob Grep
   ---
   ```
3. Follow the existing skill structure:
   - **Tell** — the pattern
   - **Why** — why it falls below the gate
   - **Fix** — what to do instead
   - Reference core rules by number (`FG-XX`)
   - Add a checklist at the end
4. Add credit: `> Created by **Your Name**`
5. Update the pointer block in README.md
6. Update the install script if needed

### Skill Quality Standards

Every skill must:

- Follow the Tell/Why/Fix pattern consistently
- Reference core rules by number (`FG-XX`), never renumber
- Include a checklist at the end
- Have zero generic AI patterns (no buzzwords, no empty claims)
- Be testable by loading it into an AI agent and verifying output
- Include concrete code examples where applicable
- Be cross-platform compatible (web, mobile, desktop)

### Testing Your Skill

1. Load the skill into your AI agent (Claude Code, OpenCode, etc.)
2. Give the agent a task that should trigger the skill
3. Verify the agent follows the skill's rules
4. Check that the output passes the Quality Gate
5. Document any edge cases or failures

## Style Guide

### Markdown

- Use ATX-style headers (`#`, `##`, `###`)
- Use fenced code blocks with language identifiers
- Use tables for structured data
- Use bullet points for lists
- Keep lines under 120 characters where possible

### Code Examples

- Use complete, runnable examples when possible
- Include both WRONG and CORRECT examples
- Add comments explaining why something is wrong
- Use the project's naming conventions

### Terminology

| Term | Definition |
|------|-----------|
| **Quality Gate** | The five-block check that every deliverable must pass |
| **Hard Gate** | Absolute rules that cannot be bypassed |
| **Purpose Gate** | Techniques allowed but requiring a written reason |
| **Quality Locks** | Consistency requirements |
| **Craftsmanship** | The positive requirements (dials, levers, identity) |
| **FG-XX** | Fluxterprise Gate rule number |

## Release Process

1. Update version in relevant files
2. Update CHANGELOG.md
3. Create a git tag: `git tag v1.0.0`
4. Push the tag: `git push origin v1.0.0`
5. Create a GitHub Release with release notes

## Questions?

Open a GitHub issue or discussion for any questions about contributing.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
