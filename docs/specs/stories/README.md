# Mike user stories

**Status:** plan. What each role needs from Mike, one story per need, each with its factory evidence, one measurement, and a verdict.

**Source pin:** excaliwire/factory `bb2bf4c6` ([factory tree at the pinned commit](https://github.com/excaliwire/factory/tree/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8)). Each story's evidence links a factory file at that commit, naming the line and what it shows.

**Rules for these files:** [mike.md, the Mike spec](../mike.md) wins over factory and over these stories. Verdicts: KEEP (Mike does what factory does), CHANGE (the need stays, the shape changes), NEW (factory has no form of it). LEGACY stories are listed once in [the retired stories](retired.md) and are not built ([mike.md §13, done when](../mike.md#13-done-when)).

The dashboard and UI stories are the requirements of the rewritten client ([mike.md §7, the dashboard](../mike.md#7-the-dashboard)). The contract they read and write is [Mike's dashboard API](../mike-dashboard-api.md); their factory evidence is provenance only.

Stories are grouped by job. Ids are stable: a story keeps its MS id when it moves between files.

## Files

- [observe.md, the observe stories](observe.md): 26 stories; observe the fleet, the Seats tab and the seat card, phone layout, the board, target versus actual share.
- [steer.md, the steer stories](steer.md): 26 stories; steer and assign, the control plane watches, humans on GitHub.
- [review.md, the review stories](review.md): 23 stories; review and merge, the review surface.
- [seats.md, the seats stories](seats.md): 27 stories; manage seats, the Mike Runtime API, gauges and mint threshold.
- [configure.md, the configure stories](configure.md): 19 stories; configure, config store apply-on-change, multi-project single instance.
- [diagnose.md, the diagnose stories](diagnose.md): 28 stories; diagnose and health, audit records, job ids for commands, the dashboard API contract.
- [operate.md, the operate stories](operate.md): 36 stories; install and recover, identity and secrets, seat and host scoped tokens, attached sessions, cost.
- [testing.md, the testing stories](testing.md): 7 stories; testing seams, including the dashboard tested at every tier.
- [retired.md, the retired stories](retired.md): 1 story; one line per retired factory behavior (not built), and the story retired after review.

Total: 193 stories.
