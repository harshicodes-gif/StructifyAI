# Security Policy

## Supported Versions

Security fixes are applied to the current `main` branch. Users should update to
the latest released commit or tag before reporting an issue that may already be
fixed.

## Reporting a Vulnerability

Please report suspected vulnerabilities privately to the maintainers through a
GitLab confidential issue or the project maintainer contact listed in GitLab.
Do not disclose exploit details publicly until the maintainers have had a
reasonable opportunity to investigate and release a fix.

Include the following information when possible:

* Affected version, branch, or commit
* Steps to reproduce
* Impact and affected data
* Any relevant logs, screenshots, or proof-of-concept details

## Security Expectations

Structify AI is designed for local, offline processing. Contributors should
avoid adding network calls, telemetry, external document processing, or secrets
in source control unless the behavior is explicitly documented and reviewed.
