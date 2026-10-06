# Mike user stories

**Status:** plan. What each role needs from Mike, one story per need, each with its factory evidence, one measurement, and a verdict.

**Source pin:** excaliwire/factory `bb2bf4c6` ([factory tree at the pinned commit](https://github.com/excaliwire/factory/tree/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8)). Each story's evidence links a factory file at that commit, naming the line and what it shows.

**Rules for these files:** [mike.md, the Mike spec](../mike.md) wins over factory and over these stories. Verdicts: KEEP (Mike does what factory does), CHANGE (the need stays, the shape changes), NEW (factory has no form of it). LEGACY stories are listed once in [the retired stories](retired.md) and are not built ([mike.md §14, done when](../mike.md#14-done-when)).

The dashboard and UI stories are the requirements of the rewritten app ([mike.md §7, the dashboard](../mike.md#7-the-dashboard)). The contract they read and write is [Mike's dashboard API](../mike-dashboard-api.md); their factory evidence is provenance only.

**Urgency:** every story ends with an `Urgency:` line in the four words issues use, saying which release builds it ([mike.md §13, the cut: MLP, v1, backlog](../mike.md#13-the-cut-mlp-v1-backlog)): `critical` blocks progress on the current release (none today); `high` is in the MLP, the minimum lovable product; `normal` is in v1, after the MLP works end to end; `no` is backlog, not planned, and every retired story. The `high` stories, in the order to build them, are [the MLP build order](mlp.md).

Stories are grouped by job. Ids are stable: a story keeps its MS id when it moves between files.

## Files

- [observe.md, the observe stories](observe.md): 26 stories (high 13, normal 13, no 0); observe the fleet, the Seats tab and the seat card, phone layout, the board, target versus actual share.
- [steer.md, the steer stories](steer.md): 26 stories (high 14, normal 12, no 0); steer and assign, the control plane watches, humans on GitHub.
- [review.md, the review stories](review.md): 23 stories (high 11, normal 10, no 2); review and merge, the reviewer pool; the Review tab is retired.
- [seats.md, the seats stories](seats.md): 27 stories (high 15, normal 12, no 0); manage seats, the Mike Runtime API, gauges and mint threshold.
- [configure.md, the configure stories](configure.md): 19 stories (high 13, normal 6, no 0); configure, config store apply-on-change, multi-project single instance.
- [diagnose.md, the diagnose stories](diagnose.md): 28 stories (high 18, normal 9, no 1); diagnose and health, audit records, job ids for commands, the dashboard API contract.
- [operate.md, the operate stories](operate.md): 36 stories (high 13, normal 22, no 1); install and recover, identity and secrets, seat and host scoped tokens, attached sessions, cost.
- [testing.md, the testing stories](testing.md): 7 stories (high 6, normal 1, no 0); testing seams, including the dashboard tested at every tier.
- [retired.md, the retired stories](retired.md): 1 story (high 0, normal 0, no 1); one line per retired factory behavior (not built), and the story retired after review.
- [mlp.md, the MLP build order](mlp.md): no stories of its own; the 103 `high` stories in build order, in three parallel tracks and one milestone.

Total: 193 stories: critical 0, high 103, normal 85, no 5.
