# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | ✅ Active support  |
| < 1.0   | ❌ No longer supported |

## Reporting a Vulnerability

If you discover a security vulnerability in Fluxterprise Skills, please report it responsibly.

### How to Report

1. **DO NOT** open a public GitHub issue for security vulnerabilities
2. Email security reports to: [INSERT SECURITY EMAIL]
3. Include the following in your report:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- **Acknowledgment**: Within 48 hours of your report
- **Initial Assessment**: Within 5 business days
- **Resolution Timeline**: Depends on severity
  - Critical: Within 7 days
  - High: Within 14 days
  - Medium: Within 30 days
  - Low: Within 90 days

### Disclosure Policy

- We will acknowledge receipt of your vulnerability report
- We will provide an estimated timeline for a fix
- We will notify you when the vulnerability is fixed
- We will credit you in the security advisory (unless you prefer to remain anonymous)

## Security Considerations

### Skill Files

Fluxterprise Skills are instruction files loaded by AI coding agents. They do not execute code directly. However:

- **Never load untrusted skill files** from unknown sources
- **Verify skill file contents** before loading into your agent
- **Keep skills updated** to the latest version
- **Report suspicious patterns** in skill files

### Contrast Checker Scripts

The contrast checker scripts (`contrast-check.py`, `contrast-mcp.py`) are utility tools:

- They only perform mathematical calculations (WCAG contrast ratios)
- They do not make network requests
- They do not access sensitive data
- They only read/write to the local filesystem when explicitly invoked

### Installation Script

The install script (`scripts/install.sh`) performs:

- Copying skill files to a target directory
- Modifying entry files (CLAUDE.md, AGENTS.md, etc.) to add pointer blocks
- No network access
- No system-level changes
- No privilege escalation

## Best Practices

1. **Pin to a specific version** in production environments
2. **Review skill changes** before updating
3. **Use the pointer block** mechanism for controlled loading
4. **Test skills** in a development environment first
5. **Keep backups** of your entry files before installation

## Contact

For security-related inquiries, please contact:

- GitHub: [@candraprasetya](https://github.com/candraprasetya)
- LinkedIn: [Nicodemus Lin](https://www.linkedin.com/in/nicodemus-lin/)
