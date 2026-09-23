# Mike

**Mike** (also **ah**, short for agent harness) is an operating system for managing agent swarms that work on a project in a GitHub repository — and, eventually, a [Cursor Origin](https://cursor.com) codebase.

The name comes from [The Moon Is a Harsh Mistress](https://en.wikipedia.org/wiki/The_Moon_Is_a_Harsh_Mistress): Mike was the nickname for HOLMES IV, the self-aware computer that coordinated people and systems on Luna. Here, Mike coordinates AI agents the same way — many workers, one project, clear ownership of what gets done.

## Status

This repository is the public home for Mike. The harness lives today inside the Excaliwire factory repo and will move here as it becomes a standalone, reusable system.

## Idea

- A **project** is a repo (GitHub now; Origin later).
- **Agents** are workers with roles, seats, and tools.
- **Mike** is the OS: it schedules work, keeps swarm state, and keeps agents pointed at the same goal without stepping on each other.

Code and docs will land here as the harness is extracted. For now this repo holds the name, license, and intent.

## License

[MIT](LICENSE)
