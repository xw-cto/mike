# Mike user stories: retired

The stories for retired stories, which are not built. Rules, verdicts and the other files: [the user stories index](README.md).

## Retired stories

Not built ([mike.md §3.3, gates for every caller](../mike.md#33-gates-mike-enforces-for-every-caller), [mike.md §10, what Mike does not re-create](../mike.md#10-what-mike-does-not-re-create), [mike.md §13, done when](../mike.md#13-done-when)). One line each.

- The starved-lanes view ("as the control plane reads it"): every lane has a priorities row, so no lane is starved; [MS-136, target versus actual share](observe.md#ms-136-target-versus-actual-share) replaces it ([mike.md §9 rule 17, Health shows target versus actual share](../mike.md#9-what-mike-keeps)); [gate 3, the lane gate](../mike.md#33-gates-mike-enforces-for-every-caller) refuses an issue with no lane label or an unknown lane.
- Redeliver-tries, the conflict-steer cooldown and the orchestrator cooldown: nothing is redelivered; Arthur's follow-up fires on a board change ([MS-131, Arthur reads the board](observe.md#ms-131-arthur-reads-the-board), [decision 1, Arthur steered on change](../mike.md#11-decisions)).
- Verbs holding on an unmeasured reading: there are no holds; a refusal streak is [MS-053, refusal streaks named](diagnose.md#ms-053-refusal-streaks-named) ([mike.md §10 item 1, the steer-idle planner](../mike.md#10-what-mike-does-not-re-create)).
- Assigned but never steered: the label is the assignment and the remint carries it ([MS-034, remint carries the assignment](seats.md#ms-034-remint-carries-the-assignment), [mike.md §3.1, pool, assignment and share](../mike.md#31-pool-assignment-share)); the board shows it.
- Fleet idle with work, with the last planner reason: the planner is gone; the board and share rows show idle capacity ([MS-136, target versus actual share](observe.md#ms-136-target-versus-actual-share), [mike.md §10 item 1, the steer-idle planner](../mike.md#10-what-mike-does-not-re-create)).
- Frozen lane focus: there is no lane owner to freeze ([MS-015, edit the priorities list](steer.md#ms-015-edit-the-priorities-list), [mike.md §3.1, pool, assignment and share](../mike.md#31-pool-assignment-share)).
- The worker planner (steer-idle) with its 12 hold words, 12 none-eligible reasons and 9 wordless gates: Arthur decides from the board ([MS-131, Arthur reads the board](observe.md#ms-131-arthur-reads-the-board), [mike.md §10 item 1, the steer-idle planner](../mike.md#10-what-mike-does-not-re-create), [mike.md §10 item 2, two deciders on one roster](../mike.md#10-what-mike-does-not-re-create)).
- Enqueue and redeliver through `assign` and `assignments.jsonl`: one store, every steer through the control plane, no second queue ([MS-073, record every steer first](steer.md#ms-073-record-every-steer-first), [mike.md §10 item 7, machine-local steer queues](../mike.md#10-what-mike-does-not-re-create)).
- Stand-down and resume: a seat waiting on a gate gets a steer from Arthur ("wait for <issue>") ([MS-131, Arthur reads the board](observe.md#ms-131-arthur-reads-the-board), [mike.md §10 item 18, stand-down and resume](../mike.md#10-what-mike-does-not-re-create)).
- The reboot tail queueing one restart per grok-tmux orchestrator: the one-pending-actuation rule ([MS-033, no double actuation](seats.md#ms-033-no-double-actuation)) covers every runtime ([mike.md §4, runtimes](../mike.md#4-runtimes)).
- Lane-PE host moves down the ladder: gauges with a mint threshold replace the ladder ([MS-144, runtimes declare gauges in config](seats.md#ms-144-runtimes-declare-gauges-in-config), [MS-145, switch vendor at mint threshold](seats.md#ms-145-switch-vendor-at-mint-threshold), [decision 15, holds and the ladder retire](../mike.md#11-decisions)).
- Ladder tier moves on included-pool gauges: same; the gauges stay ([MS-070, vendor included pools shown](operate.md#ms-070-vendor-included-pools-shown)), the ladder goes ([decision 15, holds and the ladder retire](../mike.md#11-decisions)).
- The owned-work preamble ("A send-back beats other owned work, and owned work beats a new ticket."): a seat owns one assignment; a send-back is its next one ([MS-093, send-back returns to author](review.md#ms-093-send-back-returns-to-author), [mike.md §3.4, review and send-back](../mike.md#34-review-and-send-back)).
- The seat-assignment Discussion board publisher (`dashboard --publish`, `--minimize-stale`, `dashboards_retired`): retired boards, about 1300 dead lines ([MS-131, Arthur reads the board](observe.md#ms-131-arthur-reads-the-board), [mike.md §10 item 14, the Discussion board publisher](../mike.md#10-what-mike-does-not-re-create)).
- The `retitle` one-shot migration: finished on factory; not product code ([mike.md §10 item 20, one-shot migration verbs](../mike.md#10-what-mike-does-not-re-create)).
- The `seat-rename` one-shot migration: a stable seat id makes rename a config edit ([MS-134, role names renamable in config](observe.md#ms-134-role-names-renamable-in-config), [mike.md §10 item 20, one-shot migration verbs](../mike.md#10-what-mike-does-not-re-create)).
- The `Lexicon: Clear.` review line and the four-line self-review form: retired on factory by [factory#1741, terse comment guidance](https://github.com/excaliwire/factory/issues/1741); line 1's verdict carries it ([MS-083, self-review in one shape](review.md#ms-083-self-review-in-one-shape), [mike.md §3.4, review and send-back](../mike.md#34-review-and-send-back)).

## Retired after review

#### MS-147 Mint runs capped by budget
As a human (Tig today), I wanted each mint run capped by a token and turn budget and cancelled when over.
Evidence: [factory#1755, lane-PE mint burns tokens](https://github.com/excaliwire/factory/issues/1755), its done-when.
Verdict: LEGACY: the budget came from that issue's done-when, not from a human; Mike has no budgets. A wait-only mint ([MS-099, mint wait-only](seats.md#ms-099-mint-wait-only)) and gauges with a mint threshold ([MS-145, switch vendor at mint threshold](seats.md#ms-145-switch-vendor-at-mint-threshold), [mike.md §4, runtimes](../mike.md#4-runtimes)) cover the cost.
