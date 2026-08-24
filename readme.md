# SecureNova AI Identity Security

## Project Overview

SecureNova is an AI-powered customer service platform that uses an LLM agent, Auth0, internal APIs, RAG, and MCP tools.

This capstone focuses on securing the identity layer of the AI system. The project covers threat modelling, IAM implementation, red-team testing, blue-team security controls, compliance mapping, and AI identity security policy.

## Objectives

The main objectives of this project are:

- Identify security risks related to AI and non-human identities.
- Build a threat model using STRIDE and attack trees.
- Implement authentication and authorization using Auth0.
- Test AI identity attacks through a structured red-team campaign.
- Add guardrails and other defensive controls.
- Detect suspicious AI identity activity.
- Map the implemented controls to NIST AI RMF and OWASP LLM security areas.
- Create an AI Identity Security Policy and incident response process.

## Project Structure

```text
01-threat-model/
````

Contains the AI identity threat model, STRIDE analysis, trust boundaries, attack trees, risk register, and MITRE ATLAS mapping.

```text
02-iam-design/
```

Contains the Auth0 identity and access management implementation, including applications, APIs, scopes, MFA, token configuration, and security controls.

```text
03-red-team/
```

Contains the AI identity attack scenarios and testing performed against the vulnerable application, including prompt injection, agent identity spoofing, system prompt extraction, RAG/MCP poisoning, CVSS scoring, and attack results.

```text
04-blue-team/
```

Contains the defensive controls implemented after the red-team testing, including input and output guardrails, JWT redaction, Ed25519 agent identity binding, Auth0 hardening, refresh-token rotation, and anomaly detection.

```text
05-policy/
```

Contains the AI Identity Security Policy, compliance mapping, risk priority analysis, and security recommendations.

## Identity Security

The project considers different types of identities used by the AI platform, including:

* Human users
* AI agents
* OAuth/M2M clients
* LLM API keys
* RAG service identities
* MCP server identities

The security design uses authentication, authorization, least privilege, short-lived tokens, credential rotation, identity verification, and monitoring.

## Red Team Testing

The red-team phase tested several AI identity attack scenarios, including:

* Indirect prompt injection
* Agent identity spoofing
* System prompt extraction
* RAG chunk poisoning
* MCP/tool abuse

The attacks were documented and evaluated using CVSS 3.1 and MITRE ATLAS mappings where applicable.

## Blue Team Controls

The blue-team phase added defensive controls based on the red-team findings.

These included:

* NeMo input guardrails
* JWT output redaction using regular expressions
* Ed25519 cryptographic agent identity binding
* Auth0 token hardening
* Refresh token rotation
* Anomaly detection
* Before-and-after security testing

The hardened application was tested again to verify that the defensive controls reduced the attack success rate.

## Compliance

The project includes compliance mapping for:

* NIST AI Risk Management Framework
* OWASP LLM security categories

The mapping connects the security controls and testing performed in Projects 1–4 with their supporting evidence.

## Security Policy

The final project includes an AI Identity Security Policy covering:

* Identity lifecycle
* Credential governance
* Incident response
* Leaked LLM API keys
* Compromised agent identities
* Prompt injection and data exfiltration

## Author

**Nandayala Abhirama Varma**

SecureNova AI Identity Security Capstone Project

