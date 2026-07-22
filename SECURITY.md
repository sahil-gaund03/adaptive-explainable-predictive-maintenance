# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of our open-source software seriously. If you discover a security vulnerability, please do **NOT** open a public GitHub issue.

Instead, please send an email directly to **`sahilgaund03@gmail.com`** with:
- Description of the vulnerability
- Steps to reproduce
- Potential impact

We will acknowledge receipt within 48 hours and provide updates on resolution timeline.

## Secret Management Policy

- No private API keys, credentials, tokens, or personal identifiers may be committed to this repository.
- Local configuration secrets must be stored in `.env` (ignored by Git). Refer to `.env.example` for environment variable templates.
