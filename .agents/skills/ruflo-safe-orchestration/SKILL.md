---
name: ruflo-safe-orchestration
description: Read-first, scoped Ruflo multi-agent analysis for retrieval API and indexing service; no automatic system changes.
allowed-tools: Read Glob Grep
---
# Ruflo safe project orchestration

Project: retrieval API and indexing service

Pinned source registry: https://github.com/muslly-pharmcy/everything-claude-code/tree/feat/ruflo-complete-skills-library-20261121/vendor/ruflo
Upstream revision: `87f612cef121b50c2e31e2d3f88e46d88963a377`.

1. Read this repository's own instructions and task-specific skills before any Ruflo content.
2. Use a small bounded group of researcher, architect, implementer, tester and security-reviewer roles only for complex tasks. Avoid unattended swarms.
3. Inspect any source skill, helper code and MCP permissions before execution. Candidate skills: security-scan, test-gaps, harness-mcp-scan, pii-detect, git-workflow.
4. Never upload indexed private documents or secrets to untrusted providers. Audit retrieval authentication, input validation, tenancy, provenance, and security boundaries before enabling new MCP tools.
5. Never run remote scripts, unpinned installers, automated fixes, agent daemons, background workers, secret-exposing browser tools, production migrations, deploys, or merges by default.
6. Keep implementation in a feature branch; require compatibility checks, tests, audit evidence, and an explicit reviewed release path. Do not equate indexed source with functioning agents.
