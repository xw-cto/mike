# Mike user stories: seats

The stories for managing seats: mint, remint, archive, the Mike Runtime API, and gauges with the mint threshold. Rules, verdicts and the other files: [the user stories index](README.md).

## Manage seats

#### MS-023 Mint a seat with no session
As a human (Tig today), I want to mint a seat that has no session, wait-only, optionally with an assignment its first steer carries, so that I bring it into being.
Evidence: [factory dashboard verbs.mjs line 62, the mint verb](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/verbs.mjs#L62); [Mike dashboard API §6, commands](../mike-dashboard-api.md#6-commands).
Acceptance: enabled only when every selected row lists mint; one decision record per seat before the vendor call; the new session reads its brief and waits ([mike.md §3.2, mint, remint, steer](../mike.md#32-mint-remint-steer)).
Verdict: KEEP.

#### MS-024 Restart a stuck seat
As a human (Tig today), I want to restart a seat after one confirm, keeping its assignment, so that I replace a stuck session.
Evidence: [factory dashboard verbs.mjs line 63, the restart verb](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/verbs.mjs#L63); [Mike dashboard API §6, commands](../mike-dashboard-api.md#6-commands).
Acceptance: body carries `confirm:"restart"`; the label is unchanged afterwards; one restart record exists.
Verdict: KEEP.

#### MS-025 Archive any seat's session
As a human (Tig today), I want to archive any seat's session after one confirm, keeping the name, so that I end it on any runtime.
Evidence: [factory dashboard verbs.mjs line 65, the archive verb](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/verbs.mjs#L65).
Acceptance: for each configured runtime, archive leaves liveness `not-minted` on the next frame and one archive record.
Verdict: CHANGE: factory archives cursor-cloud and claude-tmux only; Mike archives every runtime ([mike.md §4, runtimes](../mike.md#4-runtimes)).

#### MS-026 One verb on checked rows
As a human (Tig today), I want to check rows, or all rows, and run one verb on all of them, so that I act on a group.
Evidence: [factory dashboard app.js line 1562, the row checkboxes](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L1562); [Mike dashboard API §7, payload shapes](../mike-dashboard-api.md#7-payload-shapes).
Acceptance: the bar reads "N seats selected"; a verb is enabled only if every checked row lists it.
Verdict: KEEP.

#### MS-027 Verb buttons explain themselves
As a human (Tig today), I want each verb button to say what it does and why it is off, in the server's words, so that I do not guess and the page cannot drift.
Evidence: [factory dashboard verbs.mjs line 71, the verb hover text](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/verbs.mjs#L71); [Mike dashboard API §7, payload shapes](../mike-dashboard-api.md#7-payload-shapes).
Acceptance: 0 why-off strings in the page source; each tooltip equals the server's field for that row and verb.
Verdict: CHANGE: factory's `verbReason` re-derives the rule in prose and already disagrees with the server ([mike.md §10 item 21, dashboard patches](../mike.md#10-what-mike-does-not-re-create)); Mike's server sends `verb_why` per verb on each `seatRow` ([Mike dashboard API §7, payload shapes](../mike-dashboard-api.md#7-payload-shapes)).

#### MS-028 Verbs offered by the control plane
As a human (Tig today), I want verbs offered only when the control plane lists them for the row, so that I cannot mint over a responding seat: one session per seat name.
Evidence: [factory dashboard verbs.mjs line 35, the row verb list check](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/verbs.mjs#L35); [Mike dashboard API §6, commands](../mike-dashboard-api.md#6-commands).
Acceptance: no button is enabled for a verb a selected row's `verbs` lacks; the server refuses the verb anyway with a record; a responding or unmeasured row never lists mint ([gate 7, one session per seat name](../mike.md#33-gates-mike-enforces-for-every-caller)).
Verdict: KEEP.

#### MS-029 Commands shown as notifications
As a human (Tig today), I want each command I send shown as a notification that moves from sent to done, started or refused with the why, so that I know what happened without reading logs.
Evidence: [factory dashboard rules.mjs line 1032, the command notifications](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L1032); [Mike dashboard API §6, commands](../mike-dashboard-api.md#6-commands).
Acceptance: a notification appears at click time carrying the job id ([MS-137, job ids for every command](diagnose.md#ms-137-job-ids-for-every-command)) and is updated by the answer; an identical pending command is not re-sent.
Verdict: CHANGE: keyed by job id from the 202 and updated from the `jobs` part, not by a 30-second wait ([Mike dashboard API §6, commands](../mike-dashboard-api.md#6-commands)).

#### MS-030 Change a role's vendor and model
As a human (Tig today), I want to change a role's vendor, runtime and model and choose remint now, when idle, or at the next reboot, so that I control when the money is spent.
Evidence: [factory dashboard app.js line 1034, the role vendor editor](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L1034).
Acceptance: the dialog lists exactly the seats of that role; only those seats remint; each keeps its old values until its trigger; the pending rows are written before the settings version.
Verdict: CHANGE: the field is `runtime`, not `harness` ([decision 7, the field is runtime](../mike.md#11-decisions)).

#### MS-031 Pick each vendor's billing account
As a human (Tig today), I want to pick which account each vendor bills, by secret name, so that a seat runs on the right subscription.
Evidence: [factory harness settings.py line 554, the vendor account setting](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/settings.py#L554).
Acceptance: one picker per vendor; with no account named it is disabled and reads "unmeasured: <reason>"; no value of a secret reaches the page.
Verdict: CHANGE: per vendor from config, not four fixed harness rows.

#### MS-032 Lane-PE mints need my word
As a human (Tig today), I want a lane-PE minted by me or by the loop only when that role's fill-missing setting is on, and turning it on to ask me first, so that an expensive seat is never spawned without my word.
Evidence: [factory brief factory-pe.md line 13, the lane-PE mint rule](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/briefs/factory-pe.md#L13).
Acceptance: with the setting off, a week of ticks, Hard Reboot and Arthur's verbs mint 0 lane-PE seats; turning it on shows the confirm naming the mints and the spend; a seat-token mint of a lane-PE is a refused record; every lane-PE mint is wait-only.
Verdict: CHANGE: the setting stays, off by default, human-only, with the confirm ([mike.md §2, roles](../mike.md#2-roles), [decision 12, Mike may mint lane-PEs](../mike.md#11-decisions)).

#### MS-033 No double actuation
As a worker (Artificer), I want mint and restart withheld while any actuation for me is pending, so that my session is not restarted twice and my first steer not sent twice.
Evidence: [factory harness seat_actuator.py line 318, the pending actuation check](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/seat_actuator.py#L318).
Acceptance: while an actuation is pending, the row's `verbs` lacks mint and restart and the server refuses both.
Verdict: CHANGE: one rule for every runtime and actuation kind, not a create-queued special case.

#### MS-034 Remint carries the assignment
As a worker (Artificer), I want a remint, including Worker Reboot, to carry my assignment so that my first steer after it is the same work, so that I do not lose context.
Evidence: [factory dashboard rules.mjs line 1292, Worker Reboot](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L1292).
Acceptance: after a reboot without Reset Defaults, each worker's and reviewer's first steer record has why `remint` and names its prior assignment; no other row redelivers it.
Verdict: KEEP.

#### MS-098 Remint keeps one agent per name
As Arthur (arbiter), I want a remint to archive the live session and mint one new session for the same name, and to refuse unknown or over-cap names, so that there is one session per seat name.
Evidence: [factory harness __main__.py line 1380, the remint verb](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L1380).
Acceptance: after a remint the vendor lists 1 live session for the name; a mint over a responding or unmeasured session is refused ([gate 7, one session per seat name](../mike.md#33-gates-mike-enforces-for-every-caller)); a name beyond the pool cap is refused with a record.
Verdict: CHANGE: the verb is remint for every runtime, writing one record, not a Cursor-shaped create.

#### MS-099 Mint wait-only
As a seat (any), I want to be minted wait-only and receive work only through a steer, so that a mint costs little and is never read as permission to pick work.
Evidence: [factory harness initial_prompt.py line 30, the wait-only mint prompt](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/initial_prompt.py#L30).
Acceptance: for every role, lane-PEs included, the mint prompt ends at "Wait for the first steer" and the mint run reads 0 issues.
Verdict: CHANGE: factory makes only worker mints wait-only; a lane-PE mint read 4.2M and 5.0M tokens in 30 minutes ([factory#1755, lane-PE mint burns tokens](https://github.com/excaliwire/factory/issues/1755)).

#### MS-100 First steer rendered from config
As a seat (any), I want my first steer after a mint or remint rendered by code from config, naming my assignment, so that no hand-written standing prompt drifts from Mike.
Evidence: [factory harness initial_prompt.py line 384, the first-steer template](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/initial_prompt.py#L384).
Acceptance: the remint steer matches this shape and passes the brief size test; "Do not take priority order from this prompt." and "No urgency label is `urgency:no`." appear in orchestrator first steers.
```
[<Name>] Fresh instance, same name. Assignment: <owner/repo>#N (<url>).
Read it in full. Draft the pull request before the first behavior change. Test first. Do not merge.
When the pull request is merged or closed, stop and wait for the next steer. Do not pick new work yourself.
```
Verdict: CHANGE: one template for every remint; the boards and report-and-wait lines go; "Unset severity is Low." becomes the urgency line ([mike.md §3.1, pool, assignment and share](../mike.md#31-pool-assignment-share)).

#### MS-101 Pool converges without double mint
As the loop, I want the pool brought to its configured size without ever minting twice, so that the fleet converges without a human.
Evidence: [factory harness mint_standing.py line 1, the standing mint](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/mint_standing.py#L1).
Acceptance: a pending mint or a live session for a name gives 0 new mints; an unreadable vendor listing gives 0 mints and a refused record.
Verdict: CHANGE: the pool is a cap and a name list; a seat is killed only when stale or at the cap ([decision 11, the pool model](../mike.md#11-decisions)).

#### MS-102 Orphan sessions named and fixed
As a human (Tig today), I want a fleet read that names untracked, missing and duplicate vendor sessions per runtime, and an apply that adopts or archives them, so that orphan agents stop accumulating.
Evidence: [factory harness fleet.py line 1, the fleet read](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/fleet.py#L1).
Acceptance: the read writes nothing; after apply each name has exactly 1 live session; a refused listing reads `unmeasured`.
Verdict: CHANGE: one actuator listing per runtime, not Cursor only; adopt, not claim.

#### MS-103 Restart uses the recorded launch
As Arthur (arbiter), I want restart to use the seat's recorded launch script and seat host, so that a tmux seat never relaunches with the wrong directory, model or host.
Evidence: [factory harness __main__.py line 1651, the restart launch script](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L1651).
Acceptance: a restart of a seat on another host becomes a pending actuation for that host and runs 0 tmux commands on the control-plane host; a missing launcher refuses by name.
Verdict: KEEP.

## The Mike Runtime API

#### MS-148 One actuator interface
As the loop, I want one Mike Runtime API (mint, steer, stop, restart, archive, liveness, usage, session log) that every runtime driver fills or answers `unmeasured` with a reason, whatever its vendor and access method (`cloud` or `tmux`), so that no runtime has a special path in core.
Evidence: [factory harness seat_actuator.py line 353, the actuator](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/seat_actuator.py#L353); [factory#1336 learnings 6, 11, the harness redesign](https://github.com/excaliwire/factory/issues/1336); [mike.md §4, runtimes](../mike.md#4-runtimes).
Acceptance: a contract test runs the 8 capabilities against each configured runtime and gets a result or `unmeasured` plus reason for each.
Verdict: NEW.

#### MS-149 Every steer confirmed or not
As a worker (Artificer), I want every steer on every runtime, `cloud` or `tmux` access, confirmed by a run id, pane echo or event id, or reported not confirmed, so that I never get a duplicate or a lost task.
Evidence: [factory harness seat_host.py line 934, delivery confirmation](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/seat_host.py#L934), [factory#1630, grok paste not shown](https://github.com/excaliwire/factory/issues/1630).
Acceptance: each steer record ends `confirmed` with an id or `not confirmed` with a reason; a confirmed steer is never resent.
Verdict: CHANGE: factory confirms tmux pastes and Cursor runs differently; Mike has one result field for all runtimes ([mike.md §4, runtimes](../mike.md#4-runtimes)).

#### MS-150 One record shape per actuation
As a human (Tig today), I want mint, archive, restart and kill each to write a decision record of one shape for every runtime, so that Health can show a row clear and "no seat minted twice for one issue".
Evidence: [factory harness seat_actuator.py line 1499, log lines only](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/seat_actuator.py#L1499); [factory#1418, Health red for tmux seats](https://github.com/excaliwire/factory/issues/1418).
Acceptance: each actuation has one record before it acts; Health reads only that record shape (test with one `cloud` and one `tmux` runtime).
Verdict: NEW.

#### MS-151 One pending steer per seat
As a human (Tig today), I want no second steer to a seat while one is pending in the loop window, for every caller and every runtime, pending ones included, so that a seat never gets two tasks at once.
Evidence: [factory harness __main__.py line 1054, `_loop_steer_hold` covers the loop and applied rows only](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L1054); [gate 5, one pending steer](../mike.md#33-gates-mike-enforces-for-every-caller).
Acceptance: a human steer, an Arthur steer and a loop steer sent to one seat inside the window give 1 applied and 2 refused records.
Verdict: NEW.

#### MS-172 Session log from every runtime
As a human (Tig today), I want each runtime to provide a seat's session log, its inputs and responses, with the last steer and the latest response marked, so that I and Arthur see what a seat was told and what it said on any vendor.
Evidence: [factory dashboard app.js line 2502, the seat page reads a stored log](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L2502); [mike.md §4, runtimes](../mike.md#4-runtimes); [Mike dashboard API §5, reads](../mike-dashboard-api.md#5-reads).
Acceptance: for each configured runtime the log's last input equals the last confirmed steer record's prompt and one response is marked latest; a runtime that cannot read it answers `unmeasured` with a reason; the seat page ([MS-007, seat page for diagnosis](observe.md#ms-007-seat-page-for-diagnosis)) reads it.
Verdict: NEW.

#### MS-173 Install a runtime driver by config
As a human (Tig today), I want to install or enable a new runtime driver through config, so that a new vendor or access method needs no change to Mike's core.
Evidence: [factory#1336 comments, learnings 6, 9 and 11 on the single-vendor actuator](https://github.com/excaliwire/factory/issues/1336); [mike.md §4, runtimes](../mike.md#4-runtimes).
Acceptance: enabling a driver is a config edit with 0 core code changes; the driver passes the [MS-148, one actuator interface](#ms-148-one-actuator-interface) contract test before any mint lands on it; config naming a driver not installed is refused and named on Health.
Verdict: NEW.

## Gauges and mint threshold

#### MS-144 Runtimes declare gauges in config
As a human (Tig today), I want each runtime to declare its gauges (pools, windows, probe and mint threshold) in config, so that gauges change without code.
Evidence: [factory harness meters.py line 16, `GAUGES` is a code tuple](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/meters.py#L16); [mike.md §4, runtimes](../mike.md#4-runtimes).
Acceptance: adding a gauge is a config edit with 0 code changes and its gauge appears on the Gauges tab.
Verdict: NEW.

#### MS-145 Switch vendor at mint threshold
As the loop, I want mint to pick the next vendor when one crosses its mint threshold, so that a vendor limit costs a vendor switch, not a stall.
Evidence: [factory#1501, the Mike extraction](https://github.com/excaliwire/factory/issues/1501) (at 75 percent of Claude's 5-hour limit, stop minting Claude seats and shift to xAI Grok, [decision 10, shift new seats to xAI Grok](../mike.md#11-decisions)); [mike.md §4, runtimes](../mike.md#4-runtimes).
Acceptance: with the Claude 5-hour gauge at 76 percent, the next mint record names a different vendor and cites the gauge reading.
Verdict: NEW.

#### MS-146 No mint on unmeasured gauge
As the loop, I want a mint that depends on an unmeasured gauge refused, so that an unknown gauge reading is never read as free.
Evidence: [factory harness meters.py line 73, the gauge reader](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/meters.py#L73); [mike.md §4, runtimes](../mike.md#4-runtimes).
Acceptance: with the vendor gauge `unmeasured`, 0 mints on that vendor; each attempt is a refused record naming the gauge; the gauge never reads 0.
Verdict: NEW.
