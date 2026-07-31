# Security Policy

## Supported versions

The latest tagged release and the default branch receive security fixes. The
current project is pre-1.0 and interfaces may change between minor releases.

## Reporting a vulnerability

Use GitHub's private vulnerability-reporting feature when it is available for
this repository. Do not open a public issue containing exploit details,
credentials, private prompts, or sensitive financial information.

If private reporting is not enabled, open a minimal public issue asking the
maintainer to establish a private contact channel. Include no technical detail
that would make exploitation easier.

Useful reports include:

- arbitrary code execution or unsafe deserialization;
- credential exposure in logs or reports;
- unintended network or production-tool execution;
- a scoring flaw that systematically hides critical failures;
- a way to inject real confidential data into published artifacts.

Ordinary benchmark disagreements, new-case proposals, and false positives
should use the relevant issue template instead.

## Safe testing

Test only with synthetic data and systems you own or are authorized to assess.
Never submit real credentials, customer information, non-public transactions,
or confidential employer material.

## Response targets

The maintainer will aim to acknowledge a complete report within seven days,
assess severity, and coordinate a fix and disclosure timeline appropriate to
the risk. These are targets rather than a service-level agreement.
