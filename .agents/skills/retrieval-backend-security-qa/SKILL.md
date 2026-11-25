---
name: retrieval-backend-security-qa
description: Audit legacy Python retrieval backend and document privacy without blindly upgrading integrations.
---

# retrieval-backend-security-qa

README identifies deprecated original ChatGPT plugin model; pyproject confirms Python 3.10, Poetry, FastAPI, pytest and older OpenAI client. Use GitHub review, OpenAI developer docs and security threat modeling; inventory actual lockfile, installed providers and test fixtures. Run poetry run pytest only against local or mocked providers with synthetic documents. Verify tenant filtering, bearer authorization, malicious retrieved instructions, deletion, file parsing and secret redaction. Evaluate dependency upgrades separately with compatibility tests; do not activate old API integrations or upload real documents. No UI/design plugins.

## Execution contract
Read repo instructions and existing skills first. Prefer tools already installed; external plugins are candidates until connected and approved. Keep implementation and independent QA separate. Record exact commands, results, commit SHA, blockers and rollback. No production deploy, live writes or secret transfer. Source reference: https://github.com/openai/plugins. This is an original repo-specific skill, not a copy or proof of upstream plugin installation.
