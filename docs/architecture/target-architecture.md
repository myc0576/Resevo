# Resevo Target Architecture

```mermaid
flowchart TD
  Agent["Codex / Claude Code / other external Agent"] --> CLI["resevo CLI"]
  Agent --> MCP["Resevo stdio MCP"]
  MCP --> Service["Shared core + service layer"]
  CLI --> Service
  Service --> Registry["Workspace registries\nknowledge / prompts / assets / decisions"]
  Service --> State["Workspace .resevo/\nconfig / runs / evolution / migration"]
  Service --> Index["Local SQLite FTS + utility metadata"]
  Service --> Validators["Validation + closeout gates"]
  Validators --> Provenance["run / trace / artifact manifest\nclaim-evidence-artifact links"]
  Private["research-harness private instance"] --> Service
  Private --> Extensions["private extensions / prompts / knowledge / project state"]
  Candidate["candidate / pending validation"] --> Validators
  Validators --> Human["human promotion decision"]
```

The public engine owns portable behavior, schemas, validators, CLI services,
MCP adapters, and sanitized examples. The private instance owns workspace
configuration, personal registries, knowledge, prompts, decisions, project
state, run records, and immature extensions. Compatibility wrappers remain at
the private boundary until each duplicated module has a replacement and a
passing regression test.

The dependency direction is one-way:

```text
Resevo public engine -> version-locked research-harness instance
research-harness real use -> sanitized candidate -> validation -> Resevo
```

No promotion path may infer `validated`, `reusable`, `approved`, `pass`, or
`paper_ready` from an ordinary MCP call or an automatic writeback.

