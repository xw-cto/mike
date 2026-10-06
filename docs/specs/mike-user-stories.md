# Mike user stories

**Status:** plan. What each role needs from Mike, one story per need, each with its factory evidence, one measurement, and a verdict.

**Source pin:** excaliwire/factory `bb2bf4c6` ([factory tree at the pinned commit](https://github.com/excaliwire/factory/tree/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8)). Each story's evidence links a factory file at that commit, naming the line and what it shows.

**Rules for this file:** [mike.md, the Mike spec](mike.md) wins over factory and over these stories. Verdicts: KEEP (Mike does what factory does), CHANGE (the need stays, the shape changes), NEW (factory has no form of it). LEGACY stories are listed once in [section 4, retired stories](#4-retired-stories) and are not built ([mike.md §12, done when](mike.md#12-done-when)).

## 1. Dashboard and UI stories

These are the requirements of the rewritten client ([mike.md §7, the dashboard](mike.md#7-the-dashboard)). The contract they read and write is [Mike's dashboard API](mike-dashboard-api.md); factory evidence below is provenance only.

### 1.1 Observe the fleet

#### MS-001 One table of every seat
As a human (Tig today), I want one table of every seat with its name and role, so that I see who exists without reading config files.
Evidence: [factory dashboard app.js line 1646, the seats table](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L1646).
Acceptance: row count equals the configured role seats plus the minted pool names; order is arbiter, TPM, lane-PEs, workers, reviewers; each row reads "Name - Role".
Verdict: CHANGE: rows come from role config and the pool ([mike.md §3.1, pool, assignment and share](mike.md#31-pool-assignment-share), [decision 11, the pool model](mike.md#11-decisions)), not 13 standing names in `seats.yaml`.

#### MS-002 Liveness in four words
As a human (Tig today), I want each seat's liveness as one of four words with the reason on hover, identical for every runtime, so that "no session" and "session not responding" never look alike.
Evidence: [factory dashboard rules.mjs line 878, the liveness cell](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L878); [Mike dashboard API §7, payload shapes](mike-dashboard-api.md#7-payload-shapes).
Acceptance: for cursor-cloud, claude-cloud and grok-tmux seats the word is one of `not-minted`, `responding`, `not-responding`, `unmeasured`; every non-responding word has a non-empty reason; one function computes it (test).
Verdict: KEEP.

#### MS-003 Liveness opens the vendor session
As a human (Tig today), I want the liveness cell to open the vendor session when a seat is minted, so that I can watch it in one click.
Evidence: [factory dashboard rules.mjs line 898, the liveness link](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L898); [Mike dashboard API §7, payload shapes](mike-dashboard-api.md#7-payload-shapes).
Acceptance: a link exists if and only if the word is `responding` or `not-responding` and the URL is http(s).
Verdict: KEEP.

#### MS-004 Assignment shown per seat
As a human (Tig today), I want each seat's assignment as a linked `owner/repo#N` with its title, or idle, so that I see what each seat is on and in which project.
Evidence: [factory dashboard rules.mjs line 840, the assignment cell](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L840); [Mike dashboard API §7, payload shapes](mike-dashboard-api.md#7-payload-shapes).
Acceptance: the cell matches the `seat:<name>` label on GitHub for 100% of rows in a 20-row sample; a pull request links to `/pull/N`.
Verdict: CHANGE: the label is the truth and the store a cache ([mike.md §3.1, pool, assignment and share](mike.md#31-pool-assignment-share)); the project is named on the cell.

#### MS-005 Last confirmed steer shown
As a human (Tig today), I want each seat's last confirmed steer, clipped, with the full text on hover, so that I know what it was last told.
Evidence: [factory dashboard app.js line 1691, the last steer cell](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L1691).
Acceptance: at most 40 characters shown; the full prompt is in the title when longer.
Verdict: KEEP.

#### MS-006 Page updates by itself
As a human (Tig today), I want an open page to update by itself when state changes, so that I never reload.
Evidence: [factory dashboard app.js line 2685, the live update stream](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L2685); [Mike dashboard API §4, the stream](mike-dashboard-api.md#4-the-stream).
Acceptance: a store change reaches an open page in under 2 s plus network time.
Verdict: KEEP.

#### MS-007 Seat page for diagnosis
As a human (Tig today), I want a seat page with liveness, last mint, last steer, pending steer, and the stored session log, so that I can diagnose one seat.
Evidence: [factory dashboard app.js line 2502, the seat page](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L2502); [Mike dashboard API §5, reads](mike-dashboard-api.md#5-reads).
Acceptance: `/sessions/<seat>` shows all 5 blocks; a missing log reads `unmeasured`.
Verdict: KEEP.

#### MS-008 Arthur reads the same API
As Arthur (arbiter), I want the seat list, verbs, assignments and Health over the same API with my seat token, so that my decisions use a human's view.
Evidence: [factory dashboard rules.mjs line 7, the shared row rules](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L7); [Mike dashboard API §5, reads](mike-dashboard-api.md#5-reads).
Acceptance: the sessions read with a seat token returns rows byte-identical to the rows the page draws.
Verdict: KEEP.

#### MS-009 Runtime and host per row
As a human (Tig today), I want each row to name the seat's runtime and host, so that I know where a seat runs without expecting it to carry a control-plane key.
Evidence: [factory harness api.py line 2210, the runtime and host fields](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/api.py#L2210); [Mike dashboard API §7, payload shapes](mike-dashboard-api.md#7-payload-shapes).
Acceptance: every row shows a runtime from the config list and a host or `cloud`; 0 rows carry the per-seat "acts through the control plane" text.
Verdict: CHANGE: every seat acts through the control plane ([mike.md §4, runtimes](mike.md#4-runtimes)), so the special-case marker goes.

### 1.2 Steer and assign

#### MS-010 Steer one seat from its page
As a human (Tig today), I want to type a steer on a seat's page and send it, so that I can redirect one seat fast.
Evidence: [factory dashboard app.js line 2513, the seat page steer box](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L2513); [Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands).
Acceptance: one POST `{verb:steer, seats:[name], prompt}` answered 202 with a job id; the button is disabled unless the row's `verbs` lists steer; the job's outcome names confirmed or not confirmed.
Verdict: CHANGE: 202 with a job id; the outcome arrives on the `jobs` part, not in a synchronous answer ([Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands)).

#### MS-011 Steer several seats at once
As a human (Tig today), I want to steer several checked seats at once with one prompt and an optional assignment, so that I can redirect a group.
Evidence: [factory dashboard app.js line 1377, the multi-seat steer](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L1377); [Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands).
Acceptance: one POST with `seats` equal to every checked name; refused before sending when prompt and assignment are both empty.
Verdict: KEEP.

#### MS-012 Set or clear an assignment
As a human (Tig today), I want to set a seat's assignment (`owner/repo#N`) while minting, steering or restarting, and clear it with `idle`, so that I own the durable assignment.
Evidence: [factory dashboard verbs.mjs line 106, the assignment input](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/verbs.mjs#L106); [Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands).
Acceptance: after a save the `seat:<name>` label is on that issue within one tick; empty input changes nothing; `idle` removes the label.
Verdict: CHANGE: the write is the label in the named project, recorded first.

#### MS-013 Pending steer shown apart
As a human (Tig today), I want a pending steer shown apart from the last confirmed one, with its age and why it waits, so that I know why a steer has not landed.
Evidence: [factory dashboard rules.mjs line 914, the pending steer cell](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L914); [Mike dashboard API §7, payload shapes](mike-dashboard-api.md#7-payload-shapes).
Acceptance: with the loop Paused and a steer pending, the cell reads "pending, not delivered: Paused, <age>" and a second steer to that seat is refused.
Verdict: CHANGE: at most one pending steer per seat ([gate 5, one pending steer](mike.md#33-gates-mike-enforces-for-every-caller)) with a reason, replacing the separate "Assignments untouched" finding.

#### MS-014 Stop keeps the session
As a human (Tig today), I want Stop to set a seat idle and keep its session, and only me or Arthur to undo it, so that the loop leaves it alone.
Evidence: [factory dashboard verbs.mjs line 66, the Stop verb](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/verbs.mjs#L66).
Acceptance: after Stop the cell reads "stopped"; 0 loop steer records target the seat until a record by a human or Arthur clears Stop.
Verdict: CHANGE: factory clears Stop on any human steer; Mike lets a human or Arthur clear it, nothing else ([gate 8, the human switches](mike.md#33-gates-mike-enforces-for-every-caller)).

#### MS-015 Edit the priorities list
As a human (Tig today), I want a priorities list with one row per lane that I can reorder by tap or drag and give a note per row, so that I set what the fleet works on from phone or desk.
Evidence: [factory dashboard app.js line 2143, the priorities editor](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L2143); [Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands).
Acceptance: each reorder or note edit is one POST and one config-store version; the list always has exactly one row per configured lane; adding or deleting a row is refused and names the lanes config; up and down work without drag.
Verdict: CHANGE: priorities list, not direction; one row per lane, so every lane is ranked; rows change only when the lanes in config change ([mike.md §3, the seat model, lanes](mike.md#3-the-seat-model), [mike.md §3.1, pool, assignment and share](mike.md#31-pool-assignment-share)); Mike's API has `POST priorities` (reorder or note) and no `direction` command ([Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands), [decision 8, priorities replace direction](mike.md#11-decisions)).

#### MS-016 Rows follow configured lanes
As a human (Tig today), I want the priorities rows built from the configured lanes, not typed, so that the list cannot contain a typo or miss a lane.
Evidence: [factory dashboard rules.mjs line 1227, the lane picker](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L1227); [Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands).
Acceptance: adding a lane in config adds one row at the bottom and removing one removes its row, each one config-store version; there is no lane picker and no free-text lane.
Verdict: CHANGE: factory's picker guards typed rows; Mike has no typed rows ([mike.md §3, the seat model, lanes](mike.md#3-the-seat-model)).

#### MS-017 Priorities page names unreadable store
As a human (Tig today), I want the priorities page to say when it cannot read the store, so that an unreadable store does not look empty.
Evidence: [factory dashboard rules.mjs line 558, the unreadable store message](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L558).
Acceptance: with the store unreadable the page reads "unmeasured: <reason>", a save is refused, and every worker steer is refused.
Verdict: CHANGE: no seed file view; shipped defaults and instance config are separate files ([mike.md §5, the control plane](mike.md#5-the-control-plane), [mike.md §10 item 16, settings seeded from four places](mike.md#10-what-mike-does-not-re-create)).

#### MS-018 Arthur steers with his token
As Arthur (arbiter), I want to steer a seat with my seat token when the caller matrix allows it, and a denied attempt recorded with my name, so that I assign work without a click and a denial is evidence.
Evidence: [factory harness api.py line 4686, the seat-token steer check](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/api.py#L4686); [Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands).
Acceptance: an allowed call answers 202 and its job reads `actor=<seat>`; a denied one answers 403 and writes a record with `caller=<seat>`, outcome refused.
Verdict: CHANGE: every gate in [mike.md §3.3, gates for every caller](mike.md#33-gates-mike-enforces-for-every-caller) applies to Arthur's steers as to the loop's; the actor is on the job row ([Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands)).

#### MS-019 Steer only owner-assigned work
As the loop, I want to steer only issues and pull requests assigned to `gh_user`, and a human to confirm any change to it, so that a wrong login cannot start spending.
Evidence: [factory harness harness_gh_user.py line 1, the harness-gh-user gate](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/harness_gh_user.py#L1).
Acceptance: changing `gh_user` opens a confirm; with it empty or unmeasured, 0 steers apply and each is a refused record.
Verdict: KEEP. Renamed from harness-gh-user.

### 1.3 Review and merge

#### MS-020 Conflicting pull requests listed
As a human (Tig today), I want ready pull requests in merge conflict listed with their author seat, so that each becomes a send-back.
Evidence: [factory harness attention.py line 136, the merge-conflict finding](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/attention.py#L136).
Acceptance: one row per conflicting ready pull request with `owner/repo#N` and the author seat, linked.
Verdict: CHANGE: shown on the review surface ([MS-128, review surface lists ready pulls](#ms-128-review-surface-lists-ready-pulls)), routed as a send-back ([decision 5, conflicts are changes, not verbs](mike.md#11-decisions)).

#### MS-021 Reviewer links its pull request
As a human (Tig today), I want a reviewer whose assignment is a pull request to link to that pull request, so that I open the review in one click.
Evidence: [factory harness api.py line 2024, the pull request assignment link](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/api.py#L2024).
Acceptance: the assignment URL ends in `/pull/N` when the item is a pull request.
Verdict: KEEP.

#### MS-022 Point a reviewer at a pull request
As a human (Tig today), I want to point a reviewer at a pull request by typing it as the reviewer's assignment with a steer, so that a review starts now.
Evidence: [factory dashboard verbs.mjs line 109, the reviewer assignment](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/verbs.mjs#L109).
Acceptance: the reviewer row shows `#N` on the next sessions frame; the steer is refused when the reviewer wrote the pull request or has another without a verdict.
Verdict: CHANGE: reviewer independence and one-pull-request-per-reviewer are gates ([gate 9, reviewer independence](mike.md#33-gates-mike-enforces-for-every-caller), [mike.md §3.6, how reviewers operate](mike.md#36-how-reviewers-operate)).

### 1.4 Manage seats

#### MS-023 Mint a seat with no session
As a human (Tig today), I want to mint a seat that has no session, wait-only, optionally with an assignment its first steer carries, so that I bring it into being.
Evidence: [factory dashboard verbs.mjs line 62, the mint verb](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/verbs.mjs#L62); [Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands).
Acceptance: enabled only when every selected row lists mint; one decision record per seat before the vendor call; the new session reads its brief and waits ([mike.md §3.2, mint, remint, steer](mike.md#32-mint-remint-steer)).
Verdict: KEEP.

#### MS-024 Restart a stuck seat
As a human (Tig today), I want to restart a seat after one confirm, keeping its assignment, so that I replace a stuck session.
Evidence: [factory dashboard verbs.mjs line 63, the restart verb](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/verbs.mjs#L63); [Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands).
Acceptance: body carries `confirm:"restart"`; the label is unchanged afterwards; one restart record exists.
Verdict: KEEP.

#### MS-025 Archive any seat's session
As a human (Tig today), I want to archive any seat's session after one confirm, keeping the name, so that I end it on any runtime.
Evidence: [factory dashboard verbs.mjs line 65, the archive verb](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/verbs.mjs#L65).
Acceptance: for each configured runtime, archive leaves liveness `not-minted` on the next frame and one archive record.
Verdict: CHANGE: factory archives cursor-cloud and claude-tmux only; Mike archives every runtime ([mike.md §4, runtimes](mike.md#4-runtimes)).

#### MS-026 One verb on checked rows
As a human (Tig today), I want to check rows, or all rows, and run one verb on all of them, so that I act on a group.
Evidence: [factory dashboard app.js line 1562, the row checkboxes](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L1562); [Mike dashboard API §7, payload shapes](mike-dashboard-api.md#7-payload-shapes).
Acceptance: the bar reads "N seats selected"; a verb is enabled only if every checked row lists it.
Verdict: KEEP.

#### MS-027 Verb buttons explain themselves
As a human (Tig today), I want each verb button to say what it does and why it is off, in the server's words, so that I do not guess and the page cannot drift.
Evidence: [factory dashboard verbs.mjs line 71, the verb hover text](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/verbs.mjs#L71); [Mike dashboard API §7, payload shapes](mike-dashboard-api.md#7-payload-shapes).
Acceptance: 0 why-off strings in the page source; each tooltip equals the server's field for that row and verb.
Verdict: CHANGE: factory's `verbReason` re-derives the rule in prose and already disagrees with the server ([mike.md §10 item 21, dashboard patches](mike.md#10-what-mike-does-not-re-create)); Mike's server sends `verb_why` per verb on each `seatRow` ([Mike dashboard API §7, payload shapes](mike-dashboard-api.md#7-payload-shapes)).

#### MS-028 Verbs offered by the control plane
As a human (Tig today), I want verbs offered only when the control plane lists them for the row, so that I cannot mint over a responding seat: one session per seat name.
Evidence: [factory dashboard verbs.mjs line 35, the row verb list check](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/verbs.mjs#L35); [Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands).
Acceptance: no button is enabled for a verb a selected row's `verbs` lacks; the server refuses the verb anyway with a record; a responding or unmeasured row never lists mint ([gate 7, one session per seat name](mike.md#33-gates-mike-enforces-for-every-caller)).
Verdict: KEEP.

#### MS-029 Commands shown as notifications
As a human (Tig today), I want each command I send shown as a notification that moves from sent to done, started or refused with the why, so that I know what happened without reading logs.
Evidence: [factory dashboard rules.mjs line 1032, the command notifications](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L1032); [Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands).
Acceptance: a notification appears at click time carrying the job id ([MS-137, job ids for every command](#ms-137-job-ids-for-every-command)) and is updated by the answer; an identical pending command is not re-sent.
Verdict: CHANGE: keyed by job id from the 202 and updated from the `jobs` part, not by a 30-second wait ([Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands)).

#### MS-030 Change a role's vendor and model
As a human (Tig today), I want to change a role's vendor, runtime and model and choose remint now, when idle, or at the next reboot, so that I control when the money is spent.
Evidence: [factory dashboard app.js line 1034, the role vendor editor](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L1034).
Acceptance: the dialog lists exactly the seats of that role; only those seats remint; each keeps its old values until its trigger; the pending rows are written before the settings version.
Verdict: CHANGE: the field is `runtime`, not `harness` ([decision 7, the field is runtime](mike.md#11-decisions)).

#### MS-031 Pick each vendor's billing account
As a human (Tig today), I want to pick which account each vendor bills, by secret name, so that a seat runs on the right subscription.
Evidence: [factory harness settings.py line 554, the vendor account setting](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/settings.py#L554).
Acceptance: one picker per vendor; with no account named it is disabled and reads "unmeasured: <reason>"; no value of a secret reaches the page.
Verdict: CHANGE: per vendor from config, not four fixed harness rows.

#### MS-032 Lane-PE mints need my word
As a human (Tig today), I want a lane-PE minted by me or by the loop only when that role's fill-missing setting is on, and turning it on to ask me first, so that an expensive seat is never spawned without my word.
Evidence: [factory brief factory-pe.md line 13, the lane-PE mint rule](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/briefs/factory-pe.md#L13).
Acceptance: with the setting off, a week of ticks, Hard Reboot and Arthur's verbs mint 0 lane-PE seats; turning it on shows the confirm naming the mints and the spend; a seat-token mint of a lane-PE is a refused record; every lane-PE mint is wait-only.
Verdict: CHANGE: the setting stays, off by default, human-only, with the confirm ([mike.md §2, roles](mike.md#2-roles), [decision 12, Mike may mint lane-PEs](mike.md#11-decisions)).

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

### 1.5 Configure

#### MS-035 One Running or Paused switch
As a human (Tig today), I want one Running/Paused switch for the loop that acts on click, so that I can stop all automated action at once.
Evidence: [factory dashboard app.js line 956, the Running/Paused switch](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L956); [Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands).
Acceptance: while Paused a tick records 0 seat actions; a repeat click's job is applied with why `already Paused`.
Verdict: CHANGE: Running or Paused is a setting key written by `POST settings`, its answer a job ([Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands)).

#### MS-036 Live or dry-run loop mode
As a human (Tig today), I want loop mode live or dry-run, with a confirm only when going live, so that dry-run is safe and live is deliberate.
Evidence: [factory dashboard rules.mjs line 1543, the loop mode confirm](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L1543); [Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands).
Acceptance: switching to live opens a confirm, to dry-run does not; in dry-run every verb writes a record and sends 0 bytes to any vendor or GitHub.
Verdict: KEEP.

#### MS-037 Loop cadence from 1 to 60 minutes
As a human (Tig today), I want the loop cadence settable from 1 to 60 minutes, so that I trade responsiveness for cost.
Evidence: [factory harness settings.py line 409, the cadence setting](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/settings.py#L409); [Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands).
Acceptance: 0 and 61 are refused by the server; a non-integer is refused on the page.
Verdict: KEEP.

#### MS-038 Settings show source and actor
As a human (Tig today), I want every setting shown with its value, where it came from, and who changed it last and when, so that I can trust and audit settings.
Evidence: [factory dashboard app.js line 1141, the settings table](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L1141); [Mike dashboard API §7, payload shapes](mike-dashboard-api.md#7-payload-shapes).
Acceptance: 4 columns: Setting, Value, From (`default`, `instance`, `store` or `unmeasured`), Changed by (login and ISO 8601 time).
Verdict: CHANGE: `settingRow` carries `source`, `changed_by` as a login (not an email header) and `changed_at` ([Mike dashboard API §7, payload shapes](mike-dashboard-api.md#7-payload-shapes)).

#### MS-039 Schema check before save
As a human (Tig today), I want a value checked against the store's schema before it saves, so that a typo fails on the page and not in the loop.
Evidence: [factory dashboard rules.mjs line 1517, the schema check](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L1517); [Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands).
Acceptance: invalid input shows "<label> must be <type>" and writes no version; the page and the server use one schema file.
Verdict: KEEP.

#### MS-040 Copyable View Settings dump
As a human (Tig today), I want a View Settings dump of every effective value with its source that I can copy, so that I can paste the config into an issue.
Evidence: [factory dashboard app.js line 892, View Settings](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L892); [Mike dashboard API §5, reads](mike-dashboard-api.md#5-reads).
Acceptance: JSON with `{value, source}` per key; a secret appears by name only; Copy says "Copied."
Verdict: KEEP.

#### MS-041 Typing survives live frames
As a human (Tig today), I want what I am typing kept when a frame arrives, so that live updates do not eat my edit.
Evidence: [factory dashboard app.js line 1202, the per-frame redraw](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L1202).
Acceptance: a field with unsaved text keeps its text and focus across 10 consecutive frames.
Verdict: CHANGE: the page patches changed rows instead of rebuilding the tab per frame ([mike.md §10 item 21, dashboard patches](mike.md#10-what-mike-does-not-re-create)).

#### MS-042 Unreadable config store said
As a human (Tig today), I want the page to say when the config store cannot be read, so that I know nothing is steered.
Evidence: [factory dashboard app.js line 1170, the store unreadable banner](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L1170).
Acceptance: the lead line reads "The config store is unmeasured: <reason>. Nothing is steered until it reads." and the loop records 0 steers.
Verdict: KEEP.

#### MS-043 Every tunable read each tick
As the loop, I want every tunable read from the config store each tick, so that a tune needs no pull request.
Evidence: [factory harness settings.py line 445, the tunable settings](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/settings.py#L445).
Acceptance: a save writes one version and one log line; the next tick's records cite the new version.
Verdict: CHANGE: the key set shrinks to Mike's (loop window, read reserve, fill-missing cap, shares, mint thresholds); paste, pe-retarget, main-restart lists and redelivery keys go.

### 1.6 Diagnose and health

#### MS-044 Health first with snapshot age
As a human (Tig today), I want Health as the first tab with the snapshot age ticking, so that I see at a glance whether the data is fresh.
Evidence: [factory dashboard app.js line 606, the Health tab](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L606); [Mike dashboard API §7, payload shapes](mike-dashboard-api.md#7-payload-shapes).
Acceptance: "updated Ns ago" changes every second from the ISO `snapshot_at`; with none it reads "update time not recorded".
Verdict: CHANGE: the field is `snapshot_at` on the `health` part ([Mike dashboard API §7, payload shapes](mike-dashboard-api.md#7-payload-shapes)).

#### MS-045 Needs attention groups faults
As a human (Tig today), I want a Needs attention block that groups every fault by kind, worst first, with counts and links, so that I triage in one read.
Evidence: [factory dashboard app.js line 640, the Needs attention block](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L640); [Mike dashboard API §7, payload shapes](mike-dashboard-api.md#7-payload-shapes).
Acceptance: the summary reads "N not ok, M unmeasured" or "Nothing needs attention."; not-ok groups precede unmeasured.
Verdict: KEEP.

#### MS-046 Loop heartbeat and timer rows
As a human (Tig today), I want loop rows for heartbeat, mode, Running/Paused and timer, with the heartbeat stamped only by the loop, so that a stopped loop never reads as a Paused or healthy one.
Evidence: [factory dashboard rules.mjs line 635, the loop rows](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L635); [Mike dashboard API §7, payload shapes](mike-dashboard-api.md#7-payload-shapes).
Acceptance: a hand run of a verb leaves the heartbeat unchanged; timer not active is marked fault; Paused is marked paused.
Verdict: CHANGE: no row for a poke heartbeat or a tick verb list; one loop, one heartbeat.

#### MS-047 Header names a stopped loop
As a human (Tig today), I want the header to read "Loop Paused: <reason>" or "Loop timer not active" on every tab, so that I never miss a stopped loop.
Evidence: [factory dashboard rules.mjs line 969, the header loop status](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L969).
Acceptance: the line is on all tabs while Paused and absent while Running with the timer active.
Verdict: KEEP.

#### MS-048 Hosts table shows host health
As a human (Tig today), I want a Hosts table with reachability, seat count, check-in age, checkout commit and pending actuations, so that I see which seat host is down.
Evidence: [factory dashboard rules.mjs line 775, the Hosts table](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L775); [Mike dashboard API §7, payload shapes](mike-dashboard-api.md#7-payload-shapes).
Acceptance: a host with a stale check-in is red with a note row; a host with 0 seats that never checked in is not in the payload.
Verdict: CHANGE: the server omits never-used hosts; the page filters nothing ([mike.md §10 item 21, dashboard patches](mike.md#10-what-mike-does-not-re-create)).

#### MS-049 Served commit and checkout lag
As a human (Tig today), I want the commit this control plane serves and how far the loop checkout is behind `main`, linked, so that I know whether a merge is live.
Evidence: [factory dashboard rules.mjs line 577, the served commit row](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L577); [Mike dashboard API §7, payload shapes](mike-dashboard-api.md#7-payload-shapes).
Acceptance: "serving <branch · sha8>, started <ISO time>"; the loop checkout item says "N behind".
Verdict: KEEP.

#### MS-050 Unconfirmed steers counted per seat
As a human (Tig today), I want steers not confirmed counted per seat with a link to the matching log lines, so that I see lost deliveries.
Evidence: [factory harness attention.py line 271, the steers not confirmed finding](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/attention.py#L271).
Acceptance: the count equals the not-confirmed steer records in the window, for every runtime; "Show in log" opens a log view with exactly those lines.
Verdict: CHANGE: one delivery result for every runtime, not tmux pastes only.

#### MS-051 Mint anomaly named
As a human (Tig today), I want a mint anomaly named from the mint records, so that runaway minting is visible.
Evidence: [factory harness attention.py line 119, the mint anomaly finding](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/attention.py#L119).
Acceptance: Health shows "no seat minted twice for one issue" as ok or names each seat and issue; a vendor session with no mint record is one red item.
Verdict: CHANGE: one check over mint records replaces six detectors for past defects ([mike.md §10 item 21, dashboard patches](mike.md#10-what-mike-does-not-re-create)).

#### MS-052 Platform faults named
As a human (Tig today), I want platform faults named (GitHub read budget, vendor account, store not writable, another loop on this store, runtime launcher missing on a seat host, process and tree disagree), so that I fix the platform before the fleet.
Evidence: [factory harness attention.py line 212, the platform faults](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/attention.py#L212).
Acceptance: each fault appears as its own labelled group when not ok and clears on the next snapshot after the fault clears.
Verdict: CHANGE: the account check is per vendor, not Cursor only.

#### MS-053 Refusal streaks named
As a human (Tig today), I want a verb that refused N times in a row named, with each refusal's reason in its record, so that a broken verb shows and one cause is not buried under hundreds of rows.
Evidence: [factory harness api.py line 606, the refusal streak](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/api.py#L606).
Acceptance: "<verb> refusing (N in a row): <why>" appears at the threshold inside the window; a later applied record clears it.
Verdict: CHANGE: refusal streaks only; Mike has no holds ([mike.md §10 item 1, the steer-idle planner](mike.md#10-what-mike-does-not-re-create)).

#### MS-054 Four distinct connection failures
As a human (Tig today), I want signed out, not allowed, unreachable and wrong version each said differently, so that a refusal never looks like a dead control plane.
Evidence: [factory dashboard client.mjs line 108, the connection error states](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/client.mjs#L108); [Mike dashboard API §3, version](mike-dashboard-api.md#3-version), [Mike dashboard API §4, the stream](mike-dashboard-api.md#4-the-stream).
Acceptance: four distinct texts; 401 and 403 do not retry; other failures retry every 3 s.
Verdict: KEEP.

#### MS-055 Live stream recovers itself
As a human (Tig today), I want the live stream to recover by itself after sleep, a proxy drop or a control plane restart, so that an open tab stays true.
Evidence: [factory dashboard client.mjs line 280, the stream reconnect](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/client.mjs#L280); [Mike dashboard API §4, the stream](mike-dashboard-api.md#4-the-stream).
Acceptance: 45 s with no bytes, or a return to the tab, opens a new stream that resends every opening frame.
Verdict: KEEP.

#### MS-056 Health from the tick snapshot
As a human (Tig today), I want Health built from a snapshot the tick wrote, and a stale snapshot said on open pages, so that polling the page costs nothing and silence never reads as healthy.
Evidence: [factory harness api.py line 3995, the Health snapshot read](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/api.py#L3995); [Mike dashboard API §4, the stream](mike-dashboard-api.md#4-the-stream).
Acceptance: a Health request makes 0 vendor and 0 GitHub calls (test); within one keep-alive after the loop window passes, one `health` frame has `stale` true and the item "health snapshot stale", even with a log frame in the same pass.
Verdict: CHANGE: the stale signal is `stale` true on one `health` frame per stale period ([Mike dashboard API §4, the stream](mike-dashboard-api.md#4-the-stream)).

#### MS-057 Watch and drive a tmux pane
As a human (Tig today), I want to watch a tmux seat's pane in the browser and take control to type, one human at a time, so that I can unstick it without SSH.
Evidence: [factory dashboard app.js line 2451, the browser terminal](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L2451).
Acceptance: view mode sends 0 keys; keys reach the pane only after Take control; the seat host defers steers and restarts while a human has control and runs each once after.
Verdict: CHANGE: deferred from API 1.0.0; served by the seat host over a two-way channel and added later as a minor bump ([Mike dashboard API §8, what changed and the terminal deferral](mike-dashboard-api.md#8-what-changed-from-the-starting-point)).

### 1.7 Audit records

#### MS-058 Filterable log in the URL
As a human (Tig today), I want the log under Health, filterable by level and up, component, seat, command, project and text, with the filter in the URL, so that I can share or reload a filtered view.
Evidence: [factory dashboard app.js line 1767, the log filters](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L1767); [Mike dashboard API §5, reads](mike-dashboard-api.md#5-reads).
Acceptance: the URL carries `log_*` keys; Back and Forward restore the filter; Clear empties every field.
Verdict: CHANGE: adds a project filter ([mike.md §1.2, multi-repository, one instance](mike.md#12-multi-repository-one-instance)).

#### MS-059 Since view reads whole window
As a human (Tig today), I want a "since" log view that reads the whole window up to 2000 rows, so that a count on Health matches the lines I see.
Evidence: [factory dashboard rules.mjs line 1151, the since log view](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L1151); [Mike dashboard API §5, reads](mike-dashboard-api.md#5-reads).
Acceptance: a since query sends `limit=2000`; rereads come at most every 30 s, one in flight.
Verdict: KEEP.

#### MS-060 Every command recorded with identity
As a human (Tig today), I want every dashboard command recorded with my identity and its outcome, so that I can audit who did what.
Evidence: [factory harness api.py line 4717, the command record](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/api.py#L4717); [Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands).
Acceptance: one record per command, pending then applied, refused or cancelled, with `actor` and the job id.
Verdict: KEEP.

#### MS-061 Settings history by version
As a human (Tig today), I want every settings change stored as a new version with actor, and a history I can list, so that "who changed what" needs no pull request.
Evidence: [factory harness api.py line 5131, the settings versions](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/api.py#L5131); [Mike dashboard API §5, reads](mike-dashboard-api.md#5-reads).
Acceptance: the answer says "saved as version N"; one log line names key, actor, from and to; `settings history` lists every version.
Verdict: KEEP.

### 1.8 Install and recover

#### MS-062 Hard Reboot the fleet
As a human (Tig today), I want Hard Reboot (archive and remint every seat, restart the control plane), optionally with Reset Defaults, so that I can start the fleet clean.
Evidence: [factory dashboard rules.mjs line 1290, Hard Reboot](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L1290); [Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands).
Acceptance: one confirm (`confirm` equals the mode); the record names a human actor; after `reset-defaults` every seat ends idle and 0 `seat:` labels remain, written as one record; a seat token is refused.
Verdict: CHANGE: Reset Defaults is its own fleet mode `reset-defaults`, run as a separate job beside `hard-reboot` ([Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands)).

#### MS-063 Orchestrator Reboot starts fresh
As Arthur (arbiter), I want an Orchestrator Reboot to archive and remint K and me with idle assignments, so that a confused orchestrator starts fresh.
Evidence: [factory dashboard rules.mjs line 1291, Orchestrator Reboot](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L1291); [Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands).
Acceptance: only the `arbiter` and `tpm` role seats are reminted; both read idle afterwards.
Verdict: KEEP.

#### MS-064 Fill-Missing closes gaps
As a human (Tig today), I want Fill-Missing to adopt or mint every absent pool seat and leave live ones alone, capped per window, so that gaps close in one click.
Evidence: [factory dashboard rules.mjs line 1293, Fill-Missing](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L1293); [Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands).
Acceptance: 0 responding or unmeasured seats are reminted ([gate 7, one session per seat name](mike.md#33-gates-mike-enforces-for-every-caller)); at most `max_creates` per seat per `window_minutes`; the confirm states the mint count and the vendor each bills.
Verdict: CHANGE: adopt, not claim; never a lane-PE; the cost line comes from vendor config, not fixed text.

#### MS-065 Fleet commands never collide
As a human (Tig today), I want a running fleet command shown as progress, and the server to refuse any command that collides with it, so that two commands cannot collide.
Evidence: [factory dashboard rules.mjs line 1005, the fleet command progress](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L1005); [Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands).
Acceptance: "<mode>: step N of M, started by <actor>" shows to every viewer; the server answers 409 to a colliding seat verb or fleet mode.
Verdict: CHANGE: factory's seat verbs have no server busy check, only a client lock ([mike.md §10 item 21, dashboard patches](mike.md#10-what-mike-does-not-re-create)).

#### MS-066 Restart the control plane
As a human (Tig today), I want to restart the control plane process from the page, even while Paused, so that I recover a stuck API without SSH.
Evidence: [factory dashboard rules.mjs line 1294, the control plane restart](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L1294); [Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands).
Acceptance: one confirm; the stream reconnects in under 10 s; 0 seats reminted.
Verdict: KEEP.

### 1.9 Identity and secrets

#### MS-067 Microsoft sign-in renews silently
As a human (Tig today), I want to sign in with Microsoft, renew silently, and be told when a renewal needs me, so that a long session does not just die.
Evidence: [factory dashboard client.mjs line 158, the sign-in renewal](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/client.mjs#L158); [Mike dashboard API §2, identity](mike-dashboard-api.md#2-identity).
Acceptance: a silent renewal shows "Your sign-in renewed silently." for 10 s; an interactive need redirects with a notice.
Verdict: CHANGE: identity provider, base path and origins are instance config ([mike.md §7, the dashboard](mike.md#7-the-dashboard), [tig/mike#1, the dashboard rewrite](https://github.com/tig/mike/issues/1)).

### 1.10 Cost

#### MS-068 Tokens per seat and fleet
As a human (Tig today), I want tokens per seat since its last mint and a fleet total that never counts unmeasured as zero, so that I see spend.
Evidence: [factory dashboard app.js line 530, the token columns](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L530); [Mike dashboard API §7, payload shapes](mike-dashboard-api.md#7-payload-shapes).
Acceptance: the total reads "incomplete" with an unmeasured count when any seat is unmeasured; each bar is that seat's percent of the measured total.
Verdict: KEEP.

#### MS-069 Context fullness per seat
As a human (Tig today), I want each seat's context fullness, fullest first, so that I can remint a seat before it summarizes.
Evidence: [factory dashboard rules.mjs line 414, the context fullness column](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L414); [Mike dashboard API §7, payload shapes](mike-dashboard-api.md#7-payload-shapes).
Acceptance: measured seats sorted by percent descending; "summarized" marked; unmeasured seats last with their reason.
Verdict: KEEP.

#### MS-070 Vendor included pools shown
As a human (Tig today), I want each vendor's included pools with percent used, age and overage, so that I know when we start paying more.
Evidence: [factory dashboard app.js line 363, the included pools gauges](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L363); [Mike dashboard API §7, payload shapes](mike-dashboard-api.md#7-payload-shapes).
Acceptance: one row per configured pool reading "N% used, <age>" or "unmeasured, <reason>"; a pool with no gauge source is named as not shown.
Verdict: CHANGE: pools come from vendor config, not two fixed Cursor names and a code tuple.

## 2. Operator, loop and seat stories

### 2.1 Observe the fleet

#### MS-071 Talk to humans by measurement
As a seat (any), I want to talk to a human by measurement, bad news first, with one recommendation, ordered decisions then merges then next, and cost unasked, so that a human reads one message and acts.
Evidence: [factory AGENTS.md line 84, talking to humans](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/AGENTS.md#L84).
Acceptance: each loaded brief contains the five rules (test); a report with a cost has a number and a unit.
Verdict: KEEP.

#### MS-072 Focus stored in detail
As a seat (any), I want my reported focus and check-in stored in the record's `detail`, never its `why`, so that the Seats tab shows focus without hiding a refusal reason.
Evidence: [factory harness __main__.py line 3024, the check-in detail field](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L3024).
Acceptance: `detail.focus` and `detail.checked_in` written, `detail.present_keys` holds names only; `why` unchanged.
Verdict: KEEP.

### 2.2 Steer and assign

#### MS-073 Record every steer first
As Arthur (arbiter), I want every steer recorded before it is sent, and apply to refuse an unrecorded decision, so that no steer exists without a trail.
Evidence: [factory harness __main__.py line 748, the record-before-act steer](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L748).
Acceptance: for 100% of steers the record's write time precedes the send; apply with no record id is refused.
Verdict: KEEP.

#### MS-074 No worker steer onto urgency:no
As a human (Tig today), I want any worker steer onto an `urgency:no` issue, or one with no urgency label, refused for every caller, so that spare capacity is never spent on work nobody marked urgent.
Evidence: [factory harness severity_floor.py line 1, the severity floor](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/severity_floor.py#L1).
Acceptance: the refusal reads `urgency floor: urgency:no is never steered` with a record; unreadable labels refuse as `unmeasured`; factory's Urgent, High, Medium and Low map to `critical`, `high`, `normal` and `no`.
Verdict: CHANGE: urgency is a label, `urgency:<level>`, not the GitHub Priority field, so a human sets it from the GitHub mobile app ([gate 4, the urgency floor](mike.md#33-gates-mike-enforces-for-every-caller), [mike.md §3.1, pool, assignment and share](mike.md#31-pool-assignment-share)).

#### MS-075 No action on unmeasured liveness
As the loop, I want no mint, steer or restart decided on a seat whose liveness is unmeasured, so that a blind read cannot plan work over running seats.
Evidence: [factory harness liveness.py line 1, the liveness module](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/liveness.py#L1).
Acceptance: with a seat `unmeasured`, 0 mints and 0 loop steers target it; each attempt is a refused record naming the reason.
Verdict: KEEP.

#### MS-076 Lane-PE files, workers code
As a lane-PE, I want to file an issue with an `urgency:<level>` label and a lane label and steer it to a worker instead of writing code, so that judgment stays separate from development.
Evidence: [factory brief factory-pe.md line 79, the lane-PE file-and-steer rule](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/briefs/factory-pe.md#L79).
Acceptance: 0 development pull requests authored by Arthur, K or lane-PE seats; `pr-check` names one as a finding; a `[none]` title prefix does not bypass it; each filed issue carries one `urgency:` label and one lane label.
Verdict: CHANGE: urgency is set as a label, not the Priority field ([mike.md §3.1, pool, assignment and share](mike.md#31-pool-assignment-share)).

#### MS-077 GitHub writes through Mike
As a seat (any), I want issue and pull-request writes through Mike's verbs, recorded first, through one GitHub module, so that no seat runs raw `gh` and no write comes from a read-only account.
Evidence: [factory harness gh.py line 1, the GitHub write module](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/gh.py#L1).
Acceptance: only one module spawns `gh` or calls the API (test); a write as the read-only account raises; a GraphQL mutation counts as a write.
Verdict: KEEP.

#### MS-078 Geas lints every prompt
As the loop, I want every outbound steer, poke and mint prompt linted by Geas against the banned-terms table before sending, so that a banned word never reaches a seat.
Evidence: [factory harness geas.py line 1, Geas](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/geas.py#L1).
Acceptance: a prompt with a banned term is refused with 0 bytes sent; the table comes from the project's hook, not from Mike.
Verdict: KEEP.

#### MS-079 Events routed to the owner seat
As the loop, I want a GitHub event on an issue or pull request routed to the seat its `seat:<name>` label names, so that the owner hears about a comment or review without polling.
Evidence: [factory harness poke.py line 525, the event routing](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/poke.py#L525).
Acceptance: a signed webhook delivery produces one prompt of the form `[<owner>] GitHub poke (<reason>): <title>` within one tick; an unsigned delivery is refused.
Verdict: CHANGE: signed webhook is the design; polling a human's notifications is a fallback ([mike.md §5, the control plane](mike.md#5-the-control-plane)).

#### MS-080 K nudges missing self-review
As K (TPM), I want to post one nudge when a ready pull request has no owner self-review on its head, so that the gate is met by the owner, not waived.
Evidence: [factory brief tpm.md line 55, K's self-review nudge](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/briefs/tpm.md#L55).
Acceptance: at most one nudge per pull request per head, in this shape:
```
[K (TPM)] <owner seat>, owner self-review is missing on <sha>.
```
Verdict: CHANGE: the name is the instance's TPM name; the sha is named.

#### MS-081 K follows up idle lane-PEs
As K (TPM), I want to send a follow-up once per idle stretch to a lane-PE idle past 30 minutes, with the measured idle time, 1 to 3 open items, and a reminder to use a cheaper model for grunt work, so that a stalled lane-PE moves without a human.
Evidence: [factory brief tpm.md line 57, K's idle follow-up](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/briefs/tpm.md#L57).
Acceptance: 0 or 1 follow-ups per lane-PE per idle stretch; each names idle minutes and a last-activity ISO time.
Verdict: CHANGE: delivered as a follow-up steer through Mike, gated like every steer.

### 2.3 Review and merge

#### MS-082 Draft early, ready when clean
As a worker (Artificer), I want to open my pull request as a draft early, labelled `seat:<name>`, and mark it ready only with a self-review done with my runtime's code-review tool and green CI on the same sha, so that other seats see which files I hold.
Evidence: [factory AGENTS.md line 105, the draft-early rule](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/AGENTS.md#L105).
Acceptance: `pull create` opens a draft by default; `pull ready` is refused unless self-review and CI name the current head.
Verdict: KEEP.

#### MS-083 Self-review in one shape
As a worker (Artificer), I want my self-review counted only in this exact shape, written by me, naming the head sha, so that a review of an old commit or prose about a review never passes the gate.
Evidence: [factory harness pr_state.py line 41, the self-review parser](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/pr_state.py#L41).
Acceptance: the gate matches `^\s*(\[[^\]\n]+\]\s*)?Self-Review:\s*Done\b`, finds the head sha (7 to 40 hex) in the comment, and the `[Name]` prefix equals the `seat:` owner; anything else does not count.
```
[Name] Self-Review: Done
Head: <sha>
```
Verdict: CHANGE: the old four-line form (`Lexicon: Clear.` and the rest) is refused by the gate, not only banned in briefs; the review behind it is the runtime's code-review tool ([MS-176, self-review with the runtime's code-review tool](#ms-176-self-review-with-the-runtimes-code-review-tool)).

#### MS-084 pr-check names rule breaks
As a worker (Artificer), I want `pr-check` to name mechanical rule breaks (one `seat:` label naming a real seat, no `[Name]` or `Name:` title, `Closes` in the same project, no development pull request from an orchestrator or lane-PE), so that review time is not spent on them.
Evidence: [factory harness __main__.py line 2149, the pr-check verb](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L2149).
Acceptance: `--strict` exits 1 on any finding; a cross-repository `Closes` is a finding.
Verdict: KEEP.

#### MS-085 One independent reviewer each
As the loop, I want each ready pull request given one reviewer, urgency first then oldest ready, never its author and never a reviewer already holding a pull request without a verdict, so that every ready pull request gets an independent review in parallel.
Evidence: [factory harness review.py line 123, the reviewer assignment](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/review.py#L123).
Acceptance: two ready pull requests and three idle reviewers give exactly two steers; with one reviewer idle, a `critical` pull request is steered before an older `normal` one; mergeable `UNKNOWN` read twice is `unmeasured` naming the pull request.
Verdict: CHANGE: urgency orders review before age; no reviewer waits behind a busy one ([factory#1759, reviewer queued behind a busy one](https://github.com/excaliwire/factory/issues/1759)); Arthur may order it, Mike enforces independence ([mike.md §3.4, review and send-back](mike.md#34-review-and-send-back), [mike.md §3.6, how reviewers operate](mike.md#36-how-reviewers-operate)).

#### MS-086 Review pinned to the head
As a reviewer (Warden), I want `review <pr>` to print one results table naming the head and refuse when the head moved or a read failed, so that my review is of this commit only.
Evidence: [factory harness review.py line 96, the review verb](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/review.py#L96).
Acceptance: the table contains `| head | <sha> |`; a review without that table for the head does not clear the gate.
Verdict: KEEP.

#### MS-087 Fails on main, passes on head
As a reviewer (Warden), I want new tests copied onto a `main` worktree and run there and on the head, so that "fails on main, passes on head" is measured for code, config, schema and briefs.
Evidence: [factory brief reviewer.md line 17, the main worktree test rule](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/briefs/reviewer.md#L17).
Acceptance: the table has one main result and one head result per new test; a behavior finding without a failing test is not blocking.
Verdict: KEEP.

#### MS-088 Review in one fixed shape
As a reviewer (Warden), I want my review in one fixed shape of at most 12 lines, so that a human reads it on a phone and the gate parses it.
Evidence: [factory brief reviewer.md line 27, the review shape](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/briefs/reviewer.md#L27).
Acceptance: line 1 matches the verdict pattern with a head sha; verdict is `Merge`, `Send back` or `Hold`; one line per blocking finding as `file:line, what is wrong, the fix`; one `Ran:` line; at most 12 lines outside `<details>`; non-blocking findings become issues, not comment text.
```
[Name] Recommendation: Send back on 1a2b3c4.
tools/board.py:42: skips the last row. Fix: iterate to n.
Ran: `review 1741`: new test fails on main, passes on head.
<details><summary>Review results</summary>

(the verb's table)

</details>
Next: <Seat> fixes tools/board.py:42.
```
Verdict: KEEP.

#### MS-089 Comments end with next steps
As a seat (any), I want every comment to end with its next steps, one line each, each naming who does it, so that nobody has to infer the hand-off.
Evidence: [factory brief psde.md line 34, the Next line rule](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/briefs/psde.md#L34).
Acceptance: the last non-blank lines of every seat comment match `^Next: \S+ .+\.$`, and no non-`Next:` line follows them (test on a sample of 50 comments).
```
Next: <Seat> <does X>.
```
Verdict: KEEP.

#### MS-090 Comment length caps
As a human (Tig today), I want seat comments capped at 12 lines for a review, 20 for a pull request body, and 6 for any other comment, so that I read the fleet on a phone.
Evidence: [factory AGENTS.md line 104, the comment limits](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/AGENTS.md#L104).
Acceptance: each loaded brief states the three limits (test); a pull request body has change, `Fixes #N` or `Advances #N`, test-first in one line, verdicts, merge order, follow-ups, and at most 20 lines.
Verdict: KEEP.

#### MS-091 Reviewers cannot push
As a reviewer (Warden), I want to be unable to push a fix or open a development pull request, so that review stays independent.
Evidence: [factory brief reviewer.md line 23, the reviewer no-push rule](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/briefs/reviewer.md#L23).
Acceptance: 0 commits by a reviewer seat on a development path; a bug a reviewer finds becomes 1 issue with an `urgency:` label and a steer to a worker.
Verdict: CHANGE: a push by a reviewer seat token is refused by mechanism, not only by the brief ([gate 9, reviewer independence](mike.md#33-gates-mike-enforces-for-every-caller), [mike.md §3.6, how reviewers operate](mike.md#36-how-reviewers-operate)).

#### MS-092 Gates pinned to head sha
As a human (Tig today), I want every gate pinned to the head sha, so that a new commit voids self-review, CI and review.
Evidence: [factory harness merge_gate.py line 1, the merge gate](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/merge_gate.py#L1).
Acceptance: pushing one commit after a `Merge` review moves the pull request's next step back to self-review within one tick.
Verdict: KEEP.

#### MS-093 Send-back returns to author
As a worker (Artificer), I want a send-back from any independent reviewer (a seat, an attached session or a human) to return my pull request to draft and come back to me as my next assignment, so that the fix lands on the seat that has the context and nobody else waits.
Evidence: [factory harness draft_sent_back.py line 1, draft on send-back](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/draft_sent_back.py#L1).
Acceptance: after `Send back` on the head from a reviewer seat, an attached session or a listed human, the pull request is draft within one tick and the author seat's next assignment is that pull request; a send-back naming an older sha does nothing.
Verdict: CHANGE: send-back is a first-class state on the board, and no seat waits on it ([mike.md §3.4, review and send-back](mike.md#34-review-and-send-back)).

#### MS-094 Conflicts and Copilot threads sent back
As a worker (Artificer), I want a ready pull request that turns conflicting, or gets unresolved Copilot threads on its head, sent back to me once, so that I fix it without a human polling.
Evidence: [factory harness conflict_steer.py line 243, the conflict steer](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/conflict_steer.py#L243).
Acceptance: one send-back per pull request per head per cause; the prompt names the cause and says "Merge origin/main. Never rebase on a shared branch."
Verdict: CHANGE: kept as wakes until the planner is gone, then routed as send-backs ([decision 5, conflicts are changes, not verbs](mike.md#11-decisions)).

#### MS-095 Request merge when gates pass
As a human (Tig today), I want Mike to request merge from the configured merger exactly when self-review, CI, ready and an independent `Merge` review (seat, attached session or human) all name the same head, so that my assignment list is my merge queue.
Evidence: [factory harness assign_tig.py line 1, assign-tig](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/assign_tig.py#L1).
Acceptance: a draft never gets a request; a pull request already assigned to the merger is not re-requested; the merger login comes from config.
Verdict: CHANGE: request merge, not assign-tig.

#### MS-096 No merge verb
As a human (Tig today), I want Mike to have no merge verb, so that only a human merges.
Evidence: [factory harness merge_gate.py line 5, the no-merge rule](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/merge_gate.py#L5).
Acceptance: a test fails if any verb, route or GitHub call that merges is added.
Verdict: KEEP.

#### MS-097 Waive and grant by comment
As a human (Tig today), I want to waive a gate with a comment and grant a reviewer with a comment, honored only from my account, so that I unblock without editing code.
Evidence: [factory harness pr_state.py line 89, the waive and reviewer comments](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/pr_state.py#L89).
Acceptance: a waiver or grant from any seat is ignored and recorded; an unpinned waiver expires on the next commit; each honored waiver is a record.
```
waive: <self_review|ci|ready|ir|all> [sha]
reviewer: <Name>
```
Verdict: CHANGE: honored from the configured merger account, not a hard-coded `tig`.

### 2.4 Manage seats

#### MS-098 Remint keeps one agent per name
As Arthur (arbiter), I want a remint to archive the live session and mint one new session for the same name, and to refuse unknown or over-cap names, so that there is one session per seat name.
Evidence: [factory harness __main__.py line 1380, the remint verb](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L1380).
Acceptance: after a remint the vendor lists 1 live session for the name; a mint over a responding or unmeasured session is refused ([gate 7, one session per seat name](mike.md#33-gates-mike-enforces-for-every-caller)); a name beyond the pool cap is refused with a record.
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
Verdict: CHANGE: one template for every remint; the boards and report-and-wait lines go; "Unset severity is Low." becomes the urgency line ([mike.md §3.1, pool, assignment and share](mike.md#31-pool-assignment-share)).

#### MS-101 Pool converges without double mint
As the loop, I want the pool brought to its configured size without ever minting twice, so that the fleet converges without a human.
Evidence: [factory harness mint_standing.py line 1, the standing mint](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/mint_standing.py#L1).
Acceptance: a pending mint or a live session for a name gives 0 new mints; an unreadable vendor listing gives 0 mints and a refused record.
Verdict: CHANGE: the pool is a cap and a name list; a seat is killed only when stale or at the cap ([decision 11, the pool model](mike.md#11-decisions)).

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

### 2.5 Configure

#### MS-104 Seat host files from config
As a lane-PE, I want a seat host's runtime files rendered from instance config with a report of what differs, and an apply that fixes only that, so that a host is config-as-code.
Evidence: [factory agent-harness README.md line 179, the host render](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/README.md#L179).
Acceptance: report-only by default; apply writes nothing outside the configured root; a launch script without the generated-by marker is refused without `--force`.
Verdict: CHANGE: rendered from instance config, not `seats.yaml`; no ladder step check.

### 2.6 Diagnose and health

#### MS-105 One structured log
As a lane-PE, I want one structured log, rotated, secrets redacted, with every verb's start and end, so that I can rebuild a miss a week later.
Evidence: [factory harness harness_log.py line 1, the harness log](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/harness_log.py#L1).
Acceptance: every verb logs start and end with exit code and ms; a failure leaves a line even at exit 0; a scan of 7 days finds 0 secret values.
Verdict: CHANGE: the file is `mike.jsonl`; a new signal is a log line first ([mike.md §5, the control plane](mike.md#5-the-control-plane)).

#### MS-106 Written path to one cause
As a lane-PE, I want a written path from "it did not fire" to one cause, so that I answer it without reading code.
Evidence: [factory agent-harness README.md line 240, the did-not-fire guide](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/README.md#L240).
Acceptance: each branch (no event line, dry-run, `error=`, event id absent, gauge `unmeasured`) maps to exactly one cause.
Verdict: CHANGE: starts from the webhook event and the decision record, not the notification poll.

#### MS-107 Skip reads below budget reserve
As the loop, I want every GitHub-reading verb skipped for the tick when the read budget is below the reserve, so that polling cannot exhaust the token.
Evidence: [factory harness read_budget.py line 1, the read budget](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/read_budget.py#L1).
Acceptance: with remaining below `read_budget_reserve`, the tick records the number and makes 0 GitHub reads beyond the budget read.
Verdict: KEEP.

#### MS-108 Remints counted per seat
As a lane-PE, I want remints per seat counted between two times from the records, so that I can measure churn.
Evidence: [factory harness __main__.py line 705, the remint count](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L705).
Acceptance: the count writes nothing and equals the applied mint and remint records for that seat in the range.
Verdict: KEEP.

#### MS-109 Each loop-down reason named
As a human (Tig today), I want each reason the loop cannot run named as its own token, so that I never read healthy for a loop that does not run.
Evidence: [factory agent-harness README.md line 208, the loop health tokens](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/README.md#L208).
Acceptance: timer absent, timer inactive, another loop on the store, and checkout off branch each read as a distinct Health value; an unreadable scheduler reads `unmeasured`, never empty.
Verdict: CHANGE: one timer unit per instance and a store lock replace cron-line repair.

### 2.7 Install and recover

#### MS-110 One install command
As a human (Tig today), I want one command that installs the tool stack on Linux or Windows, so that a fresh machine reaches ready without a package list in my head.
Evidence: [factory agent-harness install.sh line 2, the install script](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/install.sh#L2).
Acceptance: the check exits 0 with every must-have present, exits 1 naming the installer to run; `--check-only` changes nothing.
Verdict: KEEP.

#### MS-111 Cloud setup installs the delta
As a seat host, I want a cloud setup script that installs only the delta over the vendor image and never fails the session, so that cloud seats boot with pinned tools.
Evidence: [factory agent-harness cloud-environment.sh line 2, the cloud setup script](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/cloud-environment.sh#L2).
Acceptance: exits 0 on every run in under 5 minutes; a second run on the same machine is a no-op.
Verdict: KEEP.

#### MS-112 One non-overlapping tick timer
As the loop, I want one timer that starts a tick 60 s after the last one finished and never overlaps it, so that two ticks never act at once.
Evidence: [factory agent-harness deploy/control-plane/hgl-control-loop.timer line 7, the tick timer](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/deploy/control-plane/hgl-control-loop.timer#L7).
Acceptance: over 24 hours, 0 tick start times fall inside another tick's run; one loop per instance.
Verdict: KEEP.

#### MS-113 Narrow-helper control plane deploy
As a human (Tig today), I want the control plane deployed from the instance's checkout and restarted by a narrow root helper, so that a deploy needs no shell on the control-plane host.
Evidence: [factory agent-harness deploy/control-plane/apply-unit.sh line 1, the apply-unit helper](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/deploy/control-plane/apply-unit.sh#L1).
Acceptance: the restart action neither fetches nor installs; the helper never starts or stops the loop timer.
Verdict: KEEP.

#### MS-114 End-to-end proof on a host
As a human (Tig today), I want an end-to-end proof on a real seat host for event routing, gauges and confirmed steer delivery, posted on the pull request before ready, so that a green contract test is not mistaken for a working host.
Evidence: [factory agent-harness e2e-box.md line 1, the end-to-end proof](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/e2e-box.md#L1).
Acceptance: stdout has one line per part, each a number, an id, or `unmeasured`; the pull request carries the output before ready.
Verdict: CHANGE: the retarget and ladder lines go; one delivery line per runtime comes in.

#### MS-115 Remint seats when main moves
As the loop, I want seats running code that a `main` move changed reminted, and all actuation stopped when the loop's own checkout lacks the fetched `main`, so that a broken fetch cannot steer live seats with old code.
Evidence: [factory harness main_restart.py line 1, main-restart](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/main_restart.py#L1).
Acceptance: a docs-only `main` move remints 0 seats; with the checkout behind, the tick records 0 seat actions and one refusal.
Verdict: CHANGE: the preserve and remint name lists go; what a seat runs is read from config.

#### MS-116 Restart control plane on drift
As the loop, I want the control plane restarted once, recorded first, when the commit it serves differs from the instance checkout, so that a merged fix reaches the API.
Evidence: [factory harness serve_restart.py line 1, serve-restart](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/serve_restart.py#L1).
Acceptance: the decision record precedes the restart; a missing unit or helper refuses by name; unreadable health is `unmeasured`.
Verdict: KEEP.

#### MS-117 Discard stale actuation backlog
As a lane-PE, I want a stale pending actuation backlog discarded without touching claimed ones, so that a returning seat host does not replay old steers.
Evidence: [factory harness __main__.py line 3196, the backlog discard](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L3196).
Acceptance: matching pending rows become refused with `why: stale-backlog`; claimed rows are unchanged.
Verdict: CHANGE: the store expires a pending actuation after a configured age as well, so a discard is rarely needed.

#### MS-118 Dismiss grok usage-limit dialogs
As a seat host, I want a vendor usage-limit dialog on a grok-tmux pane dismissed with that dialog's own key, so that a seat stuck on a modal resumes.
Evidence: [factory harness tmux.py line 188, the usage-limit dialog key](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/tmux.py#L188).
Acceptance: dismissed only when the heading and the `Shift+x:dismiss` footer are both on the pane; a sign-in prompt gets 0 keys; not retried.
Verdict: CHANGE: lives in the grok-tmux runtime driver under the Mike Runtime API, not in core ([mike.md §4, runtimes](mike.md#4-runtimes)).

#### MS-119 Reap expired branches
As the loop, I want expired reserved-prefix branches deleted, and a no-op run still recorded, so that throwaway branches do not pile up and silence does not mean "did not run".
Evidence: [factory harness reap.py line 1, the branch reaper](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/reap.py#L1).
Acceptance: a branch without the prefix or younger than `max_age_days` is untouched; each run writes one record.
Verdict: KEEP.

### 2.8 Identity and secrets

#### MS-120 Vendor keys stored safely
As a human (Tig today), I want a vendor key stored by hidden prompt, mode 600, and its account checked against config, so that a key is never in history and spend lands on the right account.
Evidence: [factory harness __main__.py line 2093, the hidden key prompt](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L2093).
Acceptance: file mode 600; the key is in no log, record or argv; a key on the wrong account is a Health fault and mint refuses.
Verdict: CHANGE: one check per vendor, not Cursor only.

#### MS-121 Secrets outside live state
As a lane-PE, I want secrets kept in a directory outside live state and referenced by name, so that wiping live state does not drop credentials.
Evidence: [factory agent-harness load-secrets.sh line 2, the secrets loader](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/load-secrets.sh#L2).
Acceptance: after deleting live state, the next verb finds its credentials; 0 secret values in logs, records or check-ins.
Verdict: CHANGE: the config store names each secret; no wrapper exports all of them into every verb's environment.

#### MS-122 No seat acts as a human
As a human (Tig today), I want no seat able to post, review, push or run GitHub calls as a human merger, and Arthur's GitHub token read-only, so that a waiver or approval in my name cannot be forged.
Evidence: [factory AGENTS.md line 59, the no-human-account rule](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/AGENTS.md#L59).
Acceptance: a write as the merger account from Mike raises; `waive:` is honored only from that account.
Verdict: KEEP.

#### MS-123 Host tokens name one host
As a seat host, I want a host token that names one host and a verified bearer on every pull, check-in and result, so that a compromised host can act only for itself.
Evidence: [factory harness __main__.py line 3387, the host token check](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L3387).
Acceptance: a check-in naming another host is refused; signature, iss, aud, tid, exp and nbf are all checked; the identity read lists roles with no secret.
Verdict: KEEP.

#### MS-124 Fixed writer, owner, addressee marks
As a seat (any), I want writer, owner and addressee carried by fixed marks, so that nobody is ambiguous across GitHub accounts.
Evidence: [factory AGENTS.md line 48, the address marks](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/AGENTS.md#L48).
Acceptance: gate parsers accept an optional `[Name] ` prefix and nothing else; `To: Name` at the start of the body (after the prefix, if any) is the address; 0 open titles carry a `[Name]` or `Name:` prefix; ownership reads only the label.
```
[Name] <text>              written by seat Name
To: Name. <text>           addressed to seat Name (a human writes this with no prefix)
[Name] To: Other. <text>   written by Name, addressed to Other
seat:<name>                label: the seat that owns this issue or pull request
```
Verdict: CHANGE: `To: Name` is the address, the email header word; factory's `Name:` form retires because it means the speaker in a transcript and the addressee on IRC ([mike.md §2.1, humans](mike.md#21-humans), [mike.md §9 rule 15, the address contract](mike.md#9-what-mike-keeps)).

### 2.9 Cost

#### MS-125 Gauges read unmeasured, not guessed
As the loop, I want every gauge to read `unmeasured` with a reason rather than a guessed percent, and a reading older than its stale window treated as `unmeasured`, so that no decision runs on stale or invented data.
Evidence: [factory harness write_meters.py line 1, the meter writer](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/write_meters.py#L1).
Acceptance: every absent source yields the literal `unmeasured` and a `why`; a `5% left` line parses to 95 used; text without a percent is `unparsed`.
Verdict: CHANGE: gauge sources are config; a vendor usage API is preferred over a screen scrape ([mike.md §10 item 19, screen-scraped meters](mike.md#10-what-mike-does-not-re-create)).

#### MS-126 Price spend before it runs
As a seat (any), I want to price a spend before it runs and report cost unasked, so that a human only says yes to money he can see.
Evidence: [factory AGENTS.md line 117, the cost rule](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/AGENTS.md#L117).
Acceptance: model-call spend under USD 100 needs no ask and is reported; any other spend, or over USD 100, waits for a yes; the price is a number from a measurement.
Verdict: KEEP.

#### MS-127 One pull request read per project
As the loop, I want one read of open pull requests and one of open issues per project per tick, with urgency and lane read from labels, so that a 60 s tick fits the GitHub rate limit.
Evidence: [factory agent-harness retarget-loop.sh line 64, the tick reads](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/retarget-loop.sh#L64).
Acceptance: GitHub reads per tick equal 1 pull-request page plus 1 issue page per project and 0 Priority field reads; a failed page is not reused.
Verdict: CHANGE: per project across the instance; urgency is a label, so the Priority field connection goes ([mike.md §3.1, pool, assignment and share](mike.md#31-pool-assignment-share)); webhook events cut the reads further.

## 3. Stories mike.md requires that neither source had

### 3.1 Review surface

#### MS-128 Review surface lists ready pulls
As a human (Tig today), I want a review surface listing every ready pull request, the reviewer assigned to each, and each verdict on the current head, so that I see review state without opening GitHub.
Evidence: [factory dashboard rules.mjs line 57, the router has no review route](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L57); [mike.md §7, the dashboard](mike.md#7-the-dashboard); [Mike dashboard API §7, payload shapes](mike-dashboard-api.md#7-payload-shapes).
Acceptance: the rows equal the open non-draft pull requests across all projects; each shows reviewer or `none`, and `Merge`, `Send back`, `Hold` or `pending` for the head sha.
Verdict: NEW.

#### MS-129 Review surface by urgency then age
As a human (Tig today), I want the review surface ordered by urgency, then by the time each pull request went ready, oldest first, with send-backs and their author seats listed apart, so that the most urgent, oldest wait is on top.
Evidence: [factory harness review.py line 123, the reviewer assignment](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/review.py#L123); [mike.md §3.4, review and send-back](mike.md#34-review-and-send-back); [Mike dashboard API §7, payload shapes](mike-dashboard-api.md#7-payload-shapes).
Acceptance: row order is `critical`, `high`, `normal`, `no`, then ascending ready time from GitHub events inside each; each send-back row names the author seat and its next-assignment state.
Verdict: NEW.

#### MS-130 Reviewer pool sized to workers
As the loop, I want the reviewer pool sized at `ceil(workers / 3)`, with one reviewer per ready pull request inside it, so that review keeps pace with work.
Evidence: [factory#1336 section 1 point 5, the harness redesign](https://github.com/excaliwire/factory/issues/1336); [decision 3, the reviewer pool cap](mike.md#11-decisions), [mike.md §3.6, how reviewers operate](mike.md#36-how-reviewers-operate).
Acceptance: with 9 workers the pool cap is 3; with 2 ready pull requests and 3 idle reviewers, 2 are steered.
Verdict: NEW.

#### MS-176 Self-review with the runtime's code-review tool
As a worker (Artificer), I want my self-review done with my runtime's code-review tool on the head, so that the self-review is a review, not a stamp, before an independent reviewer spends time.
Evidence: [factory harness pr_state.py line 41, the self-review parser checks shape only](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/pr_state.py#L41); [mike.md §3.4, review and send-back](mike.md#34-review-and-send-back), [mike.md §6 step 2, owner self-review](mike.md#6-the-pull-request-lifecycle).
Acceptance: every runtime's config names its code-review tool (test); the worker brief says to run it on the head before posting the self-review block ([MS-083, self-review in one shape](#ms-083-self-review-in-one-shape)); a pull request with no self-review on the head is not marked ready.
Verdict: NEW.

### 3.2 The board

#### MS-131 Arthur reads the board
As Arthur (arbiter), I want the board on each board change or newly idle seat (idle seats, each seat's assignment and last completed assignment, send-backs with owner seat, ready pull requests per seat, the priorities list with its notes, target and actual share per row), so that I decide who does what from one read.
Evidence: [factory harness idle_steer.py line 1279, the follow-up carries no board](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/idle_steer.py#L1279); [mike.md §3.1, pool, assignment and share](mike.md#31-pool-assignment-share), [decision 1, Arthur steered on change](mike.md#11-decisions).
Acceptance: the [factory#1761, send-back held awaiting-response](https://github.com/excaliwire/factory/issues/1761) state yields a board naming the 3 send-backs as next assignments; a tick with idle workers writes 0 planner rows.
Verdict: NEW.

#### MS-132 Board Arthur read is shown
As a human (Tig today), I want the board Arthur last read shown on the dashboard with its tick time, so that I can judge his choices against the same input.
Evidence: [factory dashboard rules.mjs line 57, no board view](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L57); [mike.md §7, the dashboard](mike.md#7-the-dashboard); [Mike dashboard API §5, reads](mike-dashboard-api.md#5-reads).
Acceptance: the page payload's board equals, byte for byte, the board in Arthur's last follow-up record.
Verdict: NEW.

#### MS-133 No steer across open work
As a worker (Artificer), I want Mike to refuse any steer that moves me off an open assignment, so that I keep my context; a replaced session is reminted onto the same work.
Evidence: [factory#1336 section 3, the harness redesign](https://github.com/excaliwire/factory/issues/1336) (Avalon lost context 4 times on 2026-09-26); [mike.md §3.2, mint, remint, steer](mike.md#32-mint-remint-steer).
Acceptance: a steer naming a different item than the seat's open assignment is a refused record; a remint onto the same item is applied.
Verdict: NEW. The rule for the first cut; once the assignment closes the seat may be reused ([MS-174, Arthur reuses an idle seat](#ms-174-arthur-reuses-an-idle-seat)).

#### MS-134 Role names renamable in config
As Arthur (arbiter), I want the instance's role names renamable in config, so that renaming a seat needs no code change and no migration verb.
Evidence: [factory#1164, the hardened control-plane API](https://github.com/excaliwire/factory/pull/1164); [factory harness policy.py line 214, the role name policy](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/policy.py#L214); [mike.md §2, roles](mike.md#2-roles).
Acceptance: renaming the `arbiter` default in config changes 0 code files and every record keeps the stable seat id.
Verdict: NEW.

#### MS-174 Arthur reuses an idle seat
As Arthur (arbiter), I want to steer an idle seat onto work related to its last completed assignment instead of minting a fresh seat, so that its context is not thrown away.
Evidence: [factory#1336 section 3, the harness redesign](https://github.com/excaliwire/factory/issues/1336) (Avalon lost context 4 times on 2026-09-26); [mike.md §3.2, mint, remint, steer](mike.md#32-mint-remint-steer).
Acceptance: a steer from Arthur to a seat with no open assignment is applied with a record naming the seat's last completed assignment; tokens per assignment are recorded for reused and freshly minted seats so the saving is measured, not assumed.
Verdict: NEW.

#### MS-175 Board shows last completed assignment
As Arthur (arbiter), I want the board to show each idle seat's last completed assignment, so that I can pick a seat whose context fits the next issue.
Evidence: [factory harness idle_steer.py line 1279, the follow-up carries no board](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/idle_steer.py#L1279); [mike.md §3.1, pool, assignment and share](mike.md#31-pool-assignment-share), [mike.md §3.2, mint, remint, steer](mike.md#32-mint-remint-steer); [Mike dashboard API §7, payload shapes](mike-dashboard-api.md#7-payload-shapes).
Acceptance: each idle seat's board row names `owner/repo#N` of the last item whose `seat:<name>` label it held when the item closed, or `none`; the dashboard's board view shows the same.
Verdict: NEW.

### 3.3 Target versus actual share

#### MS-135 Configurable share per rank
As a human (Tig today), I want a share per priority rank in the config store, defaulting by the number of lanes (1: 100; 2: 75, 25; 3: 60, 30, 10; 4: 50, 30, 15, 5 percent of workers), that I can override, with an empty row's share passed to the next, so that I set the split, not each assignment.
Evidence: [factory#1336 section 3, the harness redesign](https://github.com/excaliwire/factory/issues/1336); [mike.md §3.1, pool, assignment and share](mike.md#31-pool-assignment-share).
Acceptance: with no override, n lanes get weights T(n − i + 1) normalized, T(k) = k(k + 1) / 2 (test for n = 1 to 4); an override set not summing to 100 is refused; a row with 0 open issues above `urgency:no` shows target 0 and the next row's target rises by its share.
Verdict: NEW.

#### MS-136 Target versus actual share
As a human (Tig today), I want Health to show target versus actual share per priority row, so that a bad judgment by Arthur is visible.
Evidence: [factory#1336 section 4, the harness redesign](https://github.com/excaliwire/factory/issues/1336); [mike.md §9 rule 17, Health shows target versus actual share](mike.md#9-what-mike-keeps); [Mike dashboard API §7, payload shapes](mike-dashboard-api.md#7-payload-shapes).
Acceptance: each row shows target percent and actual percent of assigned workers from labels; a gap over 20 points for 3 ticks is one attention item.
Verdict: NEW.

### 3.4 Job ids for commands

#### MS-137 Job ids for every command
As a human (Tig today), I want every command to return a job id at once, and its answer to land on a row I can see whenever it finishes, so that an answer after 30 s is not lost.
Evidence: [factory harness api.py line 4726, synchronous `run_verb`](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/api.py#L4726); [mike.md §7, the dashboard](mike.md#7-the-dashboard); [Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands).
Acceptance: every command POST answers in under 1 s with a job id; a verb that takes 120 s shows its outcome on that job's row.
Verdict: NEW.

#### MS-138 ISO 8601 times on the wire
As a human (Tig today), I want every time on the wire in ISO 8601 with offset, so that the page never parses prose or guesses a year.
Evidence: [factory harness api.py line 478, `format_for_human`](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/api.py#L478); [mike.md §7, the dashboard](mike.md#7-the-dashboard); [Mike dashboard API §7, payload shapes](mike-dashboard-api.md#7-payload-shapes).
Acceptance: a schema test finds 0 time fields not matching ISO 8601 with offset; the page has 0 time-zone tables.
Verdict: NEW.

### 3.5 Phone layout

#### MS-139 Every tab fits a phone
As a human (Tig today), I want every tab readable on a phone, so that I run the fleet away from my desk.
Evidence: [factory dashboard app.css line 125, no breakpoint for the 8-column Sessions table](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.css#L125).
Acceptance: at 375 px width, 0 tabs need horizontal page scroll.
Verdict: CHANGE: today factory's Sessions tab fails; Mike lays out every tab, review surface and board included.

#### MS-140 Every seat verb by tap
As a human (Tig today), I want every single-seat verb reachable by tap, so that I need no right-click.
Evidence: [factory dashboard app.js line 1598, context menu, no touch path](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L1598).
Acceptance: on a touch device each of the 5 seat verbs is reachable within 2 taps from the seat card.
Verdict: CHANGE: today the per-row menu needs a right-click.

### 3.6 Multi-project, single instance

#### MS-141 One instance, several projects
As a human (Tig today), I want one Mike instance to manage several projects with one loop, one store, one dashboard and one priorities list, so that I do not deploy Mike per repository.
Evidence: [tig/mike#2, the master plan](https://github.com/tig/mike/issues/2); [mike.md §1.2, multi-repository, one instance](mike.md#12-multi-repository-one-instance), [decision 6, one list per instance](mike.md#11-decisions); [Mike dashboard API §9, where this is tested](mike-dashboard-api.md#9-where-this-is-tested).
Acceptance: an install with no factory checkout manages two projects from one instance and passes the contract tests in [Mike dashboard API §9, where this is tested](mike-dashboard-api.md#9-where-this-is-tested).
Verdict: NEW.

#### MS-142 Unlisted repositories refused
As a human (Tig today), I want a verb on a repository not on the instance's project list refused before any call runs, for every caller, so that no seat works outside the program.
Evidence: [factory harness __main__.py line 1425, `cmd_steer` does not check](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L1425); [gate 2, the project gate](mike.md#33-gates-mike-enforces-for-every-caller).
Acceptance: a steer, mint or GitHub write naming an unlisted repository makes 0 GitHub or vendor calls and writes one refused record.
Verdict: NEW.

#### MS-143 Every GitHub verb names project
As a seat (any), I want every verb that touches GitHub to take the project explicitly, so that `#N` is never ambiguous across projects.
Evidence: [factory harness __main__.py line 748, `cmd_steer`](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L748); [mike.md §1.2, multi-repository, one instance](mike.md#12-multi-repository-one-instance).
Acceptance: a GitHub verb called without a project is refused; every record and log line of such a verb has a `project` field.
Verdict: NEW.

### 3.7 Gauges and mint threshold

#### MS-144 Runtimes declare gauges in config
As a human (Tig today), I want each runtime to declare its gauges (pools, windows, probe and mint threshold) in config, so that gauges change without code.
Evidence: [factory harness meters.py line 16, `GAUGES` is a code tuple](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/meters.py#L16); [mike.md §4, runtimes](mike.md#4-runtimes).
Acceptance: adding a gauge is a config edit with 0 code changes and its gauge appears on the Gauges tab.
Verdict: NEW.

#### MS-145 Switch vendor at mint threshold
As the loop, I want mint to pick the next vendor when one crosses its mint threshold, so that a vendor limit costs a vendor switch, not a stall.
Evidence: [factory#1501, the Mike extraction](https://github.com/excaliwire/factory/issues/1501) (at 75 percent of Claude's 5-hour limit, stop minting Claude seats and shift to xAI Grok, [decision 10, shift new seats to xAI Grok](mike.md#11-decisions)); [mike.md §4, runtimes](mike.md#4-runtimes).
Acceptance: with the Claude 5-hour gauge at 76 percent, the next mint record names a different vendor and cites the gauge reading.
Verdict: NEW.

#### MS-146 No mint on unmeasured gauge
As the loop, I want a mint that depends on an unmeasured gauge refused, so that an unknown gauge reading is never read as free.
Evidence: [factory harness meters.py line 73, the gauge reader](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/meters.py#L73); [mike.md §4, runtimes](mike.md#4-runtimes).
Acceptance: with the vendor gauge `unmeasured`, 0 mints on that vendor; each attempt is a refused record naming the gauge; the gauge never reads 0.
Verdict: NEW.

### 3.8 The Mike Runtime API

#### MS-148 One actuator interface
As the loop, I want one Mike Runtime API (mint, steer, stop, restart, archive, liveness, usage, session log) that every runtime driver fills or answers `unmeasured` with a reason, whatever its vendor and access method (`cloud` or `tmux`), so that no runtime has a special path in core.
Evidence: [factory harness seat_actuator.py line 353, the actuator](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/seat_actuator.py#L353); [factory#1336 learnings 6, 11, the harness redesign](https://github.com/excaliwire/factory/issues/1336); [mike.md §4, runtimes](mike.md#4-runtimes).
Acceptance: a contract test runs the 8 capabilities against each configured runtime and gets a result or `unmeasured` plus reason for each.
Verdict: NEW.

#### MS-149 Every steer confirmed or not
As a worker (Artificer), I want every steer on every runtime, `cloud` or `tmux` access, confirmed by a run id, pane echo or event id, or reported not confirmed, so that I never get a duplicate or a lost task.
Evidence: [factory harness seat_host.py line 934, delivery confirmation](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/seat_host.py#L934), [factory#1630, grok paste not shown](https://github.com/excaliwire/factory/issues/1630).
Acceptance: each steer record ends `confirmed` with an id or `not confirmed` with a reason; a confirmed steer is never resent.
Verdict: CHANGE: factory confirms tmux pastes and Cursor runs differently; Mike has one result field for all runtimes ([mike.md §4, runtimes](mike.md#4-runtimes)).

#### MS-150 One record shape per actuation
As a human (Tig today), I want mint, archive, restart and kill each to write a decision record of one shape for every runtime, so that Health can show a row clear and "no seat minted twice for one issue".
Evidence: [factory harness seat_actuator.py line 1499, log lines only](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/seat_actuator.py#L1499); [factory#1418, Health red for tmux seats](https://github.com/excaliwire/factory/issues/1418).
Acceptance: each actuation has one record before it acts; Health reads only that record shape (test with one `cloud` and one `tmux` runtime).
Verdict: NEW.

#### MS-151 One pending steer per seat
As a human (Tig today), I want no second steer to a seat while one is pending in the loop window, for every caller and every runtime, pending ones included, so that a seat never gets two tasks at once.
Evidence: [factory harness __main__.py line 1054, `_loop_steer_hold` covers the loop and applied rows only](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L1054); [gate 5, one pending steer](mike.md#33-gates-mike-enforces-for-every-caller).
Acceptance: a human steer, an Arthur steer and a loop steer sent to one seat inside the window give 1 applied and 2 refused records.
Verdict: NEW.

#### MS-172 Session log from every runtime
As a human (Tig today), I want each runtime to provide a seat's session log, its inputs and responses, with the last steer and the latest response marked, so that I and Arthur see what a seat was told and what it said on any vendor.
Evidence: [factory dashboard app.js line 2502, the seat page reads a stored log](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L2502); [mike.md §4, runtimes](mike.md#4-runtimes); [Mike dashboard API §5, reads](mike-dashboard-api.md#5-reads).
Acceptance: for each configured runtime the log's last input equals the last confirmed steer record's prompt and one response is marked latest; a runtime that cannot read it answers `unmeasured` with a reason; the seat page ([MS-007, seat page for diagnosis](#ms-007-seat-page-for-diagnosis)) reads it.
Verdict: NEW.

#### MS-173 Install a runtime driver by config
As a human (Tig today), I want to install or enable a new runtime driver through config, so that a new vendor or access method needs no change to Mike's core.
Evidence: [factory#1336 comments, learnings 6, 9 and 11 on the single-vendor actuator](https://github.com/excaliwire/factory/issues/1336); [mike.md §4, runtimes](mike.md#4-runtimes).
Acceptance: enabling a driver is a config edit with 0 core code changes; the driver passes the [MS-148, one actuator interface](#ms-148-one-actuator-interface) contract test before any mint lands on it; config naming a driver not installed is refused and named on Health.
Verdict: NEW.

### 3.9 Seat and host scoped tokens

#### MS-152 Seat tokens act only as self
As a seat (any), I want my token to name me and act only as me, so that a leaked seat token cannot steer or mint another seat.
Evidence: [factory agent-harness seats.yaml line 57, caller matrix](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/seats.yaml#L57); [mike.md §4, runtimes](mike.md#4-runtimes), [mike.md §9 rule 12, the caller matrix](mike.md#9-what-mike-keeps); [Mike dashboard API §2, identity](mike-dashboard-api.md#2-identity).
Acceptance: a seat token used on any other seat's self-verb is refused with a record; Arthur's and lane-PE steers pass only the matrix rows for their role.
Verdict: NEW.

#### MS-153 No master secret on hosts
As a seat host, I want no shared master secret on my machine and no inbound path or SSH key from the control plane, so that a compromised host cannot mint tokens for other seats.
Evidence: [factory docs/host.md line 258, the host secret](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/host.md#L258), [factory#1413, host secret mints any token](https://github.com/excaliwire/factory/issues/1413); [mike.md §4, runtimes](mike.md#4-runtimes).
Acceptance: a scan of each seat host finds 0 files that can mint a token for another seat; the control-plane host holds 0 SSH keys to seat hosts.
Verdict: NEW.

#### MS-154 Humans are verified bearers
As a human (Tig today), I want to be a verified bearer, not a header any local process can set, so that a local script cannot act as me.
Evidence: [factory dashboard serve.py line 418, adds `X-HGL-Email`](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/serve.py#L418); [mike.md §4, runtimes](mike.md#4-runtimes), [mike.md §10 item 8, a shared secret and a header gate](mike.md#10-what-mike-does-not-re-create); [Mike dashboard API §2, identity](mike-dashboard-api.md#2-identity).
Acceptance: a request with only an email header and no verified bearer is refused 401 on every human-only route.
Verdict: NEW.

### 3.10 Config store apply-on-change

#### MS-155 Settings applied live
As a human (Tig today), I want a setting change applied live by the smallest action (reload, remint the affected seats, or swap a key), recorded, so that a change takes effect without a reboot.
Evidence: [factory#1524, config applied live](https://github.com/excaliwire/factory/issues/1524); [factory harness settings.py line 1258, settings apply](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/settings.py#L1258); [mike.md §5, the control plane](mike.md#5-the-control-plane).
Acceptance: each save writes one record naming the action taken; a cadence change remints 0 seats; a role model change remints only that role's seats.
Verdict: NEW.

#### MS-156 One source for each fact
As a human (Tig today), I want desired state (roles, roster, projects, lanes, hosts, vendors, briefs) as instance config changed by pull request, shipped defaults in a separate file, and live state never in git, so that one source holds each fact.
Evidence: [factory harness store.py line 3, the file store](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/store.py#L3); [mike.md §5, the control plane](mike.md#5-the-control-plane), [mike.md §10 item 16, settings seeded from four places](mike.md#10-what-mike-does-not-re-create).
Acceptance: the instance config repository holds 0 live-state files; each setting has exactly one source (shipped default, instance config, or config store).
Verdict: NEW.

#### MS-157 One locked store owner
As the loop, I want the store owned by one locked process, append-only where it is a log, so that two writers never race and no row is silently replaced.
Evidence: [factory harness store.py line 3, the unlocked file store](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/store.py#L3); [mike.md §5, the control plane](mike.md#5-the-control-plane), [mike.md §10 item 15, an unlocked file store](mike.md#10-what-mike-does-not-re-create).
Acceptance: a second process opening the store is refused and named on Health; a log row once written is never rewritten (test).
Verdict: NEW.

#### MS-158 Failed reads are unmeasured
As the loop, I want a GitHub read that fails to read `unmeasured`, never empty, so that an outage does not look like "no work".
Evidence: [factory harness gh.py line 100, the GitHub read module](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/gh.py#L100); [mike.md §5, the control plane](mike.md#5-the-control-plane).
Acceptance: with GitHub returning 502, the tick records `unmeasured` for each read and 0 steers or mints.
Verdict: NEW.

### 3.11 Attached sessions

#### MS-159 Revocable attached session tokens
As a human (Tig today), I want to issue a named, revocable session token to a session I drive (Infra Fable, Factory Fable, my portal), so that it can act through Mike without a seat and without my own credentials.
Evidence: [mike.md §2.2, attached sessions](mike.md#22-attached-sessions-non-seats-that-act-through-mike) and [mike.md §4, runtimes](mike.md#4-runtimes) (Identity); factory has only a seat token minted from a shared secret, [factory hgl-auth agent_token.py line 54, the shared-secret seat token](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/host/hgl-auth/agent_token.py#L54); [Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands).
Acceptance: the token carries the session name and its verb list; a revoked token is refused on the next call with a record; no shared secret can mint one.
Verdict: NEW.

#### MS-160 Attached sessions write through Mike
As an attached session, I want every repository interaction (issue create, label, urgency, comment, pull ready, request merge) to go through Mike's verbs with my token, so that each is recorded first and written under Mike's account with my `[Name]` prefix.
Evidence: [mike.md §2.2, attached sessions](mike.md#22-attached-sessions-non-seats-that-act-through-mike), [mike.md §5, the control plane](mike.md#5-the-control-plane) (GitHub), [mike.md §9 rule 3, one choke point for GitHub writes](mike.md#9-what-mike-keeps), [mike.md §9 rule 15, the address contract](mike.md#9-what-mike-keeps).
Acceptance: one decision record per call with `actor` = the session name; the GitHub write is by Mike's account and starts `[Name] `; a call with no record is refused.
Verdict: NEW.

#### MS-161 Attached sessions read the board
As an attached session, I want to read the board, sessions, health and priorities over the same API a seat reads, so that my judgment uses the operator's view.
Evidence: [mike.md §2.2, attached sessions](mike.md#22-attached-sessions-non-seats-that-act-through-mike), [mike.md §3.1, pool, assignment and share](mike.md#31-pool-assignment-share); seats read the same API in [MS-008, Arthur reads the same API](#ms-008-arthur-reads-the-same-api); [Mike dashboard API §5, reads](mike-dashboard-api.md#5-reads).
Acceptance: `GET {base}/api/seats` and `GET {base}/api/board` answer a session token with the same rows the page draws.
Verdict: NEW.

#### MS-162 Attached sessions steer through gates
As an attached session whose config row allows it, I want to steer a seat through Mike bound by every gate, so that I can direct work at night without a comment Arthur must notice.
Evidence: [mike.md §2.2, attached sessions](mike.md#22-attached-sessions-non-seats-that-act-through-mike), [mike.md §3.3, gates for every caller](mike.md#33-gates-mike-enforces-for-every-caller); [factory#1336 comment 2026-10-05 05:18 UTC, the harness redesign](https://github.com/excaliwire/factory/issues/1336) (steers delivered as `Arthur:` comments); [Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands).
Acceptance: a steer from the session passes [gates 1 to 6, owner gate through record before act](mike.md#33-gates-mike-enforces-for-every-caller) or is refused with a record naming the gate; a session whose row lacks `steer` gets 403 and a refused record.
Verdict: NEW.

#### MS-163 Attached sessions listed apart
As a human (Tig today), I want attached sessions listed on the dashboard with last call and token age, apart from the Seats tab, so that I can see who is acting through Mike and revoke one.
Evidence: [mike.md §2.2, attached sessions](mike.md#22-attached-sessions-non-seats-that-act-through-mike), [mike.md §7, the dashboard](mike.md#7-the-dashboard); [Mike dashboard API §7, payload shapes](mike-dashboard-api.md#7-payload-shapes).
Acceptance: one row per token with name, verbs, last call time, issued-at; a Revoke verb with one confirm; the Seats tab shows no attached session.
Verdict: NEW.

#### MS-164 Attaching is optional
As an attached session, I want attaching to be optional, so that a session with no token works as today and Mike sees it only through GitHub.
Evidence: [mike.md §2.2, attached sessions](mike.md#22-attached-sessions-non-seats-that-act-through-mike).
Acceptance: with no token set, the CLI's Mike verbs refuse and name the token; the session's direct GitHub comments carry no actor record and raise no Health row.
Verdict: NEW.

### 3.12 The control plane watches

#### MS-165 Control plane detects every change
As the loop, I want to detect every board change myself, from signed webhooks and a diff of my own store each tick, so that no seat polls GitHub and no vendor scheduler watches anything for Mike.
Evidence: [mike.md §5, the control plane](mike.md#5-the-control-plane) and [mike.md §9 rule 22, the control plane is the only watcher](mike.md#9-what-mike-keeps); factory polls a human's notifications in [factory harness poke.py line 1, polling a human's notifications](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/poke.py#L1) and seats read GitHub themselves.
Acceptance: with the webhook delivering, a tick makes 0 GitHub reads that are not the budgeted store refresh; a brief contains no instruction to poll or watch GitHub; a seat's own `gh` read of issue state is a refused record.
Verdict: NEW.

#### MS-166 Changes routed as steers
As the loop, I want each detected change routed to the seat it concerns as one recorded steer (Arthur for a board change or an idle seat; the author for a send-back, a conflict or Copilot findings; a reviewer for a ready pull request), so that a seat is told and never has to notice.
Evidence: [mike.md §5, the control plane](mike.md#5-the-control-plane), [mike.md §3.4, review and send-back](mike.md#34-review-and-send-back), [decision 1, Arthur steered on change](mike.md#11-decisions) and [decision 5, conflicts are changes, not verbs](mike.md#11-decisions); factory runs conflict-steer and copilot-findings as verbs ([MS-094, conflicts and Copilot threads sent back](#ms-094-conflicts-and-copilot-threads-sent-back)).
Acceptance: one steer record per change with `why` naming the change kind and the GitHub event or diff that produced it; the same change produces 0 further steers; the steer passes the gates or is a refused record.
Verdict: NEW.

#### MS-167 Row note carried in steers
As a lane-PE, I want the note on my lane's priorities row carried in every steer I receive, so that a human's intent for the row is my context without a comment I must find.
Evidence: [mike.md §3.1, pool, assignment and share](mike.md#31-pool-assignment-share), [decision 2, a lane plus a note](mike.md#11-decisions).
Acceptance: a steer to a lane-PE whose lane has a row with a note contains that note verbatim; a row with no note adds nothing; the note appears on the board Arthur reads.
Verdict: NEW.

### 3.13 Humans on GitHub

#### MS-168 Human issues reach the board
As a human, I want an issue I create to reach the board when I give it a lane label and assign it to `gh_user`, so that handing work to Mike is one GitHub action I already know.
Evidence: [mike.md §2.1, humans](mike.md#21-humans); factory's harness-gh-user gate, [factory harness harness_gh_user.py line 1, the harness-gh-user gate](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/harness_gh_user.py#L1).
Acceptance: within one tick of the assignment webhook the issue is on the board with my `urgency:` label, or `urgency:no` if I set none; before the assignment it is not on the board.
Verdict: NEW.

#### MS-169 Addressed comments become steers
As a human, I want a comment I start with `To: Name` on an issue or pull request delivered to that seat as a steer, so that I direct a seat from GitHub on my phone without a dashboard.
Evidence: [mike.md §2.1, humans](mike.md#21-humans), [mike.md §9 rule 15, the address contract](mike.md#9-what-mike-keeps) (address contract); [factory#1336 comment 2026-10-05 05:18 UTC, the harness redesign](https://github.com/excaliwire/factory/issues/1336) (`Arthur:` comments as steers).
Acceptance: one steer record per addressed comment with `why` naming the comment id and my login; the steer passes the gates or is a refused record; an unaddressed comment, one starting only with a writer prefix `[Name]`, or one using factory's `Name:` or the retired `[Name]:` form produces 0 steers and one lint line.
Verdict: NEW.

#### MS-170 Human reviews count when configured
As a human, I want my change request on a ready pull request to be the send-back and my Merge verdict to count as the independent review when config says so, so that a review I did is not redone by a reviewer seat.
Evidence: [mike.md §2.1, humans](mike.md#21-humans), [mike.md §3.4, review and send-back](mike.md#34-review-and-send-back), [mike.md §3.6, how reviewers operate](mike.md#36-how-reviewers-operate), [mike.md §6, the pull request lifecycle](mike.md#6-the-pull-request-lifecycle); factory's `independent_review_writers` and `reviewer:` grant, [factory harness pr_state.py line 45, independent review writers](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/pr_state.py#L45).
Acceptance: a change request from a listed human is a send-back: it returns the pull request to draft and steers the owner seat; with `human_review_counts` on, a Merge verdict from a listed human satisfies the review gate for that head.
Verdict: NEW.

#### MS-171 Unlisted users are contributors
As a human, I want a GitHub user not on the instance's human list treated as a contributor, so that their issues and comments are seen but bind nothing.
Evidence: [mike.md §2.1, humans](mike.md#21-humans).
Acceptance: a contributor's issue shows on the board as unassigned contributor work; their `waive:`, `reviewer:` and `To: Name` comments produce 0 records that act; a listed human's assignment of that issue puts it on the board.
Verdict: NEW.

### 3.14 Dashboard API contract

#### MS-177 Command outcome on the changed row
As a human (Tig today), I want a command's outcome shown on the row it changed, however long it took, so that I see the result where I acted.
Evidence: [mike.md §7, the dashboard](mike.md#7-the-dashboard); [Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands), [Mike dashboard API §7, payload shapes](mike-dashboard-api.md#7-payload-shapes).
Acceptance: each seat's outcome from `jobRow.seats` shows on that seat's card on the Seats tab; a steer that takes 120 s shows its outcome there with no reload; a stream reopen restores it from the opening `jobs` frame; `GET {base}/api/jobs?job=<id>` answers the same row.
Verdict: NEW.

#### MS-178 Stale settings write refused
As a human (Tig today), I want a settings save based on an old version refused, so that I never overwrite a change someone made after my page loaded.
Evidence: [Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands); [MS-061, settings history by version](#ms-061-settings-history-by-version).
Acceptance: a `POST settings` whose `expected_version` is not the current `store_version` answers 409 and writes no version; the page says the setting changed and shows the new value; the save with the current version is applied.
Verdict: NEW.

#### MS-179 Open streams capped per caller
As a human (Tig today), I want each caller's open streams capped by config, so that a leaking client or a looping seat cannot exhaust the control plane.
Evidence: [Mike dashboard API §4, the stream](mike-dashboard-api.md#4-the-stream).
Acceptance: with the cap at N, the caller's open N+1 answers 429 and the first N stay open; the page says the stream cap is reached, not that the control plane is down.
Verdict: NEW.

### 3.15 The Seats tab and the seat card

#### MS-180 One seat card component everywhere
As a human, I want every seat drawn as the same seat card wherever it appears, so that I learn one shape and read it the same on every tab.
Evidence: [mike.md §7.1, the Seats tab and the seat card](mike.md#71-the-seats-tab-and-the-seat-card); [the approved mockup](mike.md#71-the-seats-tab-and-the-seat-card).
Acceptance: the Seats tab, the board, and the review surface render a seat through one component; a change to the card's markup appears on all three without a second edit.
Verdict: NEW.

#### MS-181 Cards grouped by role, responsive
As a human, I want cards grouped as orchestrators, lane-PEs, workers and reviewers, side by side on a desktop and stacked on a phone, so that I find a seat by its job on any screen.
Evidence: [mike.md §7.1, the Seats tab and the seat card](mike.md#71-the-seats-tab-and-the-seat-card).
Acceptance: at 1180 px a group shows at least 2 cards per row; at 375 px one per row with no horizontal page scroll; the card's inner grid goes from two columns to one by its own container width.
Verdict: NEW.

#### MS-182 Seat card info block
As a human, I want each card to show name, role, liveness LED with its word, driver, last mint, assignment with its time, last steer with its time, context pressure as a bar gauge, and tokens since mint, so that one glance answers who, what, how long, and how full.
Evidence: [mike.md §7.1, the Seats tab and the seat card](mike.md#71-the-seats-tab-and-the-seat-card); [MS-002, liveness in four words](#ms-002-liveness-in-four-words).
Acceptance: all nine fields present on every card; the LED color always has its word beside it; an unmeasured field reads unmeasured plus its reason and draws no bar; the gauge fill changes to warning at 60 percent and critical at 80 percent.
Verdict: NEW.

#### MS-183 Seat card controls
As a human, I want a start-stop switch and Restart, Steer, Mint and Archive at the bottom of each card, with a verb disabled and explained when the seat's row does not list it, so that I act on one seat without a menu hunt.
Evidence: [mike.md §7.1, the Seats tab and the seat card](mike.md#71-the-seats-tab-and-the-seat-card); [MS-027, verb buttons explain themselves](#ms-027-verb-buttons-explain-themselves).
Acceptance: the five controls are present on every card; a control not in the row's `verbs` is disabled with `verb_why` as its hover text; a click posts one command and the card shows the job outcome.
Verdict: NEW.

#### MS-184 Phone card: expander and hamburger
As a human on a phone, I want the card's info behind a Details expander and its verbs behind a hamburger, with the start-stop switch still visible, so that the tab stays short and every verb has a touch path.
Evidence: [mike.md §7.1, the Seats tab and the seat card](mike.md#71-the-seats-tab-and-the-seat-card); [MS-005, last confirmed steer shown](#ms-005-last-confirmed-steer-shown).
Acceptance: at 375 px a closed card is at most 3 lines tall; the expander and the hamburger each open with one tap; the switch is reachable without opening either; an open expander or menu survives a sessions frame.
Verdict: NEW.

## 4. Retired stories

Not built ([mike.md §3.3, gates for every caller](mike.md#33-gates-mike-enforces-for-every-caller), [mike.md §10, what Mike does not re-create](mike.md#10-what-mike-does-not-re-create), [mike.md §12, done when](mike.md#12-done-when)). One line each.

- The starved-lanes view ("as the control plane reads it"): every lane has a priorities row, so no lane is starved; [MS-136, target versus actual share](#ms-136-target-versus-actual-share) replaces it ([mike.md §9 rule 17, Health shows target versus actual share](mike.md#9-what-mike-keeps)); [gate 3, the lane gate](mike.md#33-gates-mike-enforces-for-every-caller) refuses an issue with no lane label or an unknown lane.
- Redeliver-tries, the conflict-steer cooldown and the orchestrator cooldown: nothing is redelivered; Arthur's follow-up fires on a board change ([MS-131, Arthur reads the board](#ms-131-arthur-reads-the-board), [decision 1, Arthur steered on change](mike.md#11-decisions)).
- Verbs holding on an unmeasured reading: there are no holds; a refusal streak is [MS-053, refusal streaks named](#ms-053-refusal-streaks-named) ([mike.md §10 item 1, the steer-idle planner](mike.md#10-what-mike-does-not-re-create)).
- Assigned but never steered: the label is the assignment and the remint carries it ([MS-034, remint carries the assignment](#ms-034-remint-carries-the-assignment), [mike.md §3.1, pool, assignment and share](mike.md#31-pool-assignment-share)); the board shows it.
- Fleet idle with work, with the last planner reason: the planner is gone; the board and share rows show idle capacity ([MS-136, target versus actual share](#ms-136-target-versus-actual-share), [mike.md §10 item 1, the steer-idle planner](mike.md#10-what-mike-does-not-re-create)).
- Frozen lane focus: there is no lane owner to freeze ([MS-015, edit the priorities list](#ms-015-edit-the-priorities-list), [mike.md §3.1, pool, assignment and share](mike.md#31-pool-assignment-share)).
- The worker planner (steer-idle) with its 12 hold words, 12 none-eligible reasons and 9 wordless gates: Arthur decides from the board ([MS-131, Arthur reads the board](#ms-131-arthur-reads-the-board), [mike.md §10 item 1, the steer-idle planner](mike.md#10-what-mike-does-not-re-create), [mike.md §10 item 2, two deciders on one roster](mike.md#10-what-mike-does-not-re-create)).
- Enqueue and redeliver through `assign` and `assignments.jsonl`: one store, every steer through the control plane, no second queue ([MS-073, record every steer first](#ms-073-record-every-steer-first), [mike.md §10 item 7, machine-local steer queues](mike.md#10-what-mike-does-not-re-create)).
- Stand-down and resume: a seat waiting on a gate gets a steer from Arthur ("wait for <issue>") ([MS-131, Arthur reads the board](#ms-131-arthur-reads-the-board), [mike.md §10 item 18, stand-down and resume](mike.md#10-what-mike-does-not-re-create)).
- The reboot tail queueing one restart per grok-tmux orchestrator: the one-pending-actuation rule ([MS-033, no double actuation](#ms-033-no-double-actuation)) covers every runtime ([mike.md §4, runtimes](mike.md#4-runtimes)).
- Lane-PE host moves down the ladder: gauges with a mint threshold replace the ladder ([MS-144, runtimes declare gauges in config](#ms-144-runtimes-declare-gauges-in-config), [MS-145, switch vendor at mint threshold](#ms-145-switch-vendor-at-mint-threshold), [decision 15, holds and the ladder retire](mike.md#11-decisions)).
- Ladder tier moves on included-pool gauges: same; the gauges stay ([MS-070, vendor included pools shown](#ms-070-vendor-included-pools-shown)), the ladder goes ([decision 15, holds and the ladder retire](mike.md#11-decisions)).
- The owned-work preamble ("A send-back beats other owned work, and owned work beats a new ticket."): a seat owns one assignment; a send-back is its next one ([MS-093, send-back returns to author](#ms-093-send-back-returns-to-author), [mike.md §3.4, review and send-back](mike.md#34-review-and-send-back)).
- The seat-assignment Discussion board publisher (`dashboard --publish`, `--minimize-stale`, `dashboards_retired`): retired boards, about 1300 dead lines ([MS-131, Arthur reads the board](#ms-131-arthur-reads-the-board), [mike.md §10 item 14, the Discussion board publisher](mike.md#10-what-mike-does-not-re-create)).
- The `retitle` one-shot migration: finished on factory; not product code ([mike.md §10 item 20, one-shot migration verbs](mike.md#10-what-mike-does-not-re-create)).
- The `seat-rename` one-shot migration: a stable seat id makes rename a config edit ([MS-134, role names renamable in config](#ms-134-role-names-renamable-in-config), [mike.md §10 item 20, one-shot migration verbs](mike.md#10-what-mike-does-not-re-create)).
- The `Lexicon: Clear.` review line and the four-line self-review form: retired on factory by [factory#1741, terse comment guidance](https://github.com/excaliwire/factory/issues/1741); line 1's verdict carries it ([MS-083, self-review in one shape](#ms-083-self-review-in-one-shape), [mike.md §3.4, review and send-back](mike.md#34-review-and-send-back)).

### 4.1 Retired after review

#### MS-147 Mint runs capped by budget
As a human (Tig today), I wanted each mint run capped by a token and turn budget and cancelled when over.
Evidence: [factory#1755, lane-PE mint burns tokens](https://github.com/excaliwire/factory/issues/1755), its done-when.
Verdict: LEGACY: the budget came from that issue's done-when, not from a human; Mike has no budgets. A wait-only mint ([MS-099, mint wait-only](#ms-099-mint-wait-only)) and gauges with a mint threshold ([MS-145, switch vendor at mint threshold](#ms-145-switch-vendor-at-mint-threshold), [mike.md §4, runtimes](mike.md#4-runtimes)) cover the cost.
