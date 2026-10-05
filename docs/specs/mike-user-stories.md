# Mike user stories

**Status:** plan. What each role needs from Mike, one story per need, each with its factory evidence, one measurement, and a verdict.

**Source pin:** excaliwire/factory `bb2bf4c6` ([tree](https://github.com/excaliwire/factory/tree/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8)). The first cite in a story is a link of the form `https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/<path>#L<n>`. Later cites in the same story are short: `D/` = `agent-harness/dashboard/`, `AH/` = `agent-harness/agent_harness/`, `H/` = `agent-harness/`, `briefs/` = `agent-harness/briefs/`, `lex` = `docs/lexicon.md`, `spec` = `docs/specs/dashboard-api.md`; a bare `AGENTS.md` is the repo root.

**Rules for this file:** [`mike.md`](mike.md) wins over factory and over these stories. `was:` names the ids in the two extraction reports (`US-xx` from the dashboard read, `OS-xx` from the CLI and brief read; `OS 3.n` is that report's brief-contract section) so the evidence can be found. Verdicts: KEEP (Mike does what factory does), CHANGE (the need stays, the shape changes), NEW (factory has no form of it). LEGACY stories are listed once in section 4 and are not built (`mike.md` section 12).

## 1. Dashboard and UI stories

### 1.1 Observe the fleet

**MS-001** As the human (Tig today), I want one table of every seat with its name and role, so that I see who exists without reading config files.
Evidence: [agent-harness/dashboard/app.js:1646](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L1646), `AH/api.py:2346`. was: US-01.
Acceptance: row count equals the configured role seats plus the minted pool names; order is arbiter, TPM, lane-PEs, workers, reviewers; each row reads "Name - Role".
Verdict: CHANGE: rows come from role config and the pool (`mike.md` 3.1, decision 11), not 13 standing names in `seats.yaml`.

**MS-002** As the human (Tig today), I want each seat's liveness as one of four words with the reason on hover, identical for every runtime, so that "no session" and "session not responding" never look alike.
Evidence: [agent-harness/dashboard/rules.mjs:878](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L878), `AH/liveness.py:1`, `lex:257`. was: US-02, OS-47.
Acceptance: for cursor-cloud, claude-cloud and grok-tmux seats the word is one of `not-minted`, `responding`, `not-responding`, `unmeasured`; every non-responding word has a non-empty reason; one function computes it (test).
Verdict: KEEP.

**MS-003** As the human (Tig today), I want the liveness cell to open the vendor session when a seat is minted, so that I can watch it in one click.
Evidence: [agent-harness/dashboard/rules.mjs:898](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L898), `D/app.js:1677`. was: US-03.
Acceptance: a link exists if and only if the word is `responding` or `not-responding` and the URL is http(s).
Verdict: KEEP.

**MS-004** As the human (Tig today), I want each seat's assignment as a linked `owner/repo#N` with its title, or idle, so that I see what each seat is on and in which project.
Evidence: [agent-harness/dashboard/rules.mjs:840](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L840), `AH/api.py:1996`. was: US-04.
Acceptance: the cell matches the `seat:<name>` label on GitHub for 100% of rows in a 20-row sample; a pull request links to `/pull/N`.
Verdict: CHANGE: the label is the truth and the store a cache (`mike.md` 3.1); the project is named on the cell.

**MS-005** As the human (Tig today), I want each seat's last confirmed steer, clipped, with the full text on hover, so that I know what it was last told.
Evidence: [agent-harness/dashboard/app.js:1691](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L1691). was: US-05.
Acceptance: at most 40 characters shown; the full prompt is in the title when longer.
Verdict: KEEP.

**MS-006** As the human (Tig today), I want an open page to update by itself when state changes, so that I never reload.
Evidence: [agent-harness/dashboard/app.js:2685](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L2685), `spec:51`. was: US-06.
Acceptance: a store change reaches an open page in under 2 s plus network time.
Verdict: KEEP.

**MS-007** As the human (Tig today), I want a seat page with liveness, last mint, last steer, pending steer, and the stored session log, so that I can diagnose one seat.
Evidence: [agent-harness/dashboard/app.js:2502](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L2502), `AH/api.py:2166`. was: US-08.
Acceptance: `/sessions/<seat>` shows all 5 blocks; a missing log reads `unmeasured`.
Verdict: KEEP.

**MS-008** As Arthur (arbiter), I want the seat list, verbs, assignments and Health over the same API with my seat token, so that my decisions use the human's view.
Evidence: [agent-harness/dashboard/rules.mjs:7](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L7), `AH/api.py:3058`, `spec:13`. was: US-13.
Acceptance: the sessions read with a seat token returns rows byte-identical to the rows the page draws.
Verdict: KEEP.

**MS-009** As the human (Tig today), I want each row to name the seat's runtime and host, so that I know where a seat runs without expecting it to carry a control-plane key.
Evidence: [agent-harness/agent_harness/api.py:2210](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/api.py#L2210). was: US-14.
Acceptance: every row shows a runtime from the config list and a host or `cloud`; 0 rows carry the per-seat "acts through the control plane" text.
Verdict: CHANGE: every seat acts through the control plane (`mike.md` 4), so the special-case marker goes.

### 1.2 Steer and assign

**MS-010** As the human (Tig today), I want to type a steer on a seat's page and send it, so that I can redirect one seat fast.
Evidence: [agent-harness/dashboard/app.js:2513](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L2513). was: US-15.
Acceptance: one POST `{verb:steer, seats:[name], prompt}`; the button is disabled unless the row's `verbs` lists steer; the answer names confirmed or not confirmed.
Verdict: KEEP.

**MS-011** As the human (Tig today), I want to steer several checked seats at once with one prompt and an optional assignment, so that I can redirect a group.
Evidence: [agent-harness/dashboard/app.js:1377](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L1377), `D/app.js:1573`. was: US-16.
Acceptance: one POST with `seats` equal to every checked name; refused before sending when prompt and assignment are both empty.
Verdict: KEEP.

**MS-012** As the human (Tig today), I want to set a seat's assignment (`owner/repo#N`) while minting, steering or restarting, and clear it with `idle`, so that I own the durable assignment.
Evidence: [agent-harness/dashboard/verbs.mjs:106](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/verbs.mjs#L106), `D/app.js:1582`. was: US-17.
Acceptance: after a save the `seat:<name>` label is on that issue within one tick; empty input changes nothing; `idle` removes the label.
Verdict: CHANGE: the write is the label in the named project, recorded first.

**MS-013** As the human (Tig today), I want a pending steer shown apart from the last confirmed one, with its age and why it waits, so that I know why a steer has not landed.
Evidence: [agent-harness/dashboard/rules.mjs:914](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L914), `D/app.js:2573`, `AH/api.py:2882`. was: US-18, US-66.
Acceptance: with the loop Paused and a steer pending, the cell reads "pending, not delivered: Paused, <age>" and a second steer to that seat is refused.
Verdict: CHANGE: at most one pending steer per seat (`mike.md` 3.3.5) with a reason, replacing the separate "Assignments untouched" finding.

**MS-014** As the human (Tig today), I want Stop to set a seat idle and keep its session, and only me or Arthur to undo it, so that the loop leaves it alone.
Evidence: [agent-harness/dashboard/verbs.mjs:66](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/verbs.mjs#L66), `H/seats.yaml:70`, `lex:239`. was: US-19.
Acceptance: after Stop the cell reads "stopped"; 0 loop steer records target the seat until a record by the human or Arthur clears Stop.
Verdict: CHANGE: factory clears Stop on any human steer; Mike lets the human or Arthur clear it, nothing else (`mike.md` 3.3.8).

**MS-015** As the human (Tig today), I want an ordered priorities list of at most 3 lanes that I can add to, edit, reorder by tap or drag, and delete from, so that I set what the fleet works on from phone or desk.
Evidence: [agent-harness/dashboard/app.js:2143](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L2143), `AH/__main__.py:4642`, `D/rules.mjs:1198`. was: US-20, OS-22.
Acceptance: each action is one POST and one config-store version; a 4th row, an unknown lane or a duplicate lane is refused; up and down work without drag.
Verdict: CHANGE: priorities list, not direction; 3 rows with a share each (`mike.md` 3.1); the API's `direction` command is renamed at the next major (decision 8).

**MS-016** As the human (Tig today), I want the lane picker to offer only configured lanes not already listed, and a flag on a row whose lane is not configured, so that the list cannot contain a typo.
Evidence: [agent-harness/dashboard/rules.mjs:1227](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L1227), `D/app.js:2047`. was: US-22.
Acceptance: the picker excludes listed lanes, compared case-folded; an unknown lane row shows "not a lane: edit this row and pick one".
Verdict: KEEP.

**MS-017** As the human (Tig today), I want the priorities page to say when it cannot read the store, so that an unreadable store does not look empty.
Evidence: [agent-harness/dashboard/rules.mjs:558](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L558), `AH/api.py:3825`. was: US-23.
Acceptance: with the store unreadable the page reads "unmeasured: <reason>", a save is refused, and every worker steer is refused.
Verdict: CHANGE: no seed file view; shipped defaults and instance config are separate files (`mike.md` 5, section 10.16).

**MS-018** As Arthur (arbiter), I want to steer a seat with my seat token when the caller matrix allows it, and a denied attempt recorded with my name, so that I assign work without a click and a denial is evidence.
Evidence: [agent-harness/agent_harness/api.py:4686](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/api.py#L4686), `AH/api.py:4697`, `H/seats.yaml:57`. was: US-24, US-82.
Acceptance: an allowed call answers with `actor=<seat>`; a denied one answers 403 and writes a record with `caller=<seat>`, outcome refused.
Verdict: CHANGE: every gate in `mike.md` 3.3 applies to Arthur's steers as to the loop's.

**MS-019** As the loop, I want to steer only issues and pull requests assigned to `gh_user`, and the human to confirm any change to it, so that a wrong login cannot start spending.
Evidence: [agent-harness/agent_harness/harness_gh_user.py:1](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/harness_gh_user.py#L1), `AH/settings.py:365`, `D/rules.mjs:1543`. was: US-25, OS-27.
Acceptance: changing `gh_user` opens a confirm; with it empty or unmeasured, 0 steers apply and each is a refused record.
Verdict: KEEP. Renamed from harness-gh-user.

### 1.3 Review and merge

**MS-020** As the human (Tig today), I want ready pull requests in merge conflict listed with their author seat, so that each becomes a send-back.
Evidence: [agent-harness/agent_harness/attention.py:136](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/attention.py#L136). was: US-27.
Acceptance: one row per conflicting ready pull request with `owner/repo#N` and the author seat, linked.
Verdict: CHANGE: shown on the review surface (MS-128), routed as a send-back (decision 5).

**MS-021** As the human (Tig today), I want a reviewer whose assignment is a pull request to link to that pull request, so that I open the review in one click.
Evidence: [agent-harness/agent_harness/api.py:2024](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/api.py#L2024). was: US-28.
Acceptance: the assignment URL ends in `/pull/N` when the item is a pull request.
Verdict: KEEP.

**MS-022** As the human (Tig today), I want to point a reviewer at a pull request by typing it as the reviewer's assignment with a steer, so that a review starts now.
Evidence: [agent-harness/dashboard/verbs.mjs:109](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/verbs.mjs#L109). was: US-29.
Acceptance: the reviewer row shows `#N` on the next sessions frame; the steer is refused when the reviewer wrote the pull request or has another without a verdict.
Verdict: CHANGE: reviewer independence and one-pull-request-per-reviewer are gates (`mike.md` 3.3.9, 3.4).

### 1.4 Manage seats

**MS-023** As the human (Tig today), I want to mint a seat that has no session, optionally with an assignment, so that I bring it into being.
Evidence: [agent-harness/dashboard/verbs.mjs:62](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/verbs.mjs#L62), `D/app.js:1587`. was: US-32.
Acceptance: enabled only when every selected row lists mint; one decision record per seat before the vendor call.
Verdict: KEEP.

**MS-024** As the human (Tig today), I want to restart a seat after one confirm, keeping its assignment, so that I replace a stuck session.
Evidence: [agent-harness/dashboard/verbs.mjs:63](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/verbs.mjs#L63), `D/app.js:1551`. was: US-33.
Acceptance: body carries `confirm:"restart"`; the label is unchanged afterwards; one restart record exists.
Verdict: KEEP.

**MS-025** As the human (Tig today), I want to archive any seat's session after one confirm, keeping the name, so that I end it on any runtime.
Evidence: [agent-harness/dashboard/verbs.mjs:65](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/verbs.mjs#L65), `AH/seat_actuator.py:382`. was: US-34.
Acceptance: for each configured runtime, archive leaves liveness `not-minted` on the next frame and one archive record.
Verdict: CHANGE: factory archives cursor-cloud and claude-tmux only; Mike archives every runtime (`mike.md` 4).

**MS-026** As the human (Tig today), I want to check rows, or all rows, and run one verb on all of them, so that I act on a group.
Evidence: [agent-harness/dashboard/app.js:1562](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L1562), `D/app.js:1711`. was: US-35.
Acceptance: the bar reads "N seats selected"; a verb is enabled only if every checked row lists it.
Verdict: KEEP.

**MS-027** As the human (Tig today), I want each verb button to say what it does and why it is off, in the server's words, so that I do not guess and the page cannot drift.
Evidence: [agent-harness/dashboard/verbs.mjs:71](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/verbs.mjs#L71), `AH/seat_actuator.py:353`. was: US-37.
Acceptance: 0 why-off strings in the page source; each tooltip equals the server's field for that row and verb.
Verdict: CHANGE: factory's `verbReason` re-derives the rule in prose and already disagrees with the server (section 10.21).

**MS-028** As the human (Tig today), I want verbs offered only when the control plane lists them for the row, so that I cannot mint a responding seat.
Evidence: [agent-harness/dashboard/verbs.mjs:35](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/verbs.mjs#L35), `spec:89`. was: US-38.
Acceptance: no button is enabled for a verb a selected row's `verbs` lacks; the server refuses the verb anyway with a record.
Verdict: KEEP.

**MS-029** As the human (Tig today), I want each command I send shown as a notification that moves from sent to done, started or refused with the why, so that I know what happened without reading logs.
Evidence: [agent-harness/dashboard/rules.mjs:1032](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L1032), `D/app.js:1253`. was: US-43.
Acceptance: a notification appears at click time carrying the job id (MS-137) and is updated by the answer; an identical pending command is not re-sent.
Verdict: CHANGE: keyed by job id, not by a 30-second wait.

**MS-030** As the human (Tig today), I want to change a role's vendor, runtime and model and choose remint now, when idle, or at the next reboot, so that I control when the money is spent.
Evidence: [agent-harness/dashboard/app.js:1034](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L1034), `AH/remint.py:1`, `AH/api.py:5146`. was: US-44, US-30, OS-14.
Acceptance: the dialog lists exactly the seats of that role; only those seats remint; each keeps its old values until its trigger; the pending rows are written before the settings version.
Verdict: CHANGE: the field is `runtime`, not `harness` (decision 7).

**MS-031** As the human (Tig today), I want to pick which account each vendor bills, by secret name, so that a seat runs on the right subscription.
Evidence: [agent-harness/agent_harness/settings.py:554](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/settings.py#L554), `D/rules.mjs:1415`. was: US-45.
Acceptance: one picker per vendor; with no account named it is disabled and reads "unmeasured: <reason>"; no value of a secret reaches the page.
Verdict: CHANGE: per vendor from config, not four fixed harness rows.

**MS-032** As the human (Tig today), I want lane-PE seats minted only by me, so that an expensive seat is never spawned by an agent or the loop.
Evidence: [agent-harness/briefs/factory-pe.md:13](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/briefs/factory-pe.md#L13), `H/AGENTS.md:145`, `D/rules.mjs:1543`. was: US-46, OS-08.
Acceptance: across a week of ticks, fill-missing, Hard Reboot and Arthur's verbs mint 0 lane-PE seats; a seat-token mint of a lane-PE is a refused record.
Verdict: CHANGE: the `fill_missing_lane_pes` setting (seeded on in factory) is not re-created (`mike.md` 2).

**MS-033** As a worker (Artificer), I want mint and restart withheld while any actuation for me is pending, so that my session is not restarted twice and my first steer not sent twice.
Evidence: [agent-harness/agent_harness/seat_actuator.py:318](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/seat_actuator.py#L318), `AH/seat_actuator.py:384`. was: US-47.
Acceptance: while an actuation is pending, the row's `verbs` lacks mint and restart and the server refuses both.
Verdict: CHANGE: one rule for every runtime and actuation kind, not a create-queued special case.

**MS-034** As a worker (Artificer), I want a remint, including Worker Reboot, to carry my assignment so that my first steer after it is the same work, so that I do not lose context.
Evidence: [agent-harness/dashboard/rules.mjs:1292](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L1292), `lex:263`, `lex:299`. was: US-31, US-48.
Acceptance: after a reboot without Reset Defaults, each worker's and reviewer's first steer record has why `remint` and names its prior assignment; no other row redelivers it.
Verdict: KEEP.

### 1.5 Configure

**MS-035** As the human (Tig today), I want one Running/Paused switch for the loop that acts on click, so that I can stop all automated action at once.
Evidence: [agent-harness/dashboard/app.js:956](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L956), `H/retarget-loop.sh:38`, `lex:83`. was: US-49, OS-16.
Acceptance: while Paused a tick records 0 seat actions; a repeat click answers "already Paused".
Verdict: KEEP.

**MS-036** As the human (Tig today), I want loop mode live or dry-run, with a confirm only when going live, so that dry-run is safe and live is deliberate.
Evidence: [agent-harness/dashboard/rules.mjs:1543](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L1543), `lex:349`, `AH/__main__.py:748`. was: US-50, OS-16, OS-17.
Acceptance: switching to live opens a confirm, to dry-run does not; in dry-run every verb writes a record and sends 0 bytes to any vendor or GitHub.
Verdict: KEEP.

**MS-037** As the human (Tig today), I want the loop cadence settable from 1 to 60 minutes, so that I trade responsiveness for cost.
Evidence: [agent-harness/agent_harness/settings.py:409](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/settings.py#L409). was: US-51.
Acceptance: 0 and 61 are refused by the server; a non-integer is refused on the page.
Verdict: KEEP.

**MS-038** As the human (Tig today), I want every setting shown with its value, where it came from, and who changed it last and when, so that I can trust and audit settings.
Evidence: [agent-harness/dashboard/app.js:1141](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L1141). was: US-52.
Acceptance: 4 columns: Setting, Value, From (shipped default or instance), Changed by "email, ISO time".
Verdict: KEEP.

**MS-039** As the human (Tig today), I want a value checked against the store's schema before it saves, so that a typo fails on the page and not in the loop.
Evidence: [agent-harness/dashboard/rules.mjs:1517](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L1517). was: US-53.
Acceptance: invalid input shows "<label> must be <type>" and writes no version; the page and the server use one schema file.
Verdict: KEEP.

**MS-040** As the human (Tig today), I want a View Settings dump of every effective value with its source that I can copy, so that I can paste the config into an issue.
Evidence: [agent-harness/dashboard/app.js:892](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L892), `AH/settings.py:1834`. was: US-54.
Acceptance: JSON with `{value, source}` per key; a secret appears by name only; Copy says "Copied."
Verdict: KEEP.

**MS-041** As the human (Tig today), I want what I am typing kept when a frame arrives, so that live updates do not eat my edit.
Evidence: [agent-harness/dashboard/app.js:1202](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L1202), `D/app.js:1749`. was: US-56.
Acceptance: a field with unsaved text keeps its text and focus across 10 consecutive frames.
Verdict: CHANGE: the page patches changed rows instead of rebuilding the tab per frame (workaround 14).

**MS-042** As the human (Tig today), I want the page to say when the config store cannot be read, so that I know nothing is steered.
Evidence: [agent-harness/dashboard/app.js:1170](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L1170), `lex:343`. was: US-57.
Acceptance: the lead line reads "The config store is unmeasured: <reason>. Nothing is steered until it reads." and the loop records 0 steers.
Verdict: KEEP.

**MS-043** As the loop, I want every tunable read from the config store each tick, so that a tune needs no pull request.
Evidence: [agent-harness/agent_harness/settings.py:445](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/settings.py#L445), `lex:367`. was: US-58.
Acceptance: a save writes one version and one log line; the next tick's records cite the new version.
Verdict: CHANGE: the key set shrinks to Mike's (loop window, read reserve, fill-missing cap, shares, mint thresholds); paste, pe-retarget, main-restart lists and redelivery keys go.

### 1.6 Diagnose and health

**MS-044** As the human (Tig today), I want Health as the first tab with the snapshot age ticking, so that I see at a glance whether the data is fresh.
Evidence: [agent-harness/dashboard/app.js:606](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L606), `D/rules.mjs:1339`. was: US-59.
Acceptance: "updated Ns ago" changes every second from an ISO `snapshot_ts`; with none it reads "update time not recorded".
Verdict: KEEP.

**MS-045** As the human (Tig today), I want a Needs attention block that groups every fault by kind, worst first, with counts and links, so that I triage in one read.
Evidence: [agent-harness/dashboard/app.js:640](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L640), `AH/attention.py:254`. was: US-60.
Acceptance: the summary reads "N not ok, M unmeasured" or "Nothing needs attention."; not-ok groups precede unmeasured.
Verdict: KEEP.

**MS-046** As the human (Tig today), I want loop rows for heartbeat, mode, Running/Paused and timer, with the heartbeat stamped only by the loop, so that a stopped loop never reads as a Paused or healthy one.
Evidence: [agent-harness/dashboard/rules.mjs:635](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L635), `AH/__main__.py:523`, `H/retarget-loop.sh:28`. was: US-61, OS-43.
Acceptance: a hand run of a verb leaves the heartbeat unchanged; timer not active is marked fault; Paused is marked paused.
Verdict: CHANGE: no row for a poke heartbeat or a tick verb list; one loop, one heartbeat.

**MS-047** As the human (Tig today), I want the header to read "Loop Paused: <reason>" or "Loop timer not active" on every tab, so that I never miss a stopped loop.
Evidence: [agent-harness/dashboard/rules.mjs:969](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L969). was: US-62.
Acceptance: the line is on all tabs while Paused and absent while Running with the timer active.
Verdict: KEEP.

**MS-048** As the human (Tig today), I want a Hosts table with reachability, seat count, check-in age, checkout commit and pending actuations, so that I see which seat host is down.
Evidence: [agent-harness/dashboard/rules.mjs:775](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L775). was: US-63.
Acceptance: a host with a stale check-in is red with a note row; a host with 0 seats that never checked in is not in the payload.
Verdict: CHANGE: the server omits never-used hosts; the page filters nothing (workaround 8).

**MS-049** As the human (Tig today), I want the commit this control plane serves and how far the loop checkout is behind `main`, linked, so that I know whether a merge is live.
Evidence: [agent-harness/dashboard/rules.mjs:577](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L577). was: US-64.
Acceptance: "serving <branch · sha8>, started <ISO time>"; the loop checkout item says "N behind".
Verdict: KEEP.

**MS-050** As the human (Tig today), I want steers not confirmed counted per seat with a link to the matching log lines, so that I see lost deliveries.
Evidence: [agent-harness/agent_harness/attention.py:271](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/attention.py#L271), `D/app.js:708`. was: US-65.
Acceptance: the count equals the not-confirmed steer records in the window, for every runtime; "Show in log" opens a log view with exactly those lines.
Verdict: CHANGE: one delivery result for every runtime, not tmux pastes only.

**MS-051** As the human (Tig today), I want a mint anomaly named from the mint records, so that runaway minting is visible.
Evidence: [agent-harness/agent_harness/attention.py:119](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/attention.py#L119), `AH/api.py:2507`, `AH/api.py:2726`. was: US-67.
Acceptance: Health shows "no seat minted twice for one issue" as ok or names each seat and issue; a vendor session with no mint record is one red item.
Verdict: CHANGE: one check over mint records replaces six detectors for past defects (workaround 11).

**MS-052** As the human (Tig today), I want platform faults named (GitHub read budget, vendor account, store not writable, another loop on this store, runtime launcher missing on a seat host, process and tree disagree), so that I fix the platform before the fleet.
Evidence: [agent-harness/agent_harness/attention.py:212](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/attention.py#L212), `AH/attention.py:133`, `AH/attention.py:240`. was: US-68.
Acceptance: each fault appears as its own labelled group when not ok and clears on the next snapshot after the fault clears.
Verdict: CHANGE: the account check is per vendor, not Cursor only.

**MS-053** As the human (Tig today), I want a verb that refused N times in a row named, with each refusal's reason in its record, so that a broken verb shows and one cause is not buried under hundreds of rows.
Evidence: [agent-harness/agent_harness/api.py:606](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/api.py#L606), `briefs/infrastructure-pe.md:48`. was: US-69, OS-52.
Acceptance: "<verb> refusing (N in a row): <why>" appears at the threshold inside the window; a later applied record clears it.
Verdict: CHANGE: refusal streaks only; Mike has no holds (`mike.md` section 10.1).

**MS-054** As the human (Tig today), I want signed out, not allowed, unreachable and wrong version each said differently, so that a refusal never looks like a dead control plane.
Evidence: [agent-harness/dashboard/client.mjs:108](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/client.mjs#L108), `D/rules.mjs:31`. was: US-74.
Acceptance: four distinct texts; 401 and 403 do not retry; other failures retry every 3 s.
Verdict: KEEP.

**MS-055** As the human (Tig today), I want the live stream to recover by itself after sleep, a proxy drop or a control plane restart, so that an open tab stays true.
Evidence: [agent-harness/dashboard/client.mjs:280](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/client.mjs#L280), `D/app.js:2680`. was: US-75.
Acceptance: 45 s with no bytes, or a return to the tab, opens a new stream that resends every opening frame.
Verdict: KEEP.

**MS-056** As the human (Tig today), I want Health built from a snapshot the tick wrote, and a stale snapshot said on open pages, so that polling the page costs nothing and silence never reads as healthy.
Evidence: [agent-harness/agent_harness/api.py:3995](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/api.py#L3995), `spec:63`, `H/AGENTS.md:206`. was: US-76, OS-46.
Acceptance: a Health request makes 0 vendor and 0 GitHub calls (test); within one keep-alive after the loop window passes, one frame says "health snapshot stale" and parts read `unmeasured`.
Verdict: KEEP.

**MS-057** As the human (Tig today), I want to watch a tmux seat's pane in the browser and take control to type, one human at a time, so that I can unstick it without SSH.
Evidence: [agent-harness/dashboard/app.js:2451](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L2451), `D/rules.mjs:1607`, `H/terminal.sh:2`. was: US-09, OS-51.
Acceptance: view mode sends 0 keys; keys reach the pane only after Take control; the seat host defers steers and restarts while a human has control and runs each once after.
Verdict: KEEP.

### 1.7 Audit records

**MS-058** As the human (Tig today), I want the log under Health, filterable by level and up, component, seat, command, project and text, with the filter in the URL, so that I can share or reload a filtered view.
Evidence: [agent-harness/dashboard/app.js:1767](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L1767), `D/rules.mjs:1126`. was: US-78.
Acceptance: the URL carries `log_*` keys; Back and Forward restore the filter; Clear empties every field.
Verdict: CHANGE: adds a project filter (`mike.md` 1.2).

**MS-059** As the human (Tig today), I want a "since" log view that reads the whole window up to 2000 rows, so that a count on Health matches the lines I see.
Evidence: [agent-harness/dashboard/rules.mjs:1151](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L1151). was: US-79.
Acceptance: a since query sends `limit=2000`; rereads come at most every 30 s, one in flight.
Verdict: KEEP.

**MS-060** As the human (Tig today), I want every dashboard command recorded with my identity and its outcome, so that I can audit who did what.
Evidence: [agent-harness/agent_harness/api.py:4717](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/api.py#L4717), `AH/api.py:4861`. was: US-80.
Acceptance: one record per command, pending then applied, refused or cancelled, with `actor` and the job id.
Verdict: KEEP.

**MS-061** As the human (Tig today), I want every settings change stored as a new version with actor, and a history I can list, so that "who changed what" needs no pull request.
Evidence: [agent-harness/agent_harness/api.py:5131](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/api.py#L5131), `AH/__main__.py:4662`, `lex:343`. was: US-81, OS-15.
Acceptance: the answer says "saved as version N"; one log line names key, actor, from and to; `settings history` lists every version.
Verdict: KEEP.

### 1.8 Install and recover

**MS-062** As the human (Tig today), I want Hard Reboot (archive and remint every seat, restart the control plane), optionally with Reset Defaults, so that I can start the fleet clean.
Evidence: [agent-harness/dashboard/rules.mjs:1290](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L1290), `AH/seat_actuator.py:31`, `lex:281`, `lex:287`. was: US-39, OS-56.
Acceptance: one confirm; the record names the human actor; with Reset Defaults every seat ends idle and 0 `seat:` labels remain, written as one record; a seat token is refused.
Verdict: KEEP.

**MS-063** As Arthur (arbiter), I want an Orchestrator Reboot to archive and remint K and me with idle assignments, so that a confused orchestrator starts fresh.
Evidence: [agent-harness/dashboard/rules.mjs:1291](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L1291), `lex:293`. was: US-40.
Acceptance: only the `arbiter` and `tpm` role seats are reminted; both read idle afterwards.
Verdict: KEEP.

**MS-064** As the human (Tig today), I want Fill-Missing to adopt or mint every absent pool seat and leave live ones alone, capped per window, so that gaps close in one click.
Evidence: [agent-harness/dashboard/rules.mjs:1293](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L1293), `lex:275`. was: US-41.
Acceptance: 0 responding or unmeasured seats are reminted; at most `max_creates` per seat per `window_minutes`; the confirm states the mint count and the vendor each bills.
Verdict: CHANGE: adopt, not claim; never a lane-PE; the cost line comes from vendor config, not fixed text.

**MS-065** As the human (Tig today), I want a running fleet command shown as progress, and the server to refuse any command that collides with it, so that two commands cannot collide.
Evidence: [agent-harness/dashboard/rules.mjs:1005](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L1005), `AH/api.py:4804`. was: US-42.
Acceptance: "<mode>: step N of M, started by <actor>" shows to every viewer; the server answers 409 to a colliding seat verb or fleet mode.
Verdict: CHANGE: factory's seat verbs have no server busy check, only a client lock (workaround 2).

**MS-066** As the human (Tig today), I want to restart the control plane process from the page, even while Paused, so that I recover a stuck API without SSH.
Evidence: [agent-harness/dashboard/rules.mjs:1294](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L1294). was: US-55.
Acceptance: one confirm; the stream reconnects in under 10 s; 0 seats reminted.
Verdict: KEEP.

### 1.9 Identity and secrets

**MS-067** As the human (Tig today), I want to sign in with Microsoft, renew silently, and be told when a renewal needs me, so that a long session does not just die.
Evidence: [agent-harness/dashboard/client.mjs:158](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/client.mjs#L158), `D/app.js:259`. was: US-77.
Acceptance: a silent renewal shows "Your sign-in renewed silently." for 10 s; an interactive need redirects with a notice.
Verdict: CHANGE: identity provider, base path and origins are instance config (`mike.md` 7, #1).

### 1.10 Cost

**MS-068** As the human (Tig today), I want tokens per seat since its last mint and a fleet total that never counts unmeasured as zero, so that I see spend.
Evidence: [agent-harness/dashboard/app.js:530](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L530), `D/rules.mjs:266`. was: US-10.
Acceptance: the total reads "incomplete" with an unmeasured count when any seat is unmeasured; each bar is that seat's percent of the measured total.
Verdict: KEEP.

**MS-069** As the human (Tig today), I want each seat's context fullness, fullest first, so that I can remint a seat before it summarizes.
Evidence: [agent-harness/dashboard/rules.mjs:414](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L414), `D/app.js:491`. was: US-11.
Acceptance: measured seats sorted by percent descending; "summarized" marked; unmeasured seats last with their reason.
Verdict: KEEP.

**MS-070** As the human (Tig today), I want each vendor's included pools with percent used, age and overage, so that I know when we start paying more.
Evidence: [agent-harness/dashboard/app.js:363](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L363), `D/rules.mjs:427`, `AH/meters.py:16`. was: US-12.
Acceptance: one row per configured pool reading "N% used, <age>" or "unmeasured, <reason>"; a pool with no gauge source is named as not shown.
Verdict: CHANGE: pools come from vendor config, not two fixed Cursor names and a code tuple.

## 2. Operator, loop and seat stories

### 2.1 Observe the fleet

**MS-071** As a seat (any), I want to talk to the human by measurement, bad news first, with one recommendation, ordered decisions then merges then next, and cost unasked, so that the human reads one message and acts.
Evidence: [AGENTS.md:84](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/AGENTS.md#L84), `AGENTS.md:93`. was: OS 3.5.
Acceptance: each loaded brief contains the five rules (test); a report with a cost has a number and a unit.
Verdict: KEEP.

**MS-072** As a seat (any), I want my reported focus and check-in stored in the record's `detail`, never its `why`, so that the Sessions tab shows focus without hiding a refusal reason.
Evidence: [agent-harness/agent_harness/__main__.py:3024](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L3024), `H/README.md:49`. was: OS-26.
Acceptance: `detail.focus` and `detail.checked_in` written, `detail.present_keys` holds names only; `why` unchanged.
Verdict: KEEP.

### 2.2 Steer and assign

**MS-073** As Arthur (arbiter), I want every steer recorded before it is sent, and apply to refuse an unrecorded decision, so that no steer exists without a trail.
Evidence: [agent-harness/agent_harness/__main__.py:748](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L748), `AH/records.py:1`. was: OS-17.
Acceptance: for 100% of steers the record's write time precedes the send; apply with no record id is refused.
Verdict: KEEP.

**MS-074** As the human (Tig today), I want any worker steer onto a Low issue, or one with no severity, refused for every caller, so that spare capacity is never spent on Low.
Evidence: [agent-harness/agent_harness/severity_floor.py:1](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/severity_floor.py#L1). was: OS-18.
Acceptance: the refusal reads `severity floor: Low is never steered` with a record; an unreadable severity refuses as `unmeasured`.
Verdict: KEEP. The severity field name is instance config (`Priority` on factory).

**MS-075** As the loop, I want no mint, steer or restart decided on a seat whose liveness is unmeasured, so that a blind read cannot plan work over running seats.
Evidence: [agent-harness/agent_harness/liveness.py:1](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/liveness.py#L1), `briefs/infrastructure-pe.md:56`. was: OS-20.
Acceptance: with a seat `unmeasured`, 0 mints and 0 loop steers target it; each attempt is a refused record naming the reason.
Verdict: KEEP.

**MS-076** As a lane-PE, I want to file an issue with a severity and steer it to a worker instead of writing code, so that judgment stays separate from development.
Evidence: [agent-harness/briefs/factory-pe.md:79](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/briefs/factory-pe.md#L79), `briefs/infrastructure-pe.md:60`. was: OS-23.
Acceptance: 0 development pull requests authored by Arthur, K or lane-PE seats; `pr-check` names one as a finding; a `[none]` title prefix does not bypass it.
Verdict: KEEP.

**MS-077** As a seat (any), I want issue and pull-request writes through Mike's verbs, recorded first, through one GitHub module, so that no seat runs raw `gh` and no write comes from a read-only account.
Evidence: [agent-harness/agent_harness/gh.py:1](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/gh.py#L1), `H/README.md:122`. was: OS-28.
Acceptance: only one module spawns `gh` or calls the API (test); a write as the read-only account raises; a GraphQL mutation counts as a write.
Verdict: KEEP.

**MS-078** As the loop, I want every outbound steer, poke and mint prompt linted by Geas against the banned-terms table before sending, so that a banned word never reaches a seat.
Evidence: [agent-harness/agent_harness/geas.py:1](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/geas.py#L1), `briefs/arbiter.md:23`. was: OS-29.
Acceptance: a prompt with a banned term is refused with 0 bytes sent; the table comes from the project's hook, not from Mike.
Verdict: KEEP.

**MS-079** As the loop, I want a GitHub event on an issue or pull request routed to the seat its `seat:<name>` label names, so that the owner hears about a comment or review without polling.
Evidence: [agent-harness/agent_harness/poke.py:525](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/poke.py#L525), `AH/webhook.py:1`, `H/README.md:240`. was: operator report table 1b (`poke`), OS-45.
Acceptance: a signed webhook delivery produces one prompt of the form `[<owner>] GitHub poke (<reason>): <title>` within one tick; an unsigned delivery is refused.
Verdict: CHANGE: signed webhook is the design; polling the human's notifications is a fallback (`mike.md` 5).

**MS-080** As K (TPM), I want to post one nudge when a ready pull request has no owner self-review on its head, so that the gate is met by the owner, not waived.
Evidence: [agent-harness/briefs/tpm.md:55](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/briefs/tpm.md#L55). was: OS 3.2.
Acceptance: at most one nudge per pull request per head, in this shape:
```
[K (TPM)] <owner seat>, owner self-review is missing on <sha>.
```
Verdict: CHANGE: the name is the instance's TPM name; the sha is named.

**MS-081** As K (TPM), I want to send a follow-up once per idle stretch to a lane-PE idle past 30 minutes, with the measured idle time, 1 to 3 open items, and a reminder to use a cheaper model for grunt work, so that a stalled lane-PE moves without a human.
Evidence: [agent-harness/briefs/tpm.md:57](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/briefs/tpm.md#L57), `briefs/psde.md:27`. was: OS 3.2, OS-70.
Acceptance: 0 or 1 follow-ups per lane-PE per idle stretch; each names idle minutes and a last-activity ISO time.
Verdict: CHANGE: delivered as a follow-up steer through Mike, gated like every steer.

### 2.3 Review and merge

**MS-082** As a worker (Artificer), I want to open my pull request as a draft early, labelled `seat:<name>`, and mark it ready only with clean self-review and green CI on the same sha, so that other seats see which files I hold.
Evidence: [AGENTS.md:105](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/AGENTS.md#L105), `AGENTS.md:113`. was: OS-41.
Acceptance: `pull create` opens a draft by default; `pull ready` is refused unless self-review and CI name the current head.
Verdict: KEEP.

**MS-083** As a worker (Artificer), I want my self-review counted only in this exact shape, written by me, naming the head sha, so that a review of an old commit or prose about a review never passes the gate.
Evidence: [agent-harness/agent_harness/pr_state.py:41](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/pr_state.py#L41), `briefs/arbiter.md:62`. was: OS-30.
Acceptance: the gate matches `^\s*(\[[^\]\n]+\]\s*)?Self-Review:\s*Done\b`, finds the head sha (7 to 40 hex) in the comment, and the `[Name]` prefix equals the `seat:` owner; anything else does not count.
```
[Name] Self-Review: Done
Head: <sha>
```
Verdict: CHANGE: the old four-line form (`Lexicon: Clear.` and the rest) is refused by the gate, not only banned in briefs.

**MS-084** As a worker (Artificer), I want `pr-check` to name mechanical rule breaks (one `seat:` label naming a real seat, no `[Name]:` title, `Closes` in the same project, no development pull request from an orchestrator or lane-PE), so that review time is not spent on them.
Evidence: [agent-harness/agent_harness/__main__.py:2149](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L2149), `H/AGENTS.md:261`. was: OS-40.
Acceptance: `--strict` exits 1 on any finding; a cross-repository `Closes` is a finding.
Verdict: KEEP.

**MS-085** As the loop, I want each ready pull request given one reviewer, oldest-ready first, never its author and never a reviewer already holding a pull request without a verdict, so that every ready pull request gets an independent review in parallel.
Evidence: [agent-harness/agent_harness/review.py:123](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/review.py#L123). was: OS-34.
Acceptance: two ready pull requests and three idle reviewers give exactly two steers; mergeable `UNKNOWN` read twice is `unmeasured` naming the pull request.
Verdict: CHANGE: no reviewer waits behind a busy one (factory#1759); Arthur may order it, Mike enforces independence.

**MS-086** As a reviewer (Warden), I want `review <pr>` to print one results table naming the head and refuse when the head moved or a read failed, so that my review is of this commit only.
Evidence: [agent-harness/agent_harness/review.py:96](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/review.py#L96), `briefs/reviewer.md:17`. was: OS-31.
Acceptance: the table contains `| head | <sha> |`; a review without that table for the head does not clear the gate.
Verdict: KEEP.

**MS-087** As a reviewer (Warden), I want new tests copied onto a `main` worktree and run there and on the head, so that "fails on main, passes on head" is measured for code, config, schema and briefs.
Evidence: [agent-harness/briefs/reviewer.md:17](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/briefs/reviewer.md#L17), `AGENTS.md:132`. was: OS-32, OS 3.6.
Acceptance: the table has one main result and one head result per new test; a behavior finding without a failing test is not blocking.
Verdict: KEEP.

**MS-088** As a reviewer (Warden), I want my review in one fixed shape of at most 12 lines, so that the human reads it on a phone and the gate parses it.
Evidence: [agent-harness/briefs/reviewer.md:27](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/briefs/reviewer.md#L27), `briefs/reviewer.md:35`, `H/tests/test_comment_limits_1741.py:1`. was: OS-33.
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

**MS-089** As a seat (any), I want every comment to end with its next steps, one line each, each naming who does it, so that nobody has to infer the hand-off.
Evidence: [agent-harness/briefs/psde.md:34](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/briefs/psde.md#L34), `briefs/reviewer.md:43`, `AGENTS.md:104`. was: OS 3.2.
Acceptance: the last non-blank lines of every seat comment match `^Next: \S+ .+\.$`, and no non-`Next:` line follows them (test on a sample of 50 comments).
```
Next: <Seat> <does X>.
```
Verdict: KEEP.

**MS-090** As the human (Tig today), I want seat comments capped at 12 lines for a review, 20 for a pull request body, and 6 for any other comment, so that I read the fleet on a phone.
Evidence: [AGENTS.md:104](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/AGENTS.md#L104), `H/tests/test_comment_limits_1741.py:54`. was: OS-70, OS 3.3.
Acceptance: each loaded brief states the three limits (test); a pull request body has change, `Fixes #N` or `Advances #N`, test-first in one line, verdicts, merge order, follow-ups, and at most 20 lines.
Verdict: KEEP.

**MS-091** As a reviewer (Warden), I want to be unable to push a fix or open a development pull request, so that review stays independent.
Evidence: [agent-harness/briefs/reviewer.md:23](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/briefs/reviewer.md#L23). was: OS-42.
Acceptance: 0 commits by a reviewer seat on a development path; a bug a reviewer finds becomes 1 issue with a severity and a steer to a worker.
Verdict: CHANGE: a push by a reviewer seat token is refused by mechanism, not only by the brief (`mike.md` 3.3.9).

**MS-092** As the human (Tig today), I want every gate pinned to the head sha, so that a new commit voids self-review, CI and review.
Evidence: [agent-harness/agent_harness/merge_gate.py:1](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/merge_gate.py#L1), `AH/pr_state.py:39`. was: OS 3.6.
Acceptance: pushing one commit after a `Merge` review moves the pull request's next step back to self-review within one tick.
Verdict: KEEP.

**MS-093** As a worker (Artificer), I want a send-back to return my pull request to draft and come back to me as my next assignment, so that the fix lands on the seat that has the context and nobody else waits.
Evidence: [agent-harness/agent_harness/draft_sent_back.py:1](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/draft_sent_back.py#L1). was: OS-35.
Acceptance: after `Send back` on the head, the pull request is draft within one tick and the author seat's next assignment is that pull request; a send-back naming an older sha does nothing.
Verdict: CHANGE: send-back is a first-class state on the board, and no seat waits on it (`mike.md` 3.4).

**MS-094** As a worker (Artificer), I want a ready pull request that turns conflicting, or gets unresolved Copilot threads on its head, sent back to me once, so that I fix it without a human polling.
Evidence: [agent-harness/agent_harness/conflict_steer.py:243](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/conflict_steer.py#L243), `AH/copilot_review.py:53`. was: OS-36, OS-37.
Acceptance: one send-back per pull request per head per cause; the prompt names the cause and says "Merge origin/main. Never rebase on a shared branch."
Verdict: CHANGE: kept as wakes until the planner is gone, then routed as send-backs (decision 5).

**MS-095** As the human (Tig today), I want Mike to request merge from the configured merger exactly when self-review, CI, ready and a `Merge` review all name the same head, so that my assignment list is my merge queue.
Evidence: [agent-harness/agent_harness/assign_tig.py:1](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/assign_tig.py#L1), `AH/merge_gate.py:30`. was: OS-38.
Acceptance: a draft never gets a request; a pull request already assigned to the merger is not re-requested; the merger login comes from config.
Verdict: CHANGE: request merge, not assign-tig.

**MS-096** As the human (Tig today), I want Mike to have no merge verb, so that only a human merges.
Evidence: [agent-harness/agent_harness/merge_gate.py:5](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/merge_gate.py#L5), `briefs/psde.md:11`. was: OS-38, OS 3.4.
Acceptance: a test fails if any verb, route or GitHub call that merges is added.
Verdict: KEEP.

**MS-097** As the human (Tig today), I want to waive a gate with a comment and grant a reviewer with a comment, honored only from my account, so that I unblock without editing code.
Evidence: [agent-harness/agent_harness/pr_state.py:89](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/pr_state.py#L89), `AH/merge_gate.py:44`, `H/README.md:139`. was: OS-39.
Acceptance: a waiver or grant from any seat is ignored and recorded; an unpinned waiver expires on the next commit; each honored waiver is a record.
```
waive: <self_review|ci|ready|ir|all> [sha]
reviewer: <Name>
```
Verdict: CHANGE: honored from the configured merger account, not a hard-coded `tig`.

### 2.4 Manage seats

**MS-098** As Arthur (arbiter), I want a remint to archive the live session and mint one new session for the same name, and to refuse unknown or over-cap names, so that one name is always exactly one agent.
Evidence: [agent-harness/agent_harness/__main__.py:1380](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L1380), `AGENTS.md:46`. was: OS-09.
Acceptance: after a remint the vendor lists 1 live session for the name; a name beyond the pool cap is refused with a record.
Verdict: CHANGE: the verb is remint for every runtime, writing one record, not a Cursor-shaped create.

**MS-099** As a seat (any), I want to be minted wait-only and receive work only through a steer, so that a mint costs little and is never read as permission to pick work.
Evidence: [agent-harness/agent_harness/initial_prompt.py:30](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/initial_prompt.py#L30), `H/README.md:73`. was: OS-10.
Acceptance: for every role, lane-PEs included, the mint prompt ends at "Wait for the first steer" and the mint run reads 0 issues.
Verdict: CHANGE: factory makes only worker mints wait-only; a lane-PE mint read 4.2M and 5.0M tokens in 30 minutes (factory#1755).

**MS-100** As a seat (any), I want my first steer after a mint or remint rendered by code from config, naming my assignment, so that no hand-written standing prompt drifts from Mike.
Evidence: [agent-harness/agent_harness/initial_prompt.py:384](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/initial_prompt.py#L384), `AH/idle_steer.py:688`. was: OS-11, OS 3.2.
Acceptance: the remint steer matches this shape and passes the brief byte-budget test; "Do not take priority order from this prompt." and "Unset severity is Low." appear in orchestrator first steers.
```
[<Name>] Fresh instance, same name. Assignment: <owner/repo>#N (<url>).
Read it in full. Draft the pull request before the first behavior change. Test first. Do not merge.
When the pull request is merged or closed, stop and wait for the next steer. Do not pick new work yourself.
```
Verdict: CHANGE: one template for every remint; the boards and report-and-wait lines go.

**MS-101** As the loop, I want the pool brought to its configured size without ever minting twice, so that the fleet converges without a human.
Evidence: [agent-harness/agent_harness/mint_standing.py:1](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/mint_standing.py#L1). was: OS-12.
Acceptance: a pending mint or a live session for a name gives 0 new mints; an unreadable vendor listing gives 0 mints and a refused record.
Verdict: CHANGE: the pool is a cap and a name list; a seat is killed only when stale or at the cap (decision 11).

**MS-102** As the human (Tig today), I want a fleet read that names untracked, missing and duplicate vendor sessions per runtime, and an apply that adopts or archives them, so that orphan agents stop accumulating.
Evidence: [agent-harness/agent_harness/fleet.py:1](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/fleet.py#L1). was: OS-13.
Acceptance: the read writes nothing; after apply each name has exactly 1 live session; a refused listing reads `unmeasured`.
Verdict: CHANGE: one actuator listing per runtime, not Cursor only; adopt, not claim.

**MS-103** As Arthur (arbiter), I want restart to use the seat's recorded launch script and seat host, so that a tmux seat never relaunches with the wrong directory, model or host.
Evidence: [agent-harness/agent_harness/__main__.py:1651](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L1651), `H/README.md:110`. was: OS-53.
Acceptance: a restart of a seat on another host becomes a pending actuation for that host and runs 0 tmux commands on the control-plane host; a missing launcher refuses by name.
Verdict: KEEP.

### 2.5 Configure

**MS-104** As a lane-PE, I want a seat host's runtime files rendered from instance config with a report of what differs, and an apply that fixes only that, so that a host is config-as-code.
Evidence: [agent-harness/README.md:179](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/README.md#L179). was: OS-03.
Acceptance: report-only by default; apply writes nothing outside the configured root; a launch script without the generated-by marker is refused without `--force`.
Verdict: CHANGE: rendered from instance config, not `seats.yaml`; no ladder step check.

### 2.6 Diagnose and health

**MS-105** As a lane-PE, I want one structured log, rotated, secrets redacted, with every verb's start and end, so that I can rebuild a miss a week later.
Evidence: [agent-harness/agent_harness/harness_log.py:1](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/harness_log.py#L1), `H/logs.sh:2`, `H/README.md:222`. was: OS-44.
Acceptance: every verb logs start and end with exit code and ms; a failure leaves a line even at exit 0; a scan of 7 days finds 0 secret values.
Verdict: CHANGE: the file is `mike.jsonl`; a new signal is a log line first (`mike.md` 5).

**MS-106** As a lane-PE, I want a written path from "it did not fire" to one cause, so that I answer it without reading code.
Evidence: [agent-harness/README.md:240](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/README.md#L240). was: OS-45.
Acceptance: each branch (no event line, dry-run, `error=`, event id absent, gauge `unmeasured`) maps to exactly one cause.
Verdict: CHANGE: starts from the webhook event and the decision record, not the notification poll.

**MS-107** As the loop, I want every GitHub-reading verb skipped for the tick when the read budget is below the reserve, so that polling cannot exhaust the token.
Evidence: [agent-harness/agent_harness/read_budget.py:1](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/read_budget.py#L1), `H/retarget-loop.sh:64`. was: OS-49.
Acceptance: with remaining below `read_budget_reserve`, the tick records the number and makes 0 GitHub reads beyond the budget read.
Verdict: KEEP.

**MS-108** As a lane-PE, I want remints per seat counted between two times from the records, so that I can measure churn.
Evidence: [agent-harness/agent_harness/__main__.py:705](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L705). was: OS-50.
Acceptance: the count writes nothing and equals the applied mint and remint records for that seat in the range.
Verdict: KEEP.

**MS-109** As the human (Tig today), I want each reason the loop cannot run named as its own token, so that I never read healthy for a loop that does not run.
Evidence: [agent-harness/README.md:208](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/README.md#L208). was: OS-04.
Acceptance: timer absent, timer inactive, another loop on the store, and checkout off branch each read as a distinct Health value; an unreadable scheduler reads `unmeasured`, never empty.
Verdict: CHANGE: one timer unit per instance and a store lock replace cron-line repair.

### 2.7 Install and recover

**MS-110** As the human (Tig today), I want one command that installs the tool stack on Linux or Windows, so that a fresh machine reaches ready without a package list in my head.
Evidence: [agent-harness/install.sh:2](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/install.sh#L2), `H/install.md:11`. was: OS-01.
Acceptance: the check exits 0 with every must-have present, exits 1 naming the installer to run; `--check-only` changes nothing.
Verdict: KEEP.

**MS-111** As a seat host, I want a cloud setup script that installs only the delta over the vendor image and never fails the session, so that cloud seats boot with pinned tools.
Evidence: [agent-harness/cloud-environment.sh:2](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/cloud-environment.sh#L2). was: OS-02.
Acceptance: exits 0 on every run in under 5 minutes; a second run on the same machine is a no-op.
Verdict: KEEP.

**MS-112** As the loop, I want one timer that starts a tick 60 s after the last one finished and never overlaps it, so that two ticks never act at once.
Evidence: [agent-harness/deploy/control-plane/hgl-control-loop.timer:7](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/deploy/control-plane/hgl-control-loop.timer#L7), `H/deploy/control-plane/run.sh:4`. was: OS-05.
Acceptance: over 24 hours, 0 tick start times fall inside another tick's run; one loop per instance.
Verdict: KEEP.

**MS-113** As the human (Tig today), I want the control plane deployed from the instance's checkout and restarted by a narrow root helper, so that a deploy needs no shell on the control-plane host.
Evidence: [agent-harness/deploy/control-plane/apply-unit.sh:1](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/deploy/control-plane/apply-unit.sh#L1). was: OS-06.
Acceptance: the restart action neither fetches nor installs; the helper never starts or stops the loop timer.
Verdict: KEEP.

**MS-114** As the human (Tig today), I want an end-to-end proof on a real seat host for event routing, gauges and confirmed steer delivery, posted on the pull request before ready, so that a green contract test is not mistaken for a working host.
Evidence: [agent-harness/e2e-box.md:1](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/e2e-box.md#L1), `briefs/infrastructure-pe.md:36`. was: OS-07.
Acceptance: stdout has one line per part, each a number, an id, or `unmeasured`; the pull request carries the output before ready.
Verdict: CHANGE: the retarget and ladder lines go; one delivery line per runtime comes in.

**MS-115** As the loop, I want seats running code that a `main` move changed reminted, and all actuation stopped when the loop's own checkout lacks the fetched `main`, so that a broken fetch cannot steer live seats with old code.
Evidence: [agent-harness/agent_harness/main_restart.py:1](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/main_restart.py#L1), `H/retarget-loop.sh:73`. was: OS-54.
Acceptance: a docs-only `main` move remints 0 seats; with the checkout behind, the tick records 0 seat actions and one refusal.
Verdict: CHANGE: the preserve and remint name lists go; what a seat runs is read from config.

**MS-116** As the loop, I want the control plane restarted once, recorded first, when the commit it serves differs from the instance checkout, so that a merged fix reaches the API.
Evidence: [agent-harness/agent_harness/serve_restart.py:1](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/serve_restart.py#L1). was: OS-55.
Acceptance: the decision record precedes the restart; a missing unit or helper refuses by name; unreadable health is `unmeasured`.
Verdict: KEEP.

**MS-117** As a lane-PE, I want a stale pending actuation backlog discarded without touching claimed ones, so that a returning seat host does not replay old steers.
Evidence: [agent-harness/agent_harness/__main__.py:3196](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L3196). was: OS-58.
Acceptance: matching pending rows become refused with `why: stale-backlog`; claimed rows are unchanged.
Verdict: CHANGE: the store expires a pending actuation after a configured age as well, so a discard is rarely needed.

**MS-118** As a seat host, I want a vendor usage-limit dialog on a grok-tmux pane dismissed with that dialog's own key, so that a seat stuck on a modal resumes.
Evidence: [agent-harness/agent_harness/tmux.py:188](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/tmux.py#L188), `AH/seat_host.py:1555`. was: OS-59.
Acceptance: dismissed only when the heading and the `Shift+x:dismiss` footer are both on the pane; a sign-in prompt gets 0 keys; not retried.
Verdict: CHANGE: lives in the grok-tmux runtime adapter behind the actuator interface, not in core.

**MS-119** As the loop, I want expired reserved-prefix branches deleted, and a no-op run still recorded, so that throwaway branches do not pile up and silence does not mean "did not run".
Evidence: [agent-harness/agent_harness/reap.py:1](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/reap.py#L1). was: OS-60.
Acceptance: a branch without the prefix or younger than `max_age_days` is untouched; each run writes one record.
Verdict: KEEP.

### 2.8 Identity and secrets

**MS-120** As the human (Tig today), I want a vendor key stored by hidden prompt, mode 600, and its account checked against config, so that a key is never in history and spend lands on the right account.
Evidence: [agent-harness/agent_harness/__main__.py:2093](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L2093), `AH/cursor_account.py:1`. was: OS-62.
Acceptance: file mode 600; the key is in no log, record or argv; a key on the wrong account is a Health fault and mint refuses.
Verdict: CHANGE: one check per vendor, not Cursor only.

**MS-121** As a lane-PE, I want secrets kept in a directory outside live state and referenced by name, so that wiping live state does not drop credentials.
Evidence: [agent-harness/load-secrets.sh:2](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/load-secrets.sh#L2). was: OS-63.
Acceptance: after deleting live state, the next verb finds its credentials; 0 secret values in logs, records or check-ins.
Verdict: CHANGE: the config store names each secret; no wrapper exports all of them into every verb's environment.

**MS-122** As the human (Tig today), I want no seat able to post, review, push or run GitHub calls as the human merger, and Arthur's GitHub token read-only, so that a waiver or approval in my name cannot be forged.
Evidence: [AGENTS.md:59](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/AGENTS.md#L59), `AH/gh.py:1`, `briefs/arbiter.md:41`. was: OS-64.
Acceptance: a write as the merger account from Mike raises; `waive:` is honored only from that account.
Verdict: KEEP.

**MS-123** As a seat host, I want a host token that names one host and a verified bearer on every pull, check-in and result, so that a compromised host can act only for itself.
Evidence: [agent-harness/agent_harness/__main__.py:3387](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L3387), `AH/seat_tokens.py:1`, `H/AGENTS.md:223`. was: OS-65.
Acceptance: a check-in naming another host is refused; signature, iss, aud, tid, exp and nbf are all checked; the identity read lists roles with no secret.
Verdict: KEEP.

**MS-124** As a seat (any), I want writer, owner and addressee carried by fixed marks, so that nobody is ambiguous across GitHub accounts.
Evidence: [AGENTS.md:48](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/AGENTS.md#L48), `AH/pr_state.py:39`, `AH/poke.py:30`. was: OS-66, OS 3.2.
Acceptance: gate parsers accept an optional `[Name] ` prefix and nothing else; 0 open titles match `[Name]:`; routing reads only the label.
```
[Name] <text>        written by seat Name
Name: <text>         addressed to seat Name
seat:<name>          label: the seat that owns this issue or pull request
```
Verdict: KEEP.

### 2.9 Cost

**MS-125** As the loop, I want every gauge to read `unmeasured` with a reason rather than a guessed percent, and a reading older than its stale window treated as `unmeasured`, so that no decision runs on stale or invented data.
Evidence: [agent-harness/agent_harness/write_meters.py:1](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/write_meters.py#L1), `H/README.md:150`. was: OS-48.
Acceptance: every absent source yields the literal `unmeasured` and a `why`; a `5% left` line parses to 95 used; text without a percent is `unparsed`.
Verdict: CHANGE: gauge sources are config; a vendor usage API is preferred over a screen scrape (section 10.19).

**MS-126** As a seat (any), I want to price a spend before it runs and report cost unasked, so that the human only says yes to money he can see.
Evidence: [AGENTS.md:117](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/AGENTS.md#L117), `briefs/factory-pe.md:49`. was: OS-67.
Acceptance: model-call spend under USD 100 needs no ask and is reported; any other spend, or over USD 100, waits for a yes; the price is a number from a measurement.
Verdict: KEEP.

**MS-127** As the loop, I want one read of open pull requests per project per tick and severity in one paged read, so that a 60 s tick fits its budget.
Evidence: [agent-harness/retarget-loop.sh:64](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/retarget-loop.sh#L64), `H/AGENTS.md:203`. was: OS-69.
Acceptance: GitHub reads per tick equal 1 pull-request page per project plus 1 severity connection per project; a failed page is not reused.
Verdict: CHANGE: per project across the instance; webhook events cut the reads further.

## 3. Stories mike.md requires that neither source had

### 3.1 Review surface

**MS-128** As the human (Tig today), I want a review surface listing every ready pull request, the reviewer assigned to each, and each verdict on the current head, so that I see review state without opening GitHub.
Evidence: [agent-harness/dashboard/rules.mjs:57](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L57) (the router has no review route); `mike.md` 7.
Acceptance: the rows equal the open non-draft pull requests across all projects; each shows reviewer or `none`, and `Merge`, `Send back`, `Hold` or `pending` for the head sha.
Verdict: NEW.

**MS-129** As the human (Tig today), I want the review surface ordered by the time each pull request went ready, oldest first, with send-backs and their author seats listed apart, so that the oldest wait is on top.
Evidence: [agent-harness/agent_harness/review.py:123](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/review.py#L123); `mike.md` 3.4.
Acceptance: row order equals ascending ready time from GitHub events; each send-back row names the author seat and its next-assignment state.
Verdict: NEW.

**MS-130** As the loop, I want the reviewer pool sized at `ceil(workers / 3)`, with one reviewer per ready pull request inside it, so that review keeps pace with work.
Evidence: [factory#1336](https://github.com/excaliwire/factory/issues/1336) section 1 point 5; `mike.md` decision 3.
Acceptance: with 9 workers the pool cap is 3; with 2 ready pull requests and 3 idle reviewers, 2 are steered.
Verdict: NEW.

### 3.2 The board

**MS-131** As Arthur (arbiter), I want the board on each board change or newly idle seat (idle seats, each seat's assignment, send-backs with author seat, ready pull requests per seat, target and actual share per row), so that I decide who does what from one read.
Evidence: [agent-harness/agent_harness/idle_steer.py:1279](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/idle_steer.py#L1279) (the follow-up carries no board); `mike.md` 3.1, decision 1.
Acceptance: the factory#1761 state yields a board naming the 3 send-backs as next assignments; a tick with idle workers writes 0 planner rows.
Verdict: NEW.

**MS-132** As the human (Tig today), I want the board Arthur last read shown on the dashboard with its tick time, so that I can judge his choices against the same input.
Evidence: [agent-harness/dashboard/rules.mjs:57](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L57) (no board view); `mike.md` 7.
Acceptance: the page payload's board equals, byte for byte, the board in Arthur's last follow-up record.
Verdict: NEW.

**MS-133** As a worker (Artificer), I want Mike to refuse any steer that moves me off an open assignment, so that I keep my context and a change of work is a remint.
Evidence: [factory#1336](https://github.com/excaliwire/factory/issues/1336) section 3 (Avalon lost context 4 times on 2026-09-26); `mike.md` 3.2.
Acceptance: a steer naming a different item than the seat's open assignment is a refused record; a remint onto the same item is applied.
Verdict: NEW.

**MS-134** As Arthur (arbiter), I want the instance's role names renamable in config, so that renaming a seat needs no code change and no migration verb.
Evidence: [factory#1164](https://github.com/excaliwire/factory/issues/1164); [agent-harness/agent_harness/policy.py:214](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/policy.py#L214); `mike.md` 2.
Acceptance: renaming the `arbiter` default in config changes 0 code files and every record keeps the stable seat id.
Verdict: NEW.

### 3.3 Target versus actual share

**MS-135** As the human (Tig today), I want a share per priority rank in the config store (top 60, second 30, third 10 percent of workers) that I can change, with an empty row's share passed to the next, so that I set the split, not each assignment.
Evidence: [factory#1336](https://github.com/excaliwire/factory/issues/1336) section 3; `mike.md` 3.1.
Acceptance: the three shares are config-store keys summing to 100; a row with 0 open non-Low issues shows target 0 and the next row's target rises by its share.
Verdict: NEW.

**MS-136** As the human (Tig today), I want Health to show target versus actual share per priority row, so that a bad judgment by Arthur is visible.
Evidence: [factory#1336](https://github.com/excaliwire/factory/issues/1336) section 4; `mike.md` 9.17.
Acceptance: each row shows target percent and actual percent of assigned workers from labels; a gap over 20 points for 3 ticks is one attention item.
Verdict: NEW.

### 3.4 Job ids for commands

**MS-137** As the human (Tig today), I want every command to return a job id at once, and its answer to land on a row I can see whenever it finishes, so that an answer after 30 s is not lost.
Evidence: [agent-harness/agent_harness/api.py:4726](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/api.py#L4726) (synchronous `run_verb`), `D/rules.mjs:1043`; `mike.md` 7.
Acceptance: every command POST answers in under 1 s with a job id; a verb that takes 120 s shows its outcome on that job's row.
Verdict: NEW.

**MS-138** As the human (Tig today), I want every time on the wire in ISO 8601 with offset, so that the page never parses prose or guesses a year.
Evidence: [agent-harness/agent_harness/api.py:478](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/api.py#L478) (`format_for_human`), `D/rules.mjs:490`; `mike.md` 7.
Acceptance: a schema test finds 0 time fields not matching ISO 8601 with offset; the page has 0 time-zone tables.
Verdict: NEW.

### 3.5 Phone layout

**MS-139** As the human (Tig today), I want every tab readable on a phone, so that I run the fleet away from my desk.
Evidence: [agent-harness/dashboard/app.css:125](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.css#L125) (no breakpoint for the 8-column Sessions table). was: US-07.
Acceptance: at 375 px width, 0 tabs need horizontal page scroll.
Verdict: CHANGE: today Sessions fails; Mike lays out every tab, review surface and board included.

**MS-140** As the human (Tig today), I want every single-seat verb reachable by tap, so that I need no right-click.
Evidence: [agent-harness/dashboard/app.js:1598](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L1598) (context menu, no touch path). was: US-36.
Acceptance: on a touch device each of the 5 seat verbs is reachable within 2 taps from the Sessions row.
Verdict: CHANGE: today the per-row menu needs a right-click.

### 3.6 Multi-project, single instance

**MS-141** As the human (Tig today), I want one Mike instance to manage several projects with one loop, one store, one dashboard and one priorities list, so that I do not deploy Mike per repository.
Evidence: [tig/mike#2](https://github.com/tig/mike/issues/2); `mike.md` 1.2, decision 6.
Acceptance: an install with no factory checkout manages two projects from one instance and passes the ported contract tests.
Verdict: NEW.

**MS-142** As the human (Tig today), I want a verb on a repository not on the instance's project list refused before any call runs, for every caller, so that no seat works outside the program.
Evidence: [agent-harness/agent_harness/__main__.py:1425](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L1425) (`cmd_steer` does not check), `AH/__main__.py:121`; `mike.md` 3.3.2.
Acceptance: a steer, mint or GitHub write naming an unlisted repository makes 0 GitHub or vendor calls and writes one refused record.
Verdict: NEW.

**MS-143** As a seat (any), I want every verb that touches GitHub to take the project explicitly, so that `#N` is never ambiguous across projects.
Evidence: [agent-harness/agent_harness/__main__.py:748](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L748) (`cmd_steer`); `mike.md` 1.2.
Acceptance: a GitHub verb called without a project is refused; every record and log line of such a verb has a `project` field.
Verdict: NEW.

### 3.7 Vendor budgets and mint threshold

**MS-144** As the human (Tig today), I want each vendor to declare its pools, windows, probe and mint threshold in config, so that budgets change without code.
Evidence: [agent-harness/agent_harness/meters.py:16](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/meters.py#L16) (`GAUGES` is a code tuple); `mike.md` 4.
Acceptance: adding a vendor pool is a config edit with 0 code changes and its gauge appears on the Gauges tab.
Verdict: NEW.

**MS-145** As the loop, I want mint to pick the next vendor when one crosses its mint threshold, so that a vendor limit costs a vendor switch, not a stall.
Evidence: [factory#1501](https://github.com/excaliwire/factory/issues/1501) (at 75 percent of Claude's 5-hour limit, stop minting Claude seats); `mike.md` 4.
Acceptance: with the Claude 5-hour gauge at 76 percent, the next mint record names a different vendor and cites the gauge reading.
Verdict: NEW.

**MS-146** As the loop, I want a mint that depends on an unmeasured gauge refused, so that an unknown budget is never read as free.
Evidence: [agent-harness/agent_harness/meters.py:73](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/meters.py#L73); `mike.md` 4.
Acceptance: with the vendor gauge `unmeasured`, 0 mints on that vendor; each attempt is a refused record naming the gauge; the gauge never reads 0.
Verdict: NEW.

**MS-147** As the human (Tig today), I want each mint run capped by a token and turn budget and cancelled with a record when over, so that a mint cannot burn millions of tokens.
Evidence: [factory#1755](https://github.com/excaliwire/factory/issues/1755); `mike.md` 3.2.
Acceptance: a mint run over its budget ends cancelled with a record naming tokens and turns used.
Verdict: NEW.

### 3.8 Runtime symmetry

**MS-148** As the loop, I want one actuator interface (mint, steer, stop, restart, archive, liveness, usage) that every runtime fills or answers `unmeasured` with a reason, so that no runtime has a special path in core.
Evidence: [agent-harness/agent_harness/seat_actuator.py:353](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/seat_actuator.py#L353); factory#1336 learnings 6, 11; `mike.md` 4.
Acceptance: a contract test runs the 7 capabilities against each configured runtime and gets a result or `unmeasured` plus reason for each.
Verdict: NEW.

**MS-149** As a worker (Artificer), I want every steer on every runtime confirmed by a run id, pane echo or event id, or reported not confirmed, so that I never get a duplicate or a lost task.
Evidence: [agent-harness/agent_harness/seat_host.py:934](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/seat_host.py#L934), `AH/seat_host.py:1730`, factory#1630. was: OS-24.
Acceptance: each steer record ends `confirmed` with an id or `not confirmed` with a reason; a confirmed steer is never resent.
Verdict: CHANGE: factory confirms tmux pastes and Cursor runs differently; Mike has one result field for all runtimes.

**MS-150** As the human (Tig today), I want mint, archive, restart and kill each to write a decision record of one shape for every runtime, so that Health can show a row clear and "no seat minted twice for one issue".
Evidence: [agent-harness/agent_harness/seat_actuator.py:1499](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/seat_actuator.py#L1499) (log lines only); factory#1418.
Acceptance: each actuation has one record before it acts; Health reads only that record shape (test with one runtime of each kind).
Verdict: NEW.

**MS-151** As the human (Tig today), I want no second steer to a seat while one is pending in the loop window, for every caller and every runtime, pending ones included, so that a seat never gets two tasks at once.
Evidence: [agent-harness/agent_harness/__main__.py:1054](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L1054) (`_loop_steer_hold` covers the loop and applied rows only); `mike.md` 3.3.5.
Acceptance: a human steer, an Arthur steer and a loop steer sent to one seat inside the window give 1 applied and 2 refused records.
Verdict: NEW.

### 3.9 Seat and host scoped tokens

**MS-152** As a seat (any), I want my token to name me and act only as me, so that a leaked seat token cannot steer or mint another seat.
Evidence: [agent-harness/seats.yaml:57](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/seats.yaml#L57) (caller matrix); `mike.md` 4, 9.12.
Acceptance: a seat token used on any other seat's self-verb is refused with a record; Arthur's and lane-PE steers pass only the matrix rows for their role.
Verdict: NEW.

**MS-153** As a seat host, I want no shared master secret on my machine and no inbound path or SSH key from the control plane, so that a compromised host cannot mint tokens for other seats.
Evidence: [docs/host.md:258](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/host.md#L258), factory#1413; `mike.md` 4.
Acceptance: a scan of each seat host finds 0 files that can mint a token for another seat; the control-plane host holds 0 SSH keys to seat hosts.
Verdict: NEW.

**MS-154** As the human (Tig today), I want to be a verified bearer, not a header any local process can set, so that a local script cannot act as me.
Evidence: [agent-harness/dashboard/serve.py:418](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/serve.py#L418) (adds `X-HGL-Email`); `mike.md` 4, section 10.8.
Acceptance: a request with only an email header and no verified bearer is refused 401 on every human-only route.
Verdict: NEW.

### 3.10 Config store apply-on-change

**MS-155** As the human (Tig today), I want a setting change applied live by the smallest action (reload, remint the affected seats, or swap a key), recorded, so that a change takes effect without a reboot.
Evidence: [factory#1524](https://github.com/excaliwire/factory/issues/1524); [agent-harness/agent_harness/settings.py:1258](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/settings.py#L1258); `mike.md` 5.
Acceptance: each save writes one record naming the action taken; a cadence change remints 0 seats; a role model change remints only that role's seats.
Verdict: NEW.

**MS-156** As the human (Tig today), I want desired state (roles, roster, projects, lanes, hosts, vendors, briefs) as instance config changed by pull request, shipped defaults in a separate file, and live state never in git, so that one source holds each fact.
Evidence: [agent-harness/agent_harness/store.py:3](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/store.py#L3); `mike.md` 5, section 10.16.
Acceptance: the instance config repository holds 0 live-state files; each setting has exactly one source (shipped default, instance config, or config store).
Verdict: NEW.

**MS-157** As the loop, I want the store owned by one locked process, append-only where it is a log, so that two writers never race and no row is silently replaced.
Evidence: [agent-harness/agent_harness/store.py:3](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/store.py#L3); `mike.md` 5, section 10.15.
Acceptance: a second process opening the store is refused and named on Health; a log row once written is never rewritten (test).
Verdict: NEW.

**MS-158** As the loop, I want a GitHub read that fails to read `unmeasured`, never empty, so that an outage does not look like "no work".
Evidence: [agent-harness/agent_harness/gh.py:100](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/gh.py#L100); `mike.md` 5.
Acceptance: with GitHub returning 502, the tick records `unmeasured` for each read and 0 steers or mints.
Verdict: NEW.

## 4. Retired stories

Not built (`mike.md` 3.3, 10, 12). One line each.

- US-21, "as the control plane reads it" with starved lanes: target versus actual share (MS-136) replaces it; lane-starved survives only as the lane gate's refusal text.
- US-26, redeliver-tries, conflict-steer cooldown, orchestrator cooldown: nothing is redelivered; Arthur's follow-up fires on a board change (decision 1).
- US-70, verbs holding on an unmeasured reading: there are no holds; a refusal streak is MS-053.
- US-71, assigned but never steered: the label is the assignment and the remint carries it (MS-034); the board shows it.
- US-72, fleet idle with work and the last planner reason: the planner is gone; the board and share rows show idle capacity.
- US-73, frozen lane focus: there is no lane owner to freeze.
- OS-19, the worker planner (steer-idle) with its 12 hold words, 12 none-eligible reasons and 9 wordless gates: Arthur decides from the board (section 10.1, 10.2).
- OS-21, enqueue and redeliver through `assign` and `assignments.jsonl`: one store, every steer through the control plane, no second queue (section 10.7).
- OS-25, stand-down and resume: a seat waiting on a gate gets a steer from Arthur ("wait for #N") (section 10.18).
- OS-57, reboot tail queueing one restart per grok-tmux orchestrator: the one-pending-actuation rule (MS-033) covers every runtime.
- OS-61, lane-PE host moves down the ladder: vendor budgets and mint thresholds replace the ladder (MS-144, MS-145).
- OS-68, ladder tier moves on included-pool gauges: same; the gauges stay (MS-070), the ladder goes.
- Owned-work preamble ("A send-back beats other owned work, and owned work beats a new ticket.", OS 3.2): a seat owns one assignment; a send-back is its next one.
- Seat-assignment Discussion board publisher (`dashboard --publish`, `--minimize-stale`, `dashboards_retired`; UI report 0.1, operator table 1b): retired boards, about 1300 dead lines (section 10.14).
- `retitle` one-shot migration (operator table 1b): finished on factory; not product code (section 10.20).
- `seat-rename` one-shot migration (operator table 1a): a stable seat id makes rename a config edit (MS-134).
- `Lexicon: Clear.` review line and the four-line self-review form (OS 3.2): retired on factory by #1741; line 1's verdict carries it.
