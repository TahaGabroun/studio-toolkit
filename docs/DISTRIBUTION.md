# Codex and ChatGPT distribution

The canonical repository contains fifteen separate Agent Skills with YAML name/description, optional agents/openai.yaml, real references and scripts. The maintained installer links them into one selected Codex discovery directory. Current official guidance describes skill folders with name/description and supporting resources: https://learn.chatgpt.com/docs/build-skills and https://developers.openai.com/plugins/concepts/skills. Existing local Codex 0.165.0-alpha.1.2 also exposes ~/.codex/skills; actual discovery was inspected using the local CLI, rather than assuming Claude directories worked.

The ChatGPT artifact is a single skill ZIP with exactly one SKILL.md, specialist references, scripts, schemas and full MIT notices. Build using scripts/package_chatgpt.py. It is not an installer for ordinary chats and was not imported into a ChatGPT account here. Use a host supporting skill upload; execution still requires that host's permitted shell, filesystem, browser and dependencies. In ordinary chat, upload the package as task reference material and apply only available writing/research workflows.

Codex installation does not automatically install anything in ChatGPT. No marketplace submission or listing approval is claimed. The package can be structurally tested by extracting to an isolated directory and running scripts/studio.py init/validate; this is included in regression testing.

The 0.4 package includes all six animation workflows and their shared executable runtime as references, while retaining exactly one SKILL.md. Node dependencies and models are excluded; run the packaged runtime setup in the host environment. The package does not install itself into a ChatGPT account.
